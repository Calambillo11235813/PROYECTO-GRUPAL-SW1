# backend/audio/utils.py
import librosa
import librosa.display
import matplotlib
# Usar el backend 'Agg' que no requiere GUI
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings

def generar_espectrograma(path_audio, file_id, original_filename=None):
    """
    Genera un espectrograma a partir de un archivo de audio.
    
    Args:
        path_audio (str): Ruta al archivo de audio
        file_id (str): ID único para el archivo de salida
        original_filename (str, optional): Nombre original del archivo para mostrar en el título
    """
    try:
        y, sr = librosa.load(path_audio, sr=None)
    except Exception as e:
        # Si librosa falla (ej: falta ffmpeg), intentar con soundfile como fallback
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"librosa.load falló: {e}. Intentando con soundfile...")
        
        try:
            import soundfile as sf
            y, sr = sf.read(path_audio)
        except Exception as sf_error:
            logger.error(f"soundfile también falló: {sf_error}")
            # Si ambos fallan, retornar None para que el análisis continúe sin espectrograma
            logger.error("No se pudo generar espectrograma. Instala ffmpeg para soporte completo de formatos.")
            return None
    
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_DB = librosa.power_to_db(S, ref=1.0)

    fig, ax = plt.subplots(figsize=(12, 2), dpi=120)
    
    # Configurar el espectrograma
    img = librosa.display.specshow(S_DB, sr=sr, x_axis='time', y_axis='mel', 
                                 fmax=8000, ax=ax)
    
    # Añadir barra de color
    plt.colorbar(img, ax=ax, format='%+2.0f dB')
    
    # Usar el nombre original del archivo en el título si está disponible
    display_name = original_filename if original_filename else os.path.basename(path_audio)
    ax.set_title(f'Espectrograma: {display_name}')
    plt.tight_layout()

    output_dir = os.path.join(settings.MEDIA_ROOT, "plots")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{file_id}.png")

    plt.savefig(output_path)
    plt.close()

   
    return f"plots/{file_id}.png"
