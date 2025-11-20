# Backend/codigo/urls.py

from django.urls import path
from .views.panel_view import panel_inicio
from .views.subir_archivo_view import SubirCodigoView
from .views.historial_view import (
    HistorialAnalisisView,
    CompararAnalisisView,
    EstadisticasHistorialView,
    ExportarHistorialJSONView,
    EliminarHistorialView
)
from .views.reporte_view import ReportePDFView, ReporteJSONView
from .views.analisis_view import AnalisisDetalleView, EliminarAnalisisView

urlpatterns = [

    # ===============================
    #  PANEL HTML (VISTA PRINCIPAL)
    # ===============================
    path("", panel_inicio, name="codigo_panel"),

    # ===============================
    #  SUBIR ARCHIVO
    # ===============================
    path("subir/", SubirCodigoView.as_view(), name="codigo_subir"),
    
    # ===============================
    #  ANÁLISIS INDIVIDUAL
    # ===============================
    path("analisis/<int:pk>/", AnalisisDetalleView.as_view(), name="codigo_analisis_detalle"),
    path("analisis/<int:pk>/eliminar/", EliminarAnalisisView.as_view(), name="codigo_analisis_eliminar"),
    
    # ===============================
    #  HISTORIAL / FILTROS
    # ===============================
    path("historial/", HistorialAnalisisView.as_view(), name="codigo_historial"),
    path("historial/eliminar/", EliminarHistorialView.as_view(), name="codigo_historial_eliminar"),
    path("historial/comparar/", CompararAnalisisView.as_view(), name="codigo_comparar"),
    path("historial/estadisticas/", EstadisticasHistorialView.as_view(), name="codigo_estadisticas"),
    path("historial/exportar/", ExportarHistorialJSONView.as_view(), name="codigo_exportar"),

    # ===============================
    #  REPORTES
    # ===============================
    path("reporte/pdf/<int:id>/", ReportePDFView.as_view(), name="codigo_reporte_pdf"),
    path("reporte/json/<int:id>/", ReporteJSONView.as_view(), name="codigo_reporte_json"),
]
