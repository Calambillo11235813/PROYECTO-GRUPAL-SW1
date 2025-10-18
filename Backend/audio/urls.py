from django.urls import path
<<<<<<< HEAD
=======
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
>>>>>>> UNION
from . import views
from .views import CertificadoAudioView

urlpatterns = [
<<<<<<< HEAD
    path('', views.AudioAnalysisView.as_view(), name='audio-home'),
    path('analyze/', views.AudioUploadView.as_view(), name='audio-analyze'),
    path('certificado/<int:audio_id>/', CertificadoAudioView.as_view(), name='certificado-audio'),

=======
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
>>>>>>> UNION
]
