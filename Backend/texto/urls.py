from django.urls import path
from . import views

urlpatterns = [
    # Análisis de texto directo
    path('analizar/', views.analizar_texto, name='analizar_texto'),
    
    # Estado del servicio
    path('estado/', views.estado_servicio, name='estado_servicio'),
    
    # Comparación de modelos
    path('comparar/', views.comparar_modelos, name='comparar_modelos'),
    
    # Análisis de archivos
    path('analizar-archivo/', views.analizar_archivo, name='analizar_archivo'),
    
    # Comparación de modelos con archivo
    path('comparar-archivo/', views.comparar_modelos_archivo, name='comparar_modelos_archivo'),
    
    # Información de modelos disponibles
    path('info-modelos/', views.info_modelos, name='info_modelos'),
]