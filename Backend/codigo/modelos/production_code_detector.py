import logging
import os
from .detector_hf import CodeDetectorHF

_detector = None


def get_detector():
    """Devuelve un detector de código con fallback seguro.

    - Intenta cargar CodeDetectorHF desde `codigo/modelo_ia`.
    - Si faltan pesos u ocurre un error, devuelve un detector dummy
      que nunca lanza excepciones y reporta confianza 0.
    """
    global _detector
    if _detector is None:
        # Permitir forzar el fallback vía variable de entorno
        force_fallback = os.getenv("CODE_DETECTOR_FORCE_FALLBACK", "").lower() in ("1", "true", "yes")
        if force_fallback:
            logging.getLogger(__name__).info("CODE_DETECTOR_FORCE_FALLBACK activo: usando detector dummy.")

            class _DummyDetector:
                def __init__(self):
                    self.version = "none"
                    self.timestamp = None

                def analizar(self, codigo: str):
                    return {
                        "is_ai_generated": False,
                        "confidence": 0.0,
                        "method_used": "fallback",
                        "ai_prob": None,
                        "human_prob": None,
                    }

            _detector = _DummyDetector()
            return _detector

        try:
            print("⚡ Cargando CodeDetectorHF (CodeBERT)...")
            _detector = CodeDetectorHF()
        except Exception as e:
            logging.getLogger(__name__).warning(
                "No se pudo cargar CodeDetectorHF, usando fallback. Error: %s", e
            )

            class _DummyDetector:
                def __init__(self):
                    self.version = "none"
                    self.timestamp = None

                def analizar(self, codigo: str):
                    return {
                        "is_ai_generated": False,
                        "confidence": 0.0,
                        "method_used": "fallback",
                        "ai_prob": None,
                        "human_prob": None,
                    }

            _detector = _DummyDetector()

    return _detector
