# Backend/codigo/views/panel_view.py
from django.shortcuts import render

def panel_inicio(request):
    return render(request, 'panel.html')
