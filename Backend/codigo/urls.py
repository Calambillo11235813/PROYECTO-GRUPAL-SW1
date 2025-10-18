from django.urls import path
from .views import CodigoUploadView, CodigoHistorialView, CodigoReporteView
from . import views

urlpatterns = [
    path('', views.panel, name='codigo-panel'),
    path('upload/', CodigoUploadView.as_view(), name='codigo-upload'),
    path('history/', CodigoHistorialView.as_view(), name='codigo-history'),
    path('report/<int:codigo_id>/', CodigoReporteView.as_view(), name='codigo-report'),
]
