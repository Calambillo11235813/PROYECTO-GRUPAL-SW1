from django.urls import path
from . import views

urlpatterns = [
    path('', views.AudioAnalysisView.as_view(), name='audio-home'),
    path('analyze/', views.AudioUploadView.as_view(), name='audio-analyze'),
]
