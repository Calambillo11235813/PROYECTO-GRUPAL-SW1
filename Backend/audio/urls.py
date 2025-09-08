from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import CertificadoAudioView

urlpatterns = [
    # Autenticación
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoints de audio
    path('', views.AudioAnalysisView.as_view(), name='audio-list'),
    path('upload/', views.AudioUploadView.as_view(), name='audio-upload'),
    path('certificado/<int:audio_id>/', 
         CertificadoAudioView.as_view(), 
         name='certificado-audio'
    ),
]
