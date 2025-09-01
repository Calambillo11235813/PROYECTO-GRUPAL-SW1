# backend/audio/utils.py
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings

def generar_espectrograma(path_audio, filename):
    y, sr = librosa.load(path_audio, sr=None)
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_DB = librosa.power_to_db(S, ref=1.0) 


    plt.figure(figsize=(12, 2), dpi=120)

    librosa.display.specshow(S_DB, sr=sr, x_axis='time', y_axis='mel', fmax=8000)


    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Espectrograma: {os.path.basename(path_audio)}')

    plt.tight_layout()

    output_dir = os.path.join(settings.MEDIA_ROOT, "plots")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{filename}.png")

    plt.savefig(output_path)
    plt.close()

   
    return f"plots/{filename}.png"
