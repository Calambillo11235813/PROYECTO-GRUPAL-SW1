from django.db import models
from django.conf import settings

# Create your models here.

class AnalisisCodigo(models.Model):
    """
    Registro completo de un análisis de código.
    Cumple HU-013, HU-014, HU-015, HU-018 y HU-019.
    """

    # ==========================
    # Información del archivo
    # ==========================
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    archivo = models.FileField(upload_to='codigo/')
    nombre_archivo = models.CharField(max_length=255)
    lenguaje = models.CharField(max_length=50, null=True, blank=True)

    # ==========================
    # Resultado del modelo IA
    # ==========================
    ia_es_generado = models.BooleanField(default=False)
    ia_confianza = models.FloatField(default=0.0)
    ia_metodo = models.CharField(max_length=100, null=True, blank=True)
    ia_detalles = models.JSONField(null=True, blank=True)  # Score, heurísticas, etc

    # ==========================
    # Patrón sintáctico (HU-014)
    # ==========================
    ast_json = models.JSONField(null=True, blank=True)
    complejidad_ciclomatica = models.FloatField(default=0)
    variabilidad_funciones = models.FloatField(default=0)
    patrones_control = models.JSONField(null=True, blank=True)
    patrones_comunes = models.JSONField(null=True, blank=True)
    idiosincrasias = models.JSONField(null=True, blank=True)
    indice_predictibilidad = models.FloatField(default=0)

    # ==========================
    # HU-015 – líneas sospechosas
    # ==========================
    lineas_sospechosas = models.JSONField(null=True, blank=True)
    bloques_sospechosos = models.JSONField(null=True, blank=True)

    # ==========================
    # Reportes (HU-018)
    # ==========================
    reporte_pdf = models.FileField(upload_to='reportes/', null=True, blank=True)
    reporte_json = models.JSONField(null=True, blank=True)
    version_modelo = models.CharField(max_length=50, null=True, blank=True)
    timestamp_modelo = models.DateTimeField(null=True, blank=True)

    # ==========================
    # Metadatos – Historial (HU-019)
    # ==========================
    fecha_analisis = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_analisis']

    def __str__(self):
        return f"{self.nombre_archivo} ({self.fecha_analisis.date()})"
