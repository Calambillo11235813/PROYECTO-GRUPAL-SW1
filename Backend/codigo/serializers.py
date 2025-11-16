# backend/codigo/serializers.py
from rest_framework import serializers
from .models import AnalisisCodigo


# =======================================
# SERIALIZER BASE (MODELO COMPLETO)
# =======================================
class AnalisisCodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalisisCodigo
        fields = '__all__'


# =======================================
# SERIALIZER PERSONALIZADO (RESPUESTA DETALLADA)
# =======================================
class AnalisisRespuestaSerializer(serializers.Serializer):
    info_archivo = serializers.DictField()
    analisis_ia = serializers.DictField()
    resaltado_ia = serializers.DictField()
    metricas_codigo = serializers.DictField()
    patrones_sintacticos = serializers.DictField()
    codigo_original = serializers.CharField()
    ast = serializers.CharField()
    timestamp_analisis = serializers.DateTimeField()
