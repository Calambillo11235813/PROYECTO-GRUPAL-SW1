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

        # NOTA: Aunque config.json dice Label 0="Ai_generated", Label 1="Human_written",
        # el modelo fue entrenado con etiquetas invertidas.
        # Label 0 = HUMANO (empíricamente verificado)
        # Label 1 = IA (empíricamente verificado)
        human_prob = float(probs[0])
        ai_prob = float(probs[1])

        return {
            "is_ai_generated": ai_prob > human_prob,
            "confidence": max(ai_prob, human_prob),
            "ai_prob": ai_prob,
            "human_prob": human_prob,
            "method_used": "codebert"
        }
