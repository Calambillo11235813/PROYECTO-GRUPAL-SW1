from django.db import models
from django.utils import timezone

class AnalisisTexto(models.Model):
    """Modelo para almacenar los análisis de texto realizados."""
    
    ORIGEN_CHOICES = [
        ('IA', 'Inteligencia Artificial'),
        ('HUMANO', 'Humano'),
    ]
    
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
    
    class Meta:
        verbose_name = "Análisis de texto"
        verbose_name_plural = "Análisis de textos"
        ordering = ['-fecha_analisis']
    
    def __str__(self):
        return f"Análisis #{self.id} - {self.resultado_prediccion} ({self.fecha_analisis.strftime('%d/%m/%Y')})"
