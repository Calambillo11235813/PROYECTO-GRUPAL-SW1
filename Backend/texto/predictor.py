import torch
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
import os
import logging
import json

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextoPredictor:
    """Clase para predecir si un texto fue generado por IA o escrito por un humano."""
    
    MODELS = {
        'N': 'modelo_deteccion_ia_N',  # Modelo experimental
        'B': 'modelo_deteccion_ia_B'   # Modelo Principal 
    }
    
    # CAMBIO: Modelo por defecto es ahora 'B'
    def __init__(self, model_type='B'):  # Cambiar de 'N' a 'B'
        """
        Inicializa el predictor cargando el modelo y el tokenizador.
        
        Args:
            model_type (str): 'B' para modelo principal, 'N' para experimental
        """
        self.model_type = model_type
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.max_length = 512  # Longitud máxima de secuencia para BERT
        
        # Determinar la ruta absoluta al modelo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_folder = self.MODELS.get(model_type)
        
        if not model_folder:
            raise ValueError(f"Tipo de modelo '{model_type}' no válido. Use 'N' o 'B'")
            
        self.model_path = os.path.join(current_dir, model_folder)
        
        # Cargar tokenizador y modelo
        logger.info(f"Cargando modelo {model_type} desde: {self.model_path}")
        self.tokenizer = None
        self.model = None
        self._load_model()
        
    def _load_model(self):
        """Carga el modelo y tokenizador desde los archivos guardados."""
        try:
            # Verificar que el directorio del modelo existe
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"El directorio del modelo no existe: {self.model_path}")
            
            # Verificar archivos requeridos
            config_path = os.path.join(self.model_path, 'config.json')
            model_path = os.path.join(self.model_path, 'model.safetensors')
            
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"config.json no encontrado en {self.model_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"model.safetensors no encontrado en {self.model_path}")
            
            # Leer config.json para determinar el modelo base
            model_config = {}
            with open(config_path, 'r') as f:
                model_config = json.load(f)
            
            base_model_name = model_config.get('_name_or_path', 'bert-base-uncased')
            model_type_config = model_config.get('model_type', 'bert')
            vocab_size = model_config.get('vocab_size', 30522)
            
            logger.info(f"Modelo {self.model_type} - Base: {base_model_name}, Vocab: {vocab_size}")
            
            # Variables para controlar el éxito de la carga
            tokenizer_loaded = False
            model_loaded = False
            
            # Método 1: Intentar cargar tokenizer local
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
                tokenizer_loaded = True
                logger.info(f"Tokenizer local cargado para modelo {self.model_type}")
            except Exception as e1:
                logger.warning(f"No se pudo cargar tokenizer local: {e1}")
                
                # Método 2: Usar tokenizer del modelo base original
                try:
                    logger.info(f"Cargando tokenizer desde modelo base: {base_model_name}")
                    self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
                    tokenizer_loaded = True
                    logger.info(f"Tokenizer del modelo base cargado para modelo {self.model_type}")
                except Exception as e2:
                    logger.warning(f"Error con modelo base, usando fallback: {e2}")
                    
                    # Método 3: Fallback inteligente basado en vocab_size
                    if vocab_size > 100000:
                        fallback_model = 'bert-base-multilingual-cased'
                    elif vocab_size > 50000:
                        fallback_model = 'bert-base-multilingual-uncased'
                    else:
                        fallback_model = 'bert-base-uncased'
                    
                    try:
                        logger.info(f"Usando tokenizer fallback inteligente: {fallback_model}")
                        self.tokenizer = AutoTokenizer.from_pretrained(fallback_model)
                        tokenizer_loaded = True
                        logger.info(f"Tokenizer fallback cargado para modelo {self.model_type}")
                    except Exception as e3:
                        logger.error(f"Error con tokenizer fallback: {e3}")
            
            # Intentar cargar el modelo
            try:
                self.model = BertForSequenceClassification.from_pretrained(self.model_path)
                model_loaded = True
                logger.info(f"Modelo BERT cargado para modelo {self.model_type}")
            except Exception as e3:
                logger.warning(f"No se pudo cargar modelo como BERT: {e3}")
                
                try:
                    self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
                    model_loaded = True
                    logger.info(f"Modelo Auto cargado para modelo {self.model_type}")
                except Exception as e4:
                    logger.error(f"No se pudo cargar modelo como Auto: {e4}")
            
            # Si no se cargó el tokenizer, usar uno por defecto
            if not tokenizer_loaded:
                logger.warning(f"Usando tokenizer BERT por defecto para modelo {self.model_type}")
                try:
                    self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
                    tokenizer_loaded = True
                except Exception as e5:
                    logger.error(f"No se pudo cargar tokenizer por defecto: {e5}")
            
            # Verificar que al menos el modelo se cargó
            if not model_loaded:
                raise RuntimeError(f"No se pudo cargar el modelo {self.model_type}")
            
            # Verificar que el tokenizer se cargó
            if not tokenizer_loaded:
                raise RuntimeError(f"No se pudo cargar el tokenizer para modelo {self.model_type}")
            
            self.model.to(self.device)
            self.model.eval()  # Poner el modelo en modo evaluación
            logger.info(f"Modelo {self.model_type} cargado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al cargar el modelo {self.model_type}: {str(e)}")
            raise RuntimeError(f"No se pudo cargar el modelo {self.model_type}: {str(e)}")
    
    def get_model_info(self):
        """Retorna información sobre el modelo actual."""
        try:
            model_loaded = self.model is not None
            tokenizer_loaded = self.tokenizer is not None
            model_files = os.listdir(self.model_path) if os.path.exists(self.model_path) else []
            
            # Verificar archivos específicos del tokenizer
            tokenizer_files = []
            for file in ['tokenizer.json', 'vocab.txt', 'special_tokens_map.json']:
                if file in model_files:
                    tokenizer_files.append(file)
            
            return {
                'tipo': self.model_type,
                'nombre': self.MODELS[self.model_type],
                'dispositivo': str(self.device),
                'max_length': self.max_length,
                'modelo_cargado': model_loaded,
                'tokenizer_cargado': tokenizer_loaded,
                'archivos_disponibles': model_files,
                'archivos_tokenizer': tokenizer_files,
                'ruta': self.model_path,
                'estado': 'Funcional' if (model_loaded and tokenizer_loaded) else 'Con errores'
            }
        except Exception as e:
            return {
                'tipo': self.model_type,
                'error': str(e),
                'modelo_cargado': False,
                'tokenizer_cargado': False,
                'estado': 'Error'
            }
    
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
        
        if self.model is None or self.tokenizer is None:
            return {'error': f'Modelo {self.model_type} no está cargado correctamente'}
        
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
                'confianza': round(max(probability, probability_human) * 100, 2),
                'modelo_usado': self.model_type
            }
            
        except Exception as e:
            logger.error(f"Error durante la predicción con modelo {self.model_type}: {str(e)}")
            return {'error': f'Error al procesar el texto: {str(e)}'}

# Instancias globales para reutilización
predictors = {}

def get_predictor(model_type='B'):  # Cambiar de 'N' a 'B'
    """
    Obtiene o crea una instancia del predictor.
    
    Args:
        model_type (str): 'B' para modelo principal, 'N' para experimental
        
    Returns:
        TextoPredictor: Instancia del predictor o None si falla
    """
    global predictors
    if model_type not in predictors:
        try:
            predictors[model_type] = TextoPredictor(model_type)
        except Exception as e:
            logger.error(f"No se pudo crear predictor {model_type}: {e}")
            predictors[model_type] = None
    return predictors[model_type]

def get_available_models():
    """Retorna lista de modelos disponibles."""
    return list(TextoPredictor.MODELS.keys())