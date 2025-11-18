from .detector_hf import CodeDetectorHF

_detector = None

def get_detector():
    global _detector
    if _detector is None:
        print("⚡ Cargando CodeDetectorHF (CodeBERT)...")
        _detector = CodeDetectorHF()
    return _detector
