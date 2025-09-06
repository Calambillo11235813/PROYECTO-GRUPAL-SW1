from django.contrib import admin
from .models import AnalisisTexto, ArchivoAnalisis

@admin.register(AnalisisTexto)
class AnalisisTextoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'prediccion',
        'probabilidad_ia', 
        'probabilidad_humano',
        'confianza',
        'modelo_utilizado',
        'tipo_entrada',
        'fecha_analisis',
        'usuario'
    ]
    
    list_filter = [
        'prediccion',
        'confianza',
        'modelo_utilizado',
        'tipo_entrada',
        'fecha_analisis'
    ]
    
    search_fields = [
        'texto_original',
        'prediccion',
        'usuario__email',
        'usuario__username'
    ]
    
    readonly_fields = [
        'fecha_analisis',
        'probabilidad_ia',
        'probabilidad_humano'
    ]
    
    ordering = ['-fecha_analisis']
    
    fieldsets = (
        ('Información del Análisis', {
            'fields': ('texto_original', 'usuario', 'tipo_entrada')
        }),
        ('Resultados', {
            'fields': ('prediccion', 'probabilidad_ia', 'probabilidad_humano', 'confianza', 'modelo_utilizado')
        }),
        ('Metadatos', {
            'fields': ('fecha_analisis',),
            'classes': ('collapse',)
        })
    )

@admin.register(ArchivoAnalisis)
class ArchivoAnalisisAdmin(admin.ModelAdmin):
    # Método personalizado para mostrar nombre del archivo más amigable
    def get_filename(self, obj):
        if obj.ruta_archivo_original:
            return obj.ruta_archivo_original.split('/')[-1]
        return "Sin archivo"
    get_filename.short_description = 'Nombre Archivo'
    
    # Método para mostrar tipo de análisis relacionado
    def get_prediction(self, obj):
        return obj.analisis.prediccion
    get_prediction.short_description = 'Predicción'
    
    # UN SOLO list_display (corregido)
    list_display = [
        'id',
        'get_filename',
        'get_prediction',
        'hash_archivo',
        'fecha_subida'
    ]
    
    list_filter = ['fecha_subida']
    search_fields = ['ruta_archivo_original', 'hash_archivo']
    readonly_fields = ['fecha_subida', 'hash_archivo']
    ordering = ['-fecha_subida']
    
    fieldsets = (
        ('Análisis Asociado', {
            'fields': ('analisis',)
        }),
        ('Información del Archivo', {
            'fields': ('ruta_archivo_original', 'hash_archivo')
        }),
        ('Metadatos', {
            'fields': ('fecha_subida',),
            'classes': ('collapse',)
        })
    )
