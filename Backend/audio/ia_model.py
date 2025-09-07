import os
from .rf_model import load_rf_detector

# Cargar el modelo personalizado de Random Forest
rf_detector = load_rf_detector()

def verificar_autenticidad(path_audio):
    """
    Analiza un archivo de audio para determinar si es real o sintético
    utilizando un modelo personalizado de Random Forest.
    
    Args:
        path_audio (str): Ruta al archivo de audio a analizar
        
    Returns:
        tuple: (resultado, probabilidad) donde:
            - resultado: 'real', 'fake' o 'error'
            - probabilidad: float entre 0 y 1 que indica la confianza
    """
    try:
        # Procesar el audio con el detector RF
        result = rf_detector.process_audio(path_audio)
        
        # Si hubo un error, devolver el mensaje
        if result['result'] == 'error':
            print(f"Error: {result.get('message', 'Error desconocido')}")
            return "error", 0.5
        
        # Devolver el resultado y la probabilidad
        return result['result'], result['probability']
        
    except Exception as e:
        print(f"Error al procesar el audio: {str(e)}")
        return "error", 0.5
