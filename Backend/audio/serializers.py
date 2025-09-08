import os
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import AudioUpload
import uuid

class AudioUploadSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    original_filename = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = AudioUpload
        fields = ['id', 'file', 'file_url', 'original_filename', 'result', 'probability', 'spectrogram', 'uploaded_at']
        read_only_fields = ['result', 'probability', 'spectrogram', 'uploaded_at', 'file_url']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def create(self, validated_data):
        # Guardar el nombre original del archivo si se proporciona
        original_filename = validated_data.pop('original_filename', None)
        if not original_filename and 'file' in validated_data:
            original_filename = validated_data['file'].name
        
        instance = super().create(validated_data)
        if original_filename:
            instance.original_filename = original_filename
            instance.save()
        return instance
    
    def validate_file(self, archivo):
        """
        Valida el archivo multimedia (audio o video) antes de guardarlo.
        """
        tipo_contenido = archivo.content_type
        
        # Validar tipo de archivo
        tipo_contenido = archivo.content_type
        if tipo_contenido not in settings.TIPOS_AUDIO_PERMITIDOS:
            raise ValidationError({
                'error': 'tipo_audio_no_soportado',
                'mensaje': 'Tipo de archivo de audio no soportado',
                'tipos_audio_permitidos': settings.TIPOS_AUDIO_PERMITIDOS
            })
        
        # Validar tamaño del archivo
        if archivo.size > settings.TAMANO_MAXIMO_AUDIO:
            tamano_max_mb = settings.TAMANO_MAXIMO_AUDIO / (1024 * 1024)
            raise ValidationError({
                'error': 'tamano_excedido',
                'mensaje': 'El archivo de audio excede el tamaño máximo permitido',
                'tamano_maximo_mb': tamano_max_mb,
                'tamano_actual_mb': round(archivo.size / (1024 * 1024), 2)
            })
        
        # Generar un nombre de archivo seguro
        extension = os.path.splitext(archivo.name)[1].lower()
        nombre_seguro = f'audio_{uuid.uuid4().hex[:8]}{extension}'
        archivo.name = nombre_seguro
        
        return archivo
