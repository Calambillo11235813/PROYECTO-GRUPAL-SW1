# backend/audio/serializers.py
from rest_framework import serializers
from .models import AudioUpload

class AudioUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioUpload
        fields = ['id', 'file', 'result', 'probability', 'spectrogram', 'uploaded_at']
        read_only_fields = ['result', 'probability', 'spectrogram', 'uploaded_at']
