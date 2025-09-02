from django.contrib import admin
from .models import AnalisisTexto

class AnalisisTextoAdmin(admin.ModelAdmin):
    list_display = ('id', 'resultado_prediccion', 'probabilidad_ia', 'fecha_analisis', 'usuario')
    list_filter = ('resultado_prediccion', 'fecha_analisis')
    search_fields = ('texto', 'usuario__username')
    readonly_fields = ('fecha_analisis',)

admin.site.register(AnalisisTexto, AnalisisTextoAdmin)
