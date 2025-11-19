
"""
Ejemplos de uso del detector HF (CodeBERT-like) embebido en esta carpeta.

Este script carga el checkpoint local (model.safetensors, tokenizer.json, config.json)
y evalúa algunos fragmentos de código Python. No requiere conexión a internet.
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def cargar_detector_local():
    # Directorio del modelo = carpeta de este archivo
    base = os.path.dirname(__file__)
    print(f"📦 Cargando modelo local desde: {base}")

    tokenizer = AutoTokenizer.from_pretrained(base, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(base, local_files_only=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)

    id2label = getattr(model.config, 'id2label', {0: 'Ai_generated', 1: 'Human_written'})

    def detectar(texto: str):
        inputs = tokenizer(texto, truncation=True, padding=True, max_length=512, return_tensors='pt').to(device)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=1)[0]

        ai_prob = float(probs[0].item())
        human_prob = float(probs[1].item())
        is_ai = ai_prob >= human_prob
        confidence = max(ai_prob, human_prob)

        return {
            'is_ai_generated': is_ai,
            'confidence': confidence,
            'ai_prob': ai_prob,
            'human_prob': human_prob,
            'pred_label': id2label.get(int(probs.argmax().item()), 'Unknown'),
            'method_used': 'hf_local'
        }

    return detectar


def ejemplos_basicos():
    detectar = cargar_detector_local()

    ejemplos = [
        # Código simple humano
        """
        def suma(a, b):
            return a + b
        """,

        # Código con anotaciones y librerías científicas
        """
        from typing import List, Optional
        import numpy as np

        def process_data(data: List[float]) -> Optional[float]:
            if not data:
                return None
            return float(np.mean(data))
        """,

        # Código humano con impresión de depuración
        """
        def calcular_promedio(numeros):
            # TODO: Agregar validación de entrada
            print(f"Procesando {len(numeros)} números")
            if not numeros:
                return 0
            return sum(numeros) / len(numeros)
        """
    ]

    print("\n🧪 EJECUTANDO EJEMPLOS:")
    for i, codigo in enumerate(ejemplos, 1):
        r = detectar(codigo)
        print(f"\n📝 Ejemplo {i}:")
        print(f"   ¿Es IA?: {r['is_ai_generated']}  (pred: {r['pred_label']})")
        print(f"   Confianza: {r['confidence']:.1%}")
        print(f"   P(IA): {r['ai_prob']:.1%} | P(Humano): {r['human_prob']:.1%}")
        print(f"   Método: {r['method_used']}")


if __name__ == "__main__":
    print("🚀 EJEMPLOS DE USO - DETECTOR HF LOCAL")
    print("=" * 50)
    ejemplos_basicos()
