from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import AnalisisCodigo
from ..serializers import AnalisisCodigoSerializer
from codigo.serializers import AnalisisRespuestaSerializer, AnalisisCodigoSerializer


# =======================================================
# 📌 LISTAR TODOS LOS ANÁLISIS (RAW / historial)
# =======================================================
class AnalisisListaView(APIView):
    def get(self, request):
        analisis = AnalisisCodigo.objects.all().order_by('-fecha_analisis')
        serializer = AnalisisCodigoSerializer(analisis, many=True)
        return Response(serializer.data)


# =======================================================
# 📌 DETALLE PROFESIONAL (Con secciones)
# =======================================================
class AnalisisDetalleView(APIView):
    def get(self, request, pk):
        try:
            obj = AnalisisCodigo.objects.get(id=pk)
        except AnalisisCodigo.DoesNotExist:
            return Response({"error": "Análisis no encontrado"}, status=404)

        # Leer el código original
        codigo = ""
        try:
            with open(obj.archivo.path, "r", encoding="utf8") as f:
                codigo = f.read()
        except:
            codigo = "[Error al leer archivo original]"

        # Construir respuesta profesional
        respuesta = {
            "info_archivo": {
                "id": obj.id,
                "nombre": obj.nombre_archivo,
                "lenguaje": obj.lenguaje,
                "ruta": obj.archivo.url if obj.archivo else None,
                "tamano_bytes": obj.archivo.size if obj.archivo else None,
            },

            "analisis_ia": {
                "es_generado": obj.ia_es_generado,
                "confianza": obj.ia_confianza,
                "prob_ai": obj.ia_detalles.get("ai_prob") if obj.ia_detalles else None,
                "prob_humano": obj.ia_detalles.get("human_prob") if obj.ia_detalles else None,
                "metodo": obj.ia_metodo,
                "version_modelo": obj.version_modelo,
                "timestamp_modelo": obj.timestamp_modelo,
            },

            "resaltado_ia": {
                "lineas_sospechosas": obj.lineas_sospechosas,
                "bloques": obj.bloques_sospechosos,
            },

            "metricas_codigo": {
                "complejidad_ciclomatica": obj.complejidad_ciclomatica,
                "variabilidad_funciones": obj.variabilidad_funciones,
                "indice_predictibilidad": obj.indice_predictibilidad,
            },

            "patrones_sintacticos": {
                "patrones_control": obj.patrones_control,
                "idiosincrasias": obj.idiosincrasias,
                "patrones_comunes": obj.patrones_comunes,
            },

            "codigo_original": codigo,
            "ast": obj.ast_json,
            "timestamp_analisis": obj.fecha_analisis,
        }

        serializer = AnalisisRespuestaSerializer(respuesta)
        return Response(serializer.data)
