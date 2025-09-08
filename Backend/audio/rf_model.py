import os
import json
import joblib
import numpy as np
import librosa
import warnings
from typing import Dict, Any, List, Tuple

# Suppress warnings
warnings.filterwarnings("ignore")

class RFAudioDetector:
    def __init__(self, model_dir: str):
        """
        Inicializa el detector de audio con el modelo Random Forest.
        
        Args:
            model_dir: Directorio que contiene model_rf.joblib y manifest.json
        """
        self.model_path = os.path.join(model_dir, 'model_rf.joblib')
        self.manifest_path = os.path.join(model_dir, 'manifest.json')
        
        # Cargar el manifiesto
        with open(self.manifest_path, 'r') as f:
            self.manifest = json.load(f)
        
        # Cargar el modelo
        self.model = joblib.load(self.model_path)
        
        # Audio parameters
        self.sr = self.manifest.get('sr', 16000)
        self.win_s = self.manifest.get('win_s', 3.0)  # Window size in seconds
        self.hop_s = self.manifest.get('hop_s', 1.5)  # Hop size in seconds
        self.min_audio_length = int(self.sr * 1.0)  # Minimum 1 second of audio
        self.window_size = self.win_s  # Alias for compatibility
        self.hop_size = self.hop_s     # Alias for compatibility
        
        # Feature extraction parameters
        self.n_mfcc = 20
        self.n_fft = 1024
        self.win_length = 1024
        self.hop_length = 256
        self.n_mels = 64
        self.roll_percents = [0.85, 0.95]
        
        # Decision thresholds
        self.ia_thresh_seg = self.manifest.get('ia_thresh_seg', 0.55)
        self.ia_thresh_audio = self.manifest.get('ia_thresh_audio', 0.60)
        self.pct_segments = self.manifest.get('pct_segments', 0.20)
        
    def _spectral_flux(self, mag: np.ndarray) -> np.ndarray:
        """Compute spectral flux feature."""
        diff = np.diff(mag, axis=1)
        diff[diff < 0] = 0
        flux = np.sqrt((diff**2).sum(axis=0))
        return np.concatenate([[0.0], flux])

    def _aggregate_stats(self, x: np.ndarray) -> List[float]:
        """Compute aggregate statistics for a feature vector."""
        if x is None or len(x) == 0 or np.all(~np.isfinite(x)):
            return [np.nan] * 4
        x = x[np.isfinite(x)]
        if len(x) == 0:
            return [np.nan] * 4
        p10 = np.percentile(x, 10)
        p90 = np.percentile(x, 90)
        return [np.mean(x), np.std(x), p10, p90]

    def _extract_features(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Extract audio features matching the training pipeline.
        
        Args:
            y: Audio time series
            sr: Sample rate
            
        Returns:
            Feature vector for the audio segment
        """
        try:
            # 1) STFT (magnitude) for spectral features
            S = np.abs(librosa.stft(
                y, n_fft=self.n_fft, hop_length=self.hop_length, win_length=self.win_length))
            
            # 2) Mel-spectrogram for MFCCs
            mel = librosa.feature.melspectrogram(
                y=y, sr=sr, n_mels=self.n_mels,
                hop_length=self.hop_length, n_fft=self.n_fft)
            
            # 3) MFCCs with deltas
            mfcc = librosa.feature.mfcc(
                S=librosa.power_to_db(mel), sr=sr, n_mfcc=self.n_mfcc)
            mfcc_d = librosa.feature.delta(mfcc)
            mfcc_dd = librosa.feature.delta(mfcc, order=2)
            
            # 4) Other spectral features
            zcr = librosa.feature.zero_crossing_rate(
                y, frame_length=self.win_length, hop_length=self.hop_length, center=False)[0]
            centroid = librosa.feature.spectral_centroid(S=S, sr=sr)[0]
            flatness = librosa.feature.spectral_flatness(S=S)[0]
            rms = librosa.feature.rms(
                S=S, frame_length=self.win_length, hop_length=self.hop_length, center=False)[0]
            roll = [librosa.feature.spectral_rolloff(S=S, sr=sr, roll_percent=p)[0] 
                    for p in self.roll_percents]
            flux = self._spectral_flux(S)
            
            # 5) Aggregate features
            features = {}
            
            # MFCC features (mean and std for each coefficient)
            for name, mat in [('mfcc', mfcc), ('mfcc_d', mfcc_d), ('mfcc_dd', mfcc_dd)]:
                aggr = np.array([self._aggregate_stats(c) for c in mat])
                for i in range(aggr.shape[0]):
                    features[f"{name}_{i}_mean"] = aggr[i, 0]
                    features[f"{name}_{i}_std"] = aggr[i, 1]
            
            # Other features (mean, std, p10, p90)
            names = {
                "zcr": zcr, "centroid": centroid, 
                "flatness": flatness, "rms": rms, "flux": flux
            }
            for name, vec in names.items():
                m, s, p10, p90 = self._aggregate_stats(vec)
                features[f"{name}_mean"] = m
                features[f"{name}_std"] = s
                features[f"{name}_p10"] = p10
                features[f"{name}_p90"] = p90
            
            # Rolloff features
            for idx, r in enumerate(roll):
                m, s, p10, p90 = self._aggregate_stats(r)
                pct = int(self.roll_percents[idx] * 100)
                features[f"roll{pct}_mean"] = m
                features[f"roll{pct}_std"] = s
            
            # Convert to numpy array, handling any potential NaNs
            feature_vector = []
            for k in sorted(features.keys()):
                val = features[k]
                if np.isnan(val) or not np.isfinite(val):
                    val = 0.0  # Replace NaNs/infs with 0
                feature_vector.append(float(val))
            
            # Ensure we have at least some features
            if not feature_vector:
                return np.zeros(144)
                
            return np.array(feature_vector)
                
        except Exception as e:
            print(f"Advertencia: Error al extraer características: {str(e)}")
            return np.zeros(144)

    def process_audio(self, audio_path: str, debug: bool = False) -> Dict[str, Any]:
        """
        Procesa un archivo de audio y devuelve las predicciones más confiables.

        Args:
            audio_path: Ruta al archivo de audio
            debug: Si True imprime probabilidades por segmento

        Returns:
            Dict con el resultado final y detalle por segmento
        """
        try:
            if not os.path.exists(audio_path):
                return {
                    'result': 'error',
                    'probability': 0.5,
                    'message': f'El archivo {audio_path} no existe'
                }

            y, sr = librosa.load(audio_path, sr=self.sr, mono=True)

            if len(y) < self.min_audio_length:
                return {
                    'result': 'error',
                    'probability': 0.5,
                    'message': f'Audio demasiado corto. Mínimo {self.min_audio_length/self.sr:.1f} s requerido'
                }

            # Segmentación
            segment_length = int(self.window_size * sr)
            hop_length = int(self.hop_size * sr)

            segments = []
            for i in range(0, len(y) - segment_length + 1, hop_length):
                segments.append(y[i:i+segment_length])

            if not segments:
                # Si el audio es más corto que la ventana, usar audio completo
                segments = [y[:segment_length]]

            predictions = []

            for i, segment in enumerate(segments):
                features = self._extract_features(segment, sr)
                if len(features) == 0:
                    continue
                features = features.reshape(1, -1)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    proba = self.model.predict_proba(features)[0]

                if hasattr(self.model, 'classes_'):
                    class_idx = np.argmax(proba)
                    class_name = self.model.classes_[class_idx]
                    prob = float(proba[class_idx])
                else:
                    prob = float(proba[1] if len(proba) > 1 else proba[0])
                    class_name = 'IA' if prob >= self.ia_thresh_seg else 'REAL'

                predictions.append({
                    'class': class_name,
                    'probability': prob,
                    'segment': i+1
                })

            if not predictions:
                return {
                    'result': 'error',
                    'probability': 0.5,
                    'message': 'No se pudo realizar predicción en segmentos'
                }

            # Promedio por clase
            ia_probs = [p['probability'] for p in predictions if p['class']=='IA']
            real_probs = [p['probability'] for p in predictions if p['class']=='REAL']

            avg_ia = np.mean(ia_probs) if ia_probs else 0.0
            avg_real = np.mean(real_probs) if real_probs else 0.0

            pct_ia = len([p for p in predictions if p['class']=='IA' and p['probability']>=self.ia_thresh_seg]) / len(predictions)

            # Decisión final usando AND para reducir falsos positivos
            # Decisión final usando promedio y % de segmentos
            if avg_ia >= self.ia_thresh_audio or pct_ia >= self.pct_segments:
                result = 'IA'
                probability = avg_ia
            else:
                result = 'REAL'
                probability = 1.0 - avg_ia  # Probabilidad complementaria

            probability = max(0.0, min(1.0, probability))

            # Mostrar resumen de segmentos
            print("\n=== Análisis de Segmentos ===")
            for s in predictions:
                print(f"Segmento {s.get('segment', 'N/A')}: Prob. IA={s['probability']*100:.1f}% | Clase: {s['class']}")
            
            if debug:
                print(f"\n[DEBUG] avg_ia={avg_ia:.3f}, avg_real={avg_real:.3f}, pct_ia={pct_ia:.2f}, result={result}")

            return {
                'result': result,
                'probability': float(probability),
                'avg_ia': float(avg_ia),
                'avg_real': float(avg_real),
                'pct_ia': float(pct_ia),
                'num_segments': len(predictions),
                'segments': predictions,
                'message': 'Análisis completado',
                'model_threshold': self.ia_thresh_audio
            }

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error en process_audio: {error_details}")
            return {
                'result': 'error',
                'probability': 0.5,
                'message': f'Error al procesar el audio: {str(e)}',
                'details': error_details
            }

            

def load_rf_detector():
    """Función de conveniencia para cargar el detector RF."""
    model_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'content',
        'rf_v1'
    )
    return RFAudioDetector(model_dir)
