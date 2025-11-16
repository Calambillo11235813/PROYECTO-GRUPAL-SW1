# backend/codigo/modelos/detector_hf.py
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import os
from datetime import datetime

class CodeDetectorHF:
    def __init__(self):
        # Ruta segura a /codigo/modelo_ia/
        BASE = os.path.dirname(os.path.dirname(__file__))  # backend/codigo/
        carpeta = os.path.join(BASE, "modelo_ia")

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

        ai = float(probs[0])
        human = float(probs[1])

        return {
            "is_ai_generated": ai > human,
            "confidence": max(ai, human),
            "ai_prob": ai,
            "human_prob": human,
            "method_used": "codebert"
        }
