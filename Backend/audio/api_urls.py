from django.urls import path
from .views import AudioUploadView

app_name = 'audio_api'

urlpatterns = [
    path('analyze/', AudioUploadView.as_view(), name='audio-analyze'),
]
