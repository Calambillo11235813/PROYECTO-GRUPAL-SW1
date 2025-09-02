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

def generar_espectrograma(path_audio, filename):
    y, sr = librosa.load(path_audio, sr=None)
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_DB = librosa.power_to_db(S, ref=1.0) 


    fig, ax = plt.subplots(figsize=(12, 2), dpi=120)
    
    # Configurar el espectrograma
    img = librosa.display.specshow(S_DB, sr=sr, x_axis='time', y_axis='mel', 
                                 fmax=8000, ax=ax)
    
    # Añadir barra de color
    plt.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set_title(f'Espectrograma: {os.path.basename(path_audio)}')
    plt.tight_layout()

    output_dir = os.path.join(settings.MEDIA_ROOT, "plots")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{filename}.png")

    plt.savefig(output_path)
    plt.close()

   
    return f"plots/{filename}.png"
