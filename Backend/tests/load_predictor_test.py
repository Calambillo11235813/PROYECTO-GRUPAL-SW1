import logging, traceback
logging.basicConfig(level=logging.INFO)
from texto.predictor import TextoPredictor
try:
    TextoPredictor('B')
    print('MODEL_LOADED_OK')
except Exception:
    traceback.print_exc()
    print('MODEL_LOAD_FAILED')
