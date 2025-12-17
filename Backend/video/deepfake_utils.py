import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from mtcnn import MTCNN

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'Model_deepfake', 'modelo_deepfake_final_corregido.h5')

class DeepfakeDetector:
    _instance = None
    _model = None
    _detector = None

    def __new__(cls):
        """Singleton: una sola instancia del detector con modelo y MTCNN cacheados"""
        if cls._instance is None:
            cls._instance = super(DeepfakeDetector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Solo cargar el modelo y detector una vez
        if DeepfakeDetector._model is None:
            print("[DeepfakeDetector] Cargando modelo por primera vez...")
            DeepfakeDetector._model = load_model(MODEL_PATH)
            DeepfakeDetector._detector = MTCNN()
            print("[DeepfakeDetector] Modelo y detector cargados.")
        self.model = DeepfakeDetector._model
        self.detector = DeepfakeDetector._detector

    def extract_faces(self, video_path, max_frames=16):
        """Extrae caras del video. Reducido a 16 frames para optimizar velocidad."""
        faces = []
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_idxs = np.linspace(0, total_frames - 1, min(max_frames, total_frames)).astype(int)
        
        for idx in frame_idxs:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if not ret:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detections = self.detector.detect_faces(rgb)
            if detections:
                x, y, w, h = detections[0]['box']
                # Ajustar coordenadas para evitar valores negativos
                x, y = max(0, x), max(0, y)
                face = rgb[y:y+h, x:x+w]
                if face.size > 0:  # Verificar que la cara sea válida
                    face = cv2.resize(face, (224, 224))
                    faces.append(face)
        cap.release()
        return np.array(faces)

    def predict(self, video_path):
        faces = self.extract_faces(video_path)
        if len(faces) == 0:
            return 0.0, 'NO_FACE'
        
        # Normalizar
        faces = faces.astype('float32') / 255.0
        
        # Predicción en batch (más eficiente que frame a frame)
        preds = self.model.predict(faces, batch_size=8, verbose=0)
        
        score = float(np.mean(preds))
        verdict = 'DEEPFAKE' if score >= 0.5 else 'REAL'
        return score, verdict
