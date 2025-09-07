# backend/audio/models.py
import os
from django.conf import settings
from django.db import models
import uuid

def ruta_archivo_audio(instance, filename):
    """Genera una ruta segura para guardar archivos de audio.
    
    Args:
        instance: La instancia del modelo AudioUpload
        filename: El nombre original del archivo
        
    Returns:
        str: Ruta segura para guardar el archivo
    """
    # Si ya hay un archivo y tiene un nombre original, usarlo
    if hasattr(instance, 'original_filename') and instance.original_filename:
        base_name = os.path.basename(instance.original_filename)
    else:
        base_name = os.path.basename(filename)
    
    # Crear un nombre de archivo seguro
    name, ext = os.path.splitext(base_name)
    safe_name = "".join(c if c.isalnum() or c in '._- ' else '_' for c in name)
    safe_name = safe_name.strip()
    
    # Si el nombre está vacío, usar un UUID
    if not safe_name:
        safe_name = f"audio_{uuid.uuid4().hex}"
    
    # Asegurar la extensión
    ext = ext.lower() or ".wav"
    if not ext.startswith('.'):
        ext = '.' + ext
    
    # Limitar la longitud del nombre
    safe_name = safe_name[:100] + ext
    
    # Guardar el nombre original si no está ya guardado
    if hasattr(instance, '_dirty') and not instance._dirty:
        instance.original_filename = base_name
        instance._dirty = True
    
    return os.path.join(settings.RUTA_SUBIDA_AUDIOS, safe_name)

def ruta_espectrograma(instance, filename):
    """Genera una ruta segura para guardar espectrogramas manteniendo el nombre original."""
    # Usar el nombre del archivo de audio original para el espectrograma
    if hasattr(instance, 'file') and instance.file:
        base_name = os.path.basename(instance.file.name)
        name = os.path.splitext(base_name)[0]
        safe_name = f"espectro_{name}.png"
    else:
        safe_name = f"espectro_{uuid.uuid4().hex}.png"
    return os.path.join(settings.RUTA_ESPECTROGRAMAS, safe_name)

class AudioUpload(models.Model):
    file = models.FileField(
        upload_to=ruta_archivo_audio,
        verbose_name="Archivo de audio",
        help_text="Sube un archivo de audio para analizar"
    )
    original_filename = models.CharField(
        max_length=255,
        verbose_name="Nombre original del archivo",
        help_text="Nombre original del archivo subido",
        blank=True,
        null=True
    )
    result = models.CharField(
        max_length=100,
        verbose_name="Resultado del análisis",
        blank=True,
        null=True
    )
    probability = models.FloatField(
        verbose_name="Probabilidad del resultado",
        null=True,
        blank=True
    )
    spectrogram = models.ImageField(
        upload_to=ruta_espectrograma,
        verbose_name="Espectrograma",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_file_name = getattr(self.file, 'name', None)

def save(self, *args, **kwargs):
    if self.file and not self.original_filename:
        # Usar el nombre del archivo que subió el usuario
        if hasattr(self.file, 'file') and hasattr(self.file.file, 'name'):
            self.original_filename = os.path.basename(self.file.file.name)
        else:
            self.original_filename = os.path.basename(self.file.name)
    super().save(*args, **kwargs)

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
        return f"{self.original_filename or self.file.name} - {self.result or 'Pendiente'}"
