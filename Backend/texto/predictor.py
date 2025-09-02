import torch
from transformers import BertTokenizer, BertForSequenceClassification
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextoPredictor:
    """Clase para predecir si un texto fue generado por IA o escrito por un humano."""
    
    def __init__(self):
        """Inicializa el predictor cargando el modelo y el tokenizador."""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.max_length = 512  # Longitud máxima de secuencia para BERT
        
        # Determinar la ruta absoluta al modelo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(current_dir, 'modelo_deteccion_ia')
        
        # Cargar tokenizador y modelo
        logger.info(f"Cargando modelo desde: {self.model_path}")
        self.tokenizer = None
        self.model = None
        self._load_model()
        
    def _load_model(self):
        """Carga el modelo y tokenizador desde los archivos guardados."""
        try:
            self.tokenizer = BertTokenizer.from_pretrained(self.model_path)
            self.model = BertForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()  # Poner el modelo en modo evaluación
            logger.info("Modelo cargado exitosamente")
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {str(e)}")
            raise RuntimeError(f"No se pudo cargar el modelo: {str(e)}")
    
    def predict(self, text):
        """
        Predice si un texto fue generado por IA o por un humano.
        
        Args:
            text (str): Texto a clasificar
            
        Returns:
            dict: Diccionario con la predicción y probabilidad
        """
        if not text or not isinstance(text, str):
            return {'error': 'El texto está vacío o no es válido'}
        
        try:
            # Preprocesar texto y convertirlo a tokens
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length,
                padding="max_length"
            )
            
            # Mover inputs al dispositivo (CPU/GPU)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Realizar predicción
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                probability = probabilities[0][predicted_class].item()
            
            # Preparar respuesta
            if predicted_class == 1:  # Asumiendo que 1 = IA, 0 = Humano
                prediction = "IA"
                probability_human = 1 - probability
            else:
                prediction = "Humano"
                probability_human = probability
                probability = 1 - probability_human
            
            return {
                'prediccion': prediction,
                'probabilidad_ia': round(probability * 100, 2),
                'probabilidad_humano': round(probability_human * 100, 2),
                'confianza': round(max(probability, probability_human) * 100, 2)
            }
            
        except Exception as e:
            logger.error(f"Error durante la predicción: {str(e)}")
            return {'error': f'Error al procesar el texto: {str(e)}'}

# Instancia global para reutilización
predictor = None

def get_predictor():
    """Obtiene o crea una instancia del predictor."""
    global predictor
    if predictor is None:
        predictor = TextoPredictor()
    return predictor