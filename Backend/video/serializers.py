from rest_framework import serializers
from .models import VideoUpload, VideoFrame, AnalysisResult


class VideoUploadSerializer(serializers.ModelSerializer):
    # Representación legible del usuario que subió el archivo
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = VideoUpload
        fields = [
            'id', 'file', 'original_filename', 'uploaded_by', 'uploaded_at',
            'size', 'duration_seconds', 'status', 'notes'
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'size', 'duration_seconds', 'status']


class VideoFrameSerializer(serializers.ModelSerializer):
    """Serializador para frames extraídos de un video."""
    class Meta:
        model = VideoFrame
        fields = ['id', 'video', 'frame_number', 'image', 'extracted_at']
        read_only_fields = ['id', 'extracted_at']


class AnalysisResultSerializer(serializers.ModelSerializer):
    """Serializador para los resultados del análisis (score, veredicto, detalles)."""
    class Meta:
        model = AnalysisResult
        fields = ['id', 'video', 'model_name', 'score', 'verdict', 'created_at', 'details']
        read_only_fields = ['id', 'created_at']
