# backend/audio/models.py
from django.db import models

class AudioUpload(models.Model):
    file = models.FileField(upload_to="audios/")
    result = models.CharField(max_length=20, blank=True, null=True)  # "real" o "fake"
    probability = models.FloatField(blank=True, null=True)
    
    spectrogram = models.ImageField(upload_to="plots/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)