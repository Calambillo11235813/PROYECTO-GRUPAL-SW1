from django.urls import path
from . import views

urlpatterns = [
    path('analizar/', views.analizar_texto, name='analizar_texto'),
    path('estado/', views.estado_servicio, name='estado_servicio'),
]