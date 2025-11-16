# Backend/codigo/views/reporte_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from ..models import AnalisisCodigo
from ..utils.generador_reporte import generar_pdf_reporte


class ReportePDFView(APIView):
    def get(self, request, id):
        try:
            obj = AnalisisCodigo.objects.get(id=id)
        except AnalisisCodigo.DoesNotExist:
            return Response({"error": "No encontrado"}, 404)

        pdf = generar_pdf_reporte(obj)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="reporte_{obj.id}.pdf"'
        return response


# =============================
#     REPORTE JSON (HU-018)
# =============================
class ReporteJSONView(APIView):
    def get(self, request, id):
        try:
            obj = AnalisisCodigo.objects.get(id=id)
        except AnalisisCodigo.DoesNotExist:
            return Response({"error": "No encontrado"}, status=404)

        # Leer archivo original
        try:
            with open(obj.archivo.path, "r", encoding="utf8") as f:
                codigo = f.read()
        except:
            codigo = "[Error al leer archivo]"

        data = {
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

        return Response(data)