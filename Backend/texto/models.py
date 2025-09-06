from django.db import models
from django.utils import timezone

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
    
    # Campos existentes
    texto = models.TextField(verbose_name="Texto analizado")
    resultado_prediccion = models.CharField(
        max_length=10, 
        choices=ORIGEN_CHOICES,
        verbose_name="Resultado de predicción"
    )
    probabilidad_ia = models.FloatField(verbose_name="Probabilidad IA (%)")
    probabilidad_humano = models.FloatField(verbose_name="Probabilidad Humano (%)")
    fecha_analisis = models.DateTimeField(default=timezone.now, verbose_name="Fecha de análisis")
    usuario = models.ForeignKey(
        'usuario.Usuario', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Usuario que realizó el análisis"
    )
    
    # Nuevos campos para archivos
    tipo_entrada = models.CharField(
        max_length=10, 
        choices=TIPO_ENTRADA_CHOICES, 
        default='TEXTO',
        verbose_name="Tipo de entrada"
    )
    nombre_archivo = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Nombre del archivo"
    )
    tamano_archivo = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name="Tamaño del archivo (en bytes)"
    )  
    tipo_archivo = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        verbose_name="Tipo de archivo"
    )  
    
    class Meta:
        db_table = 'analisis_texto'
        verbose_name = 'Análisis de Texto'
        verbose_name_plural = 'Análisis de Textos'
        ordering = ['-fecha_analisis']
    
    def __str__(self):
        if self.tipo_entrada == 'ARCHIVO':
            return f"Análisis de {self.nombre_archivo} - {self.resultado_prediccion}"
        return f"Análisis de texto - {self.resultado_prediccion}"

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
