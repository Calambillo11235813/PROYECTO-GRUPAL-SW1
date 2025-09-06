from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()  # ← Esto apuntará a CustomUser

class AnalisisTexto(models.Model):
    """Modelo para almacenar los análisis de texto realizados."""
    
    ORIGEN_CHOICES = [
        ('IA', 'Generado por IA'),
        ('HUMANO', 'Escrito por Humano'),
    ]
    
    TIPO_ENTRADA_CHOICES = [
        ('TEXTO', 'Texto directo'),
        ('ARCHIVO', 'Archivo subido'),
    ]
    
    # Campos existentes...
    texto_original = models.TextField()
    prediccion = models.CharField(max_length=10, choices=ORIGEN_CHOICES)  # ← Este campo existe
    probabilidad_ia = models.FloatField()
    probabilidad_humano = models.FloatField()
    confianza = models.CharField(max_length=10)
    modelo_utilizado = models.CharField(max_length=50)
    tipo_entrada = models.CharField(max_length=10, choices=TIPO_ENTRADA_CHOICES, default='TEXTO')
    fecha_analisis = models.DateTimeField(default=timezone.now)
    
    # NUEVO: Asociar con usuario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_analisis']
        verbose_name = 'Análisis de Texto'
        verbose_name_plural = 'Análisis de Textos'
    
    def __str__(self):
        return f"Análisis {self.id} - {self.prediccion} ({self.fecha_analisis})"

class ArchivoAnalisis(models.Model):
    """Modelo para almacenar metadatos de archivos analizados"""
    analisis = models.OneToOneField(AnalisisTexto, on_delete=models.CASCADE, related_name='archivo_info')
    ruta_archivo_original = models.CharField(max_length=500, blank=True, null=True)
    hash_archivo = models.CharField(max_length=64, blank=True, null=True)  # SHA256
    fecha_subida = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'archivo_analisis'
        verbose_name = 'Archivo de Análisis'
        verbose_name_plural = 'Archivos de Análisis'
