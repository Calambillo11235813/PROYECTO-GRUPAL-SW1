# backend/codigo/modelos/detector_hf.py
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import os
from datetime import datetime

class CodeDetectorHF:
    def __init__(self):
        # Ruta segura - buscar en code_detection-model-complete primero
        BASE = os.path.dirname(os.path.dirname(__file__))  # backend/codigo/
        
        # Intentar primero code_detection-model-complete
        carpeta_completa = os.path.join(BASE, "code_detection-model-complete")
        carpeta_ia = os.path.join(BASE, "modelo_ia")
        
        # Verificar cuál existe
        if os.path.isfile(os.path.join(carpeta_completa, "model.safetensors")):
            carpeta = carpeta_completa
        elif os.path.exists(carpeta_ia):
            carpeta = carpeta_ia
        else:
            raise FileNotFoundError(f"No se encontró modelo en {carpeta_completa} ni {carpeta_ia}")

        print("📌 Cargando modelo CodeBERT desde:", carpeta)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(
            carpeta,
            local_files_only=True
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            carpeta,
            local_files_only=True
        )

        self.model.to(self.device)
        self.version = "codebert-v1.0"
        self.timestamp = datetime.now().isoformat()

    def analizar(self, texto):
        inputs = self.tokenizer(
            texto,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=1)[0]

        # Según config.json:
        # Label 0 = "Ai_generated"
        # Label 1 = "Human_written"
        ai_prob_raw = float(probs[0])
        human_prob_raw = float(probs[1])
        
        # MEJORA: El modelo está sesgado hacia IA (da ~99% en Label 0 para todo)
        # Usamos heurísticas para corregir este sesgo de forma balanceada
        
        diferencia = ai_prob_raw - human_prob_raw
        es_ia_heuristica = self._analizar_heuristica(texto)
        
        # ESTRATEGIA: Combinar modelo y heurísticas de forma inteligente
        
        # Caso 1: Modelo muy confiado en IA (>95%) y heurísticas confirman (>0.4)
        if ai_prob_raw > 0.95 and es_ia_heuristica > 0.4:
            # Ambos confirman IA - mantener alta probabilidad del modelo
            ai_prob_ajustada = ai_prob_raw
            human_prob_ajustada = human_prob_raw
        
        # Caso 2: Modelo muy confiado en IA (>95%) pero heurísticas dicen humano (<0.3)
        elif ai_prob_raw > 0.95 and es_ia_heuristica < 0.3:
            # Conflicto: modelo dice IA, heurísticas dicen humano
            # Ajustar más agresivamente hacia humano cuando heurísticas son claras
            factor_correccion = 0.4 + (es_ia_heuristica * 0.3)  # Entre 0.4 y 0.7
            ai_prob_ajustada = ai_prob_raw * factor_correccion
            human_prob_ajustada = 1.0 - ai_prob_ajustada
        
        # Caso 3: Modelo moderado (80-95%) - combinar con heurísticas
        elif ai_prob_raw > 0.80:
            # Si heurísticas sugieren humano, dar más peso
            if es_ia_heuristica < 0.4:
                # Combinar: 60% modelo, 40% heurísticas (favorecer humano)
                ai_prob_ajustada = (ai_prob_raw * 0.6) + (es_ia_heuristica * 0.4)
            else:
                # Combinar: 75% modelo, 25% heurísticas (favorecer IA)
                ai_prob_ajustada = (ai_prob_raw * 0.75) + (es_ia_heuristica * 0.25)
            human_prob_ajustada = 1.0 - ai_prob_ajustada
        
        # Caso 4: Modelo bajo (<80%) - dar más peso a heurísticas
        else:
            # Combinar: 50% modelo, 50% heurísticas
            ai_prob_ajustada = (ai_prob_raw * 0.5) + (es_ia_heuristica * 0.5)
            human_prob_ajustada = 1.0 - ai_prob_ajustada
        
        # Ajuste final: solo si la diferencia es muy pequeña (<5%), favorecer ligeramente humano
        if abs(ai_prob_ajustada - human_prob_ajustada) < 0.05:
            human_prob_ajustada += 0.03
            ai_prob_ajustada = 1.0 - human_prob_ajustada
        
        is_ai = ai_prob_ajustada > human_prob_ajustada
        confidence = max(ai_prob_ajustada, human_prob_ajustada)

        return {
            "is_ai_generated": is_ai,
            "confidence": confidence,
            "ai_prob": ai_prob_ajustada,
            "human_prob": human_prob_ajustada,
            "ai_prob_raw": ai_prob_raw,  # Para debugging
            "human_prob_raw": human_prob_raw,  # Para debugging
            "method_used": "codebert_improved"
        }
    
    def _analizar_heuristica(self, texto):
        """
        Heurísticas mejoradas para detectar código generado por IA.
        Retorna un valor entre 0 y 1 (probabilidad de ser IA).
        """
        score = 0.0
        lineas = [l for l in texto.split('\n') if l.strip()]
        total_lineas = len(lineas)
        
        if total_lineas == 0:
            return 0.5  # Incertidumbre
        
        # ===== SEÑALES DE CÓDIGO IA (aumentan score) =====
        
        # Heurística 1: Docstrings detallados con Args/Returns (típico de IA)
        docstring_count = texto.count('"""') + texto.count("'''")
        if docstring_count >= 2:
            # Verificar si tiene formato estructurado (Args, Returns, etc.)
            if 'Args:' in texto or 'Returns:' in texto or 'Parameters:' in texto:
                score += 0.4
            else:
                score += 0.2
        
        # Heurística 2: Type hints exhaustivos (típico de IA)
        type_hints = texto.count('->') + texto.count(': int') + texto.count(': str') + \
                     texto.count(': list') + texto.count(': float') + texto.count(': bool')
        ratio_type_hints = type_hints / total_lineas if total_lineas > 0 else 0
        if ratio_type_hints > 0.15:  # Más del 15% de líneas con type hints
            score += 0.35
        elif ratio_type_hints > 0.08:
            score += 0.2
        elif ratio_type_hints > 0.03:  # Incluso pocos type hints sugieren IA
            score += 0.1
        
        # Heurística 3: Comentarios excesivos explicando lo obvio
        comentarios = texto.count('#')
        ratio_comentarios = comentarios / total_lineas if total_lineas > 0 else 0
        if ratio_comentarios > 0.35:  # Más del 35% son comentarios
            score += 0.25
        elif ratio_comentarios > 0.25:
            score += 0.15
        
        # Heurística 4: Nombres de variables/funciones muy descriptivos y largos
        palabras = texto.split()
        nombres_largos = sum(1 for p in palabras if len(p) > 15 and p.isalnum())
        if nombres_largos > total_lineas * 0.08:
            score += 0.2
        
        # Heurística 5: Manejo exhaustivo de excepciones (típico de IA)
        if texto.count('try:') > 0 and texto.count('except') > 1:
            score += 0.15
        
        # Heurística 5b: Patrones repetitivos y estructurados (típico de ChatGPT)
        # Múltiples funciones con estructura similar
        funciones = texto.count('def ')
        if funciones > 2:
            # Verificar si tienen estructura similar (patrón repetitivo)
            if texto.count('if ') > funciones * 1.5:  # Muchos ifs por función
                score += 0.25
            # Múltiples funciones pequeñas con estructura similar (típico ChatGPT)
            if funciones > 3 and total_lineas < 50:
                score += 0.2
            # Funciones con nombres muy descriptivos y verbos comunes (típico ChatGPT)
            if funciones > 2:
                score += 0.15
        
        # Heurística 5c: Patrones específicos de ChatGPT
        # Funciones que siguen el patrón: def nombre_verb(nombre_sustantivo):
        patron_chatgpt = texto.count('def process_') + texto.count('def validate_') + \
                        texto.count('def calculate_') + texto.count('def filter_') + \
                        texto.count('def get_') + texto.count('def set_') + \
                        texto.count('def check_') + texto.count('def handle_')
        if patron_chatgpt >= 2:
            score += 0.25
        elif patron_chatgpt == 1 and funciones >= 3:
            score += 0.15
        
        # Heurística 5d: Código simple pero muy estructurado (típico ChatGPT simple)
        # Sin docstrings ni type hints, pero muy limpio y estructurado
        if docstring_count == 0 and type_hints == 0 and funciones >= 3:
            # Verificar si es muy estructurado (muchos returns, muchos ifs)
            returns = texto.count('return ')
            ifs_count = texto.count('if ')
            if returns >= funciones and ifs_count >= funciones:
                score += 0.25
            # Múltiples funciones pequeñas y bien definidas (típico ChatGPT)
            if funciones >= 4 and total_lineas < 60:
                score += 0.2
            # Clases con métodos bien definidos pero sin documentación (típico ChatGPT)
            clases = texto.count('class ')
            if clases > 0 and funciones >= clases * 2:
                score += 0.15
        
        # Heurística 6: Validaciones de tipos extensas
        if texto.count('isinstance') > 2 or texto.count('type(') > 2:
            score += 0.15
        
        # Heurística 7: Código muy estructurado con clases bien definidas
        if texto.count('class ') > 0 and texto.count('def ') > 3:
            # Verificar si tiene métodos bien documentados
            if docstring_count > texto.count('class '):
                score += 0.1
        
        # ===== SEÑALES DE CÓDIGO HUMANO (reducen score) =====
        
        # Heurística 8: Código minimalista y directo (típico de humano)
        if total_lineas < 25 and type_hints == 0 and docstring_count == 0:
            score -= 0.35  # Reducido de 0.4 para no ser tan agresivo
        
        # Heurística 9: Prints de debug (típico de humano)
        print_count = texto.lower().count('print(')
        if print_count > 2:
            score -= 0.3
        elif print_count > 0:
            score -= 0.15
        
        # Heurística 10: Comentarios informales/casuales (típico de humano)
        comentarios_informales = texto.lower().count('todo:') + texto.lower().count('fix') + \
                                texto.lower().count('debug') + texto.lower().count('testing')
        if comentarios_informales > 1:
            score -= 0.25
        
        # Heurística 11: Espaciado inconsistente (típico de humano)
        lineas_vacias = texto.count('\n\n\n')  # Múltiples líneas vacías
        if lineas_vacias > 2:
            score -= 0.15
        
        # Heurística 12: Variables con nombres cortos (x, y, i, j, etc.)
        variables_cortas = sum(1 for palabra in palabras if len(palabra) == 1 and palabra.isalpha())
        if variables_cortas > total_lineas * 0.1:
            score -= 0.2
        
        # Heurística 13: Código con errores menores o estilo inconsistente
        # (sin type hints, sin docstrings, pero funcional)
        if type_hints == 0 and docstring_count == 0 and total_lineas > 10:
            score -= 0.15
        
        # Normalizar a rango [0, 1]
        score = max(0.0, min(1.0, score))
        
        return score
