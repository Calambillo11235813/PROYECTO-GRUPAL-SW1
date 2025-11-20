# Backend/codigo/views/reporte_view.py
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from ..models import AnalisisCodigo
from ..utils.generador_reporte import generar_pdf_reporte

logger = logging.getLogger(__name__)


class ReportePDFView(APIView):
    def get(self, request, id):
        """
        Genera y descarga un reporte PDF del análisis.
        Usuarios autenticados solo pueden ver reportes de sus propios análisis.
        """
        try:
            # Validar que el ID sea un número
            try:
                id = int(id)
            except ValueError:
                return Response(
                    {"error": "ID inválido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Filtrar por usuario si está autenticado
            if request.user.is_authenticated:
                if request.user.is_staff:
                    obj = AnalisisCodigo.objects.get(id=id)
                else:
                    obj = AnalisisCodigo.objects.get(id=id, usuario=request.user)
            else:
                obj = AnalisisCodigo.objects.get(id=id, usuario__isnull=True)

        except AnalisisCodigo.DoesNotExist:
            return Response(
                {"error": "Análisis no encontrado o no tienes permiso para verlo"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error al obtener análisis {id}: {e}")
            return Response(
                {"error": "Error al obtener el análisis"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            pdf = generar_pdf_reporte(obj)
        except Exception as e:
            logger.error(f"Error al generar PDF para análisis {id}: {e}", exc_info=True)
            return Response(
                {"error": "Error al generar el reporte PDF"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="reporte_{obj.id}.pdf"'
        return response


# =============================
#     REPORTE JSON (HU-018)
# =============================
class ReporteJSONView(APIView):
    def get(self, request, id):
        """
        Genera un reporte JSON del análisis.
        Usuarios autenticados solo pueden ver reportes de sus propios análisis.
        """
        try:
            # Validar que el ID sea un número
            try:
                id = int(id)
            except ValueError:
                return Response(
                    {"error": "ID inválido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Filtrar por usuario si está autenticado
            if request.user.is_authenticated:
                if request.user.is_staff:
                    obj = AnalisisCodigo.objects.get(id=id)
                else:
                    obj = AnalisisCodigo.objects.get(id=id, usuario=request.user)
            else:
                obj = AnalisisCodigo.objects.get(id=id, usuario__isnull=True)

        except AnalisisCodigo.DoesNotExist:
            return Response(
                {"error": "Análisis no encontrado o no tienes permiso para verlo"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error al obtener análisis {id}: {e}")
            return Response(
                {"error": "Error al obtener el análisis"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Leer archivo original con manejo de encoding
        try:
            # Intentar UTF-8 primero
            with open(obj.archivo.path, "r", encoding="utf-8") as f:
                codigo = f.read()
        except UnicodeDecodeError:
            try:
                # Fallback a latin-1
                with open(obj.archivo.path, "r", encoding="latin-1") as f:
                    codigo = f.read()
            except Exception as e:
                logger.error(f"Error al leer archivo {obj.archivo.path}: {e}")
                codigo = "[Error al leer archivo]"
        except Exception as e:
            logger.error(f"Error inesperado al leer archivo: {e}")
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