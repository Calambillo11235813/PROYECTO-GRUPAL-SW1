import logging
import os
from .detector_pkl import CodeDetectorPKL
from .detector_hf import CodeDetectorHF

_detector = None


def get_detector():
    """Devuelve un detector de código con fallback seguro.

    Modo de selección (por prioridad):
    1) Si CODE_DETECTOR_FORCE_FALLBACK=1 -> dummy
    2) Si CODE_DETECTOR_IMPL=pkl -> PKL (joblib)
    3) Si CODE_DETECTOR_IMPL=hf -> HuggingFace (HF)
    4) auto -> intenta PKL si existe, si no HF, si no dummy

    Rutas por defecto:
    - PKL: CODE_PKL_PATH o `codigo/code_detection-model-complete/production_detector.pkl`
           (alterno: `codigo/modelo_ia/production_detector.pkl`)
    - HF:  CODE_HF_PATH o `codigo/modelo_ia`
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

        impl = (os.getenv("CODE_DETECTOR_IMPL", "auto").lower()).strip()

        def make_dummy():
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

            return _DummyDetector()

        def try_pkl():
            pkl_path = os.getenv("CODE_PKL_PATH")
            if not pkl_path:
                # rutas por defecto
                base = os.path.dirname(os.path.dirname(__file__))  # backend/codigo/
                cand1 = os.path.join(base, "code_detection-model-complete", "production_detector.pkl")
                cand2 = os.path.join(base, "modelo_ia", "production_detector.pkl")
                pkl_path = cand1 if os.path.isfile(cand1) else cand2
            if os.path.isfile(pkl_path):
                print(f"⚡ Cargando CodeDetectorPKL desde: {pkl_path}")
                return CodeDetectorPKL(pkl_path)
            raise FileNotFoundError(f"No se encontró PKL en {pkl_path}")

        def try_hf():
            print("⚡ Cargando CodeDetectorHF (Transformers)...")
            # detector_hf usa por defecto codigo/code_detection-model-complete
            return CodeDetectorHF()

        # Resolución por configuración
        if impl == "pkl":
            try:
                _detector = try_pkl()
            except Exception as e:
                logging.getLogger(__name__).warning("PKL no disponible: %s", e)
                _detector = make_dummy()
        elif impl == "hf":
            try:
                _detector = try_hf()
            except Exception as e:
                logging.getLogger(__name__).warning("HF no disponible: %s", e)
                _detector = make_dummy()
        else:  # auto
            # Intentar HF primero (más estable que PKL)
            try:
                _detector = try_hf()
            except Exception as e:
                logging.getLogger(__name__).info("HF no encontrado/usable: %s. Intentando PKL...", e)
                try:
                    _detector = try_pkl()
                except Exception as e2:
                    logging.getLogger(__name__).warning("PKL no disponible: %s. Usando dummy.", e2)
                    _detector = make_dummy()

    return _detector
