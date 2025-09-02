from django.urls import path
from . import views
from .views import CertificadoAudioView

urlpatterns = [
    path('', views.AudioAnalysisView.as_view(), name='audio-home'),
    path('analyze/', views.AudioUploadView.as_view(), name='audio-analyze'),
    path('certificado/<int:audio_id>/', CertificadoAudioView.as_view(), name='certificado-audio'),

]
