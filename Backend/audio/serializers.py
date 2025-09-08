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
        fields = [
            'id', 'file', 'file_url', 'original_filename',
            'result', 'probability', 'spectrogram', 'created_at'
        ]
        read_only_fields = [
            'result', 'probability', 'spectrogram', 
            'created_at', 'file_url', 'original_filename'
        ]
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def validate_file(self, archivo):
        """
        Valida archivo antes de guardarlo y guarda nombre original.
        """
        self.context['original_name'] = archivo.name

        if archivo.content_type not in settings.TIPOS_AUDIO_PERMITIDOS:
            raise ValidationError({
                'error': 'tipo_audio_no_soportado',
                'mensaje': 'Tipo de archivo de audio no soportado',
                'tipos_audio_permitidos': settings.TIPOS_AUDIO_PERMITIDOS
            })
        if archivo.size > settings.TAMANO_MAXIMO_AUDIO:
            tamano_max_mb = settings.TAMANO_MAXIMO_AUDIO / (1024*1024)
            raise ValidationError({
                'error': 'tamano_excedido',
                'mensaje': 'El archivo excede el tamaño máximo permitido',
                'tamano_maximo_mb': tamano_max_mb,
                'tamano_actual_mb': round(archivo.size/(1024*1024), 2)
            })
        
        extension = os.path.splitext(archivo.name)[1].lower()
        archivo.name = f'audio_{uuid.uuid4().hex[:8]}{extension}'
        return archivo
    
    def create(self, validated_data):
        original_name = self.context.get('original_name')
        if original_name:
            validated_data['original_filename'] = original_name
        return super().create(validated_data)
