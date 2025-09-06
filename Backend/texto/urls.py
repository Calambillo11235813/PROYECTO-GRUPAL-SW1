from django.urls import path
from . import views

urlpatterns = [
    path('analizar/', views.analizar_texto, name='analizar_texto'),
    path('estado/', views.estado_servicio, name='estado_servicio'),
    # Nuevas rutas para manejo de modelos
    path('comparar/', views.comparar_modelos, name='comparar_modelos'),
    path('analizar-con-modelo/', views.analizar_texto_con_modelo, name='analizar_texto_con_modelo'),
    path('info-modelos/', views.info_modelos, name='info_modelos'),
    # Nuevas URLs para archivos
    path('analizar-archivo/', views.analizar_archivo, name='analizar_archivo'),
    path('comparar-archivo/', views.comparar_modelos_archivo, name='comparar_modelos_archivo'),
]