import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import AnalisisCodigo
from ..serializers import AnalisisCodigoSerializer, AnalisisRespuestaSerializer

logger = logging.getLogger(__name__)


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
            # Filtrar por usuario si está autenticado (opcional: mostrar todos si es admin)
            if request.user.is_authenticated:
                # Si no es staff, solo mostrar sus propios análisis
                if not request.user.is_staff:
                    obj = AnalisisCodigo.objects.get(id=pk, usuario=request.user)
                else:
                    obj = AnalisisCodigo.objects.get(id=pk)
            else:
                # Usuarios anónimos pueden ver análisis sin usuario asignado
                obj = AnalisisCodigo.objects.get(id=pk, usuario__isnull=True)
        except AnalisisCodigo.DoesNotExist:
            return Response(
                {"error": "Análisis no encontrado o no tienes permiso para verlo"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error al obtener análisis {pk}: {e}")
            return Response(
                {"error": "Error al obtener el análisis"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Leer el código original
        codigo = ""
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
                codigo = "[Error al leer archivo original]"
        except Exception as e:
            logger.error(f"Error inesperado al leer archivo: {e}")
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


# =======================================================
# 📌 ELIMINAR ANÁLISIS INDIVIDUAL
# =======================================================
class EliminarAnalisisView(APIView):
    def delete(self, request, pk):
        """
        Elimina un análisis específico.
        Usuarios solo pueden eliminar sus propios análisis (staff puede eliminar cualquiera).
        """
        try:
            # Validar que el ID sea un número
            try:
                pk = int(pk)
            except ValueError:
                return Response(
                    {"error": "ID inválido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obtener el análisis con filtrado por usuario
            try:
                if request.user.is_authenticated:
                    if request.user.is_staff:
                        obj = AnalisisCodigo.objects.get(id=pk)
                    else:
                        obj = AnalisisCodigo.objects.get(id=pk, usuario=request.user)
                else:
                    obj = AnalisisCodigo.objects.get(id=pk, usuario__isnull=True)
            except AnalisisCodigo.DoesNotExist:
                return Response(
                    {"error": "Análisis no encontrado o no tienes permiso para eliminarlo"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Guardar información antes de eliminar
            nombre_archivo = obj.nombre_archivo
            archivo_path = obj.archivo.path if obj.archivo else None

            # Eliminar archivo físico si existe
            try:
                if obj.archivo:
                    obj.archivo.delete(save=False)
            except Exception as e:
                logger.warning(f"Error al eliminar archivo {archivo_path}: {e}")

            # Eliminar el registro de la base de datos
            obj.delete()

            logger.info(f"Análisis {pk} ({nombre_archivo}) eliminado por usuario {request.user.username if request.user.is_authenticated else 'anónimo'}")

            return Response({
                "mensaje": f"Análisis '{nombre_archivo}' eliminado correctamente",
                "id_eliminado": pk
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en EliminarAnalisisView: {e}", exc_info=True)
            return Response(
                {"error": "Error al eliminar el análisis"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
