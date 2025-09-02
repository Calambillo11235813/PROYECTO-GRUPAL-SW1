# backend/audio/models.py
import os
from django.conf import settings
from django.db import models
import uuid

def ruta_archivo_audio(instance, filename):
    """Genera una ruta segura para guardar archivos de audio."""
    extension = os.path.splitext(filename)[1].lower()
    nombre_archivo = f"{uuid.uuid4().hex}{extension}"
    return os.path.join(settings.RUTA_SUBIDA_AUDIOS, nombre_archivo)

def ruta_espectrograma(instance, filename):
    """Genera una ruta segura para guardar espectrogramas."""
    extension = os.path.splitext(filename)[1].lower()
    nombre_archivo = f"espectro_{uuid.uuid4().hex}{extension}"
    return os.path.join(settings.RUTA_ESPECTROGRAMAS, nombre_archivo)

class AudioUpload(models.Model):
    file = models.FileField(
        upload_to=ruta_archivo_audio,
        verbose_name="Archivo de audio",
        help_text="Sube un archivo de audio para analizar"
    )
    original_filename = models.CharField(
        max_length=255,
        verbose_name="Nombre original del archivo",
        help_text="Nombre original del archivo subido"
    )
    result = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Resultado",
        help_text="Indica si el audio es 'real' o 'fake'"
    )
    probability = models.FloatField(
        blank=True, 
        null=True,
        verbose_name="Probabilidad",
        help_text="Nivel de confianza del resultado"
    )
    spectrogram = models.ImageField(
        upload_to=ruta_espectrograma, 
        null=True, 
        blank=True,
        verbose_name="Espectrograma",
        help_text="Imagen del espectrograma generado"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de subida"
    )

    class Meta:
        verbose_name = "Audio subido"
        verbose_name_plural = "Audios subidos"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file.name} - {self.result or 'Pendiente'}"