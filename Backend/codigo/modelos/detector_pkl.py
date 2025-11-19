import os
import logging
from datetime import datetime

try:
    import joblib
except Exception:  # pragma: no cover
    joblib = None


class CodeDetectorPKL:
    """
    Carga un detector de código desde un archivo .pkl (joblib).

    Requisitos mínimos del objeto cargado:
    - Método `detect(texto: str)` que devuelva un dict con llaves:
      { 'is_ai_generated': bool, 'confidence': float, 'method_used': str }

    En caso de formatos distintos, intentamos adaptarlo de forma robusta.
    """

    def __init__(self, pkl_path: str):
        if joblib is None:
            raise RuntimeError("joblib no está instalado. Instala 'joblib' para usar CodeDetectorPKL.")

        if not os.path.isfile(pkl_path):
            raise FileNotFoundError(f"No se encontró el archivo PKL en: {pkl_path}")

        self.pkl_path = pkl_path
        
        # Intentar cargar con torch en CPU si está disponible
        try:
            import torch
            # Configurar torch para cargar en CPU
            torch.serialization.add_safe_globals([type(None)])
            self.detector = joblib.load(pkl_path, map_location=torch.device('cpu'))
            logging.getLogger(__name__).info(f"✓ Modelo PKL cargado exitosamente desde: {pkl_path}")
        except Exception as e:
            logging.getLogger(__name__).warning(f"Intento 1 falló: {e}")
            
            # Intentar con pickle directamente con map_location
            try:
                import pickle
                import torch
                
                with open(pkl_path, 'rb') as f:
                    self.detector = pickle.load(f, map_location=torch.device('cpu'))
                logging.getLogger(__name__).info(f"✓ Modelo PKL cargado con pickle + CPU map")
            except Exception as e2:
                logging.getLogger(__name__).warning(f"Intento 2 falló: {e2}")
                
                # Intentar con contexto personalizado y torch CPU
                try:
                    import sys
                    import types
                    import torch
                    
                    # Monkey patch para torch.load
                    original_torch_load = torch.load
                    def custom_torch_load(*args, **kwargs):
                        kwargs['map_location'] = torch.device('cpu')
                        return original_torch_load(*args, **kwargs)
                    
                    torch.load = custom_torch_load
                    
                    try:
                        self.detector = joblib.load(pkl_path)
                        logging.getLogger(__name__).info(f"✓ Modelo PKL cargado con monkey patch")
                    finally:
                        torch.load = original_torch_load
                        
                except Exception as e3:
                    raise RuntimeError(f"No se pudo cargar el detector PKL después de múltiples intentos: {e3}")
        
        self.version = f"pkl:{os.path.basename(pkl_path)}"
        self.timestamp = datetime.now().isoformat()

    def analizar(self, texto: str):
        try:
            # Caso ideal: el objeto tiene `detect` y devuelve un dict esperado
            if hasattr(self.detector, 'detect'):
                out = self.detector.detect(texto)
                if isinstance(out, dict) and 'is_ai_generated' in out and 'confidence' in out:
                    # Aseguramos llaves estándar
                    out.setdefault('method_used', 'pkl')
                    out.setdefault('ai_prob', None)
                    out.setdefault('human_prob', None)
                    return out

            # Si tiene `predict_proba` estilo sklearn
            if hasattr(self.detector, 'predict_proba'):
                import numpy as np  # local import para evitar dependencia si no se usa
                probs = self.detector.predict_proba([texto])[0]
                # Asumimos convención [P(IA), P(Humano)] si existen 2 clases
                ai_prob = float(probs[0]) if len(probs) > 0 else 0.0
                human_prob = float(probs[1]) if len(probs) > 1 else (1.0 - ai_prob)
                is_ai = ai_prob >= human_prob
                confidence = max(ai_prob, human_prob)
                return {
                    'is_ai_generated': is_ai,
                    'confidence': confidence,
                    'ai_prob': ai_prob,
                    'human_prob': human_prob,
                    'method_used': 'pkl_proba'
                }

            # Si solo tiene `predict`
            if hasattr(self.detector, 'predict'):
                pred = self.detector.predict([texto])[0]
                # Intentamos mapear a booleano IA
                if isinstance(pred, (int, float)):
                    is_ai = bool(pred)
                elif isinstance(pred, str):
                    is_ai = pred.lower() in ('ai', 'ai_generated', 'ia', 'true', '1')
                else:
                    is_ai = False
                return {
                    'is_ai_generated': is_ai,
                    'confidence': 1.0 if is_ai else 0.0,
                    'ai_prob': None,
                    'human_prob': None,
                    'method_used': 'pkl_predict'
                }

        except Exception as e:
            logging.getLogger(__name__).warning("Fallo analizando con PKL: %s", e)

        # Fallback seguro
        return {
            'is_ai_generated': False,
            'confidence': 0.0,
            'ai_prob': None,
            'human_prob': None,
            'method_used': 'pkl_fallback'
        }
