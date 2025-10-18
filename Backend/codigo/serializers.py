from rest_framework import serializers
from .models import CodigoUpload

class CodigoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoUpload
        fields = '__all__'
        read_only_fields = ['filename', 'created_at', 'ast_json', 'complejidad', 'predict_score']

    def create(self, validated_data):
        file = validated_data.get('file')
        validated_data['filename'] = file.name if file else 'desconocido'
        return super().create(validated_data)
