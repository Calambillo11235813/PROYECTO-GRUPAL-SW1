#backend/audio/ia_model.py
import torchaudio
from speechbrain.pretrained import SpeakerRecognition

# backend/audio/ia_model.py
import random

def verificar_autenticidad(path_audio):
    """
    Dummy detector temporal:
    Devuelve 'real' o 'fake' con una probabilidad aleatoria.
    """
    prob_fake = random.random()
    if prob_fake > 0.5:
        return "fake", prob_fake
    else:
        return "real", 1 - prob_fake



#codigo ismael
# #backen
# import torchaudio
# from speechbrain.pretrained import SpeakerRecognition

# # Cargar modelo anti-spoofing (una sola vez)
# model = SpeakerRecognition.from_hparams(
#     source="speechbrain/anti-spoofing",
#     savedir="pretrained_model"
# )

# def verificar_autenticidad(path_audio):
#     signal, fs = torchaudio.load(path_audio)
#     score = model.classify_batch(signal)

#     # score es un tensor con [prob_real, prob_fake]
#     prob_real = float(score[0][0])
#     prob_fake = float(score[0][1])

#     if prob_real > prob_fake:
#         return "real", prob_real
#     else:
#         return "fake", prob_fake
