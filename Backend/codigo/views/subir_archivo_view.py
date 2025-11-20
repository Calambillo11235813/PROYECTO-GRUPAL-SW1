# Backend/codigo/views/upload_view.py
import logging
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from ..models import AnalisisCodigo
from ..serializers import AnalisisCodigoSerializer
from ..utils.analizador_codigo import analizar_archivo_codigo
from ..utils.marcador_ia import marcar_lineas_sospechosas
from ..utils.detectar_lenguaje import detectar_lenguaje

# IMPORTANTE: usar el nuevo modelo
from ..modelos.production_code_detector import get_detector

logger = logging.getLogger(__name__)

# Extensiones permitidas
EXTENSIONES_PERMITIDAS = {'.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.ts', '.tsx', '.jsx'}
TAMANO_MAXIMO_MB = 10  # 10 MB máximo


class SubirCodigoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        """
        Sube y analiza un archivo de código.
        Valida tipo, tamaño y procesa el análisis completo.
        """
        try:
            archivo = request.FILES.get("archivo")
            if not archivo:
                return Response(
                    {"error": "Archivo requerido. Envía un archivo con la clave 'archivo'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validar extensión del archivo
            nombre_archivo = archivo.name
            extension = '.' + nombre_archivo.split('.')[-1].lower() if '.' in nombre_archivo else ''
            if extension not in EXTENSIONES_PERMITIDAS:
                return Response(
                    {
                        "error": f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(EXTENSIONES_PERMITIDAS)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validar tamaño del archivo (10 MB máximo)
            tamano_mb = archivo.size / (1024 * 1024)
            if tamano_mb > TAMANO_MAXIMO_MB:
                return Response(
                    {"error": f"El archivo es demasiado grande. Tamaño máximo: {TAMANO_MAXIMO_MB} MB"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Crear registro
            obj = AnalisisCodigo.objects.create(
                archivo=archivo,
                nombre_archivo=nombre_archivo,
                usuario=request.user if request.user.is_authenticated else None
            )

            ruta = obj.archivo.path

            # Leer código con manejo de encoding
            try:
                # Intentar UTF-8 primero
                with open(ruta, "r", encoding="utf-8") as f:
                    codigo = f.read()
            except UnicodeDecodeError:
                try:
                    # Fallback a latin-1
                    with open(ruta, "r", encoding="latin-1") as f:
                        codigo = f.read()
                except Exception as e:
                    logger.error(f"Error al leer archivo {ruta}: {e}")
                    obj.delete()  # Eliminar registro si no se puede leer
                    return Response(
                        {"error": "No se pudo leer el archivo. Verifica que sea un archivo de texto válido."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Validar que el archivo no esté vacío
            if not codigo.strip():
                obj.delete()
                return Response(
                    {"error": "El archivo está vacío."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Detectar lenguaje del archivo
            try:
                obj.lenguaje = detectar_lenguaje(obj.nombre_archivo, codigo)
            except Exception as e:
                logger.warning(f"Error al detectar lenguaje: {e}")
                obj.lenguaje = "unknown"

            # ============================
            # IA (CodeBERT) con fallback centralizado
            # ============================
            try:
                detector = get_detector()
                ia = detector.analizar(codigo)
                
                obj.ia_es_generado = ia.get("is_ai_generated", False)
                obj.ia_confianza = ia.get("confidence", 0.0)
                obj.ia_metodo = ia.get("method_used", "unknown")
                obj.ia_detalles = ia

                # Guardar versión del modelo y timestamp (si existen en el detector)
                obj.version_modelo = getattr(detector, "version", "none")
                obj.timestamp_modelo = getattr(detector, "timestamp", None)
            except Exception as e:
                logger.error(f"Error en análisis IA: {e}")
                # Valores por defecto si falla el detector
                obj.ia_es_generado = False
                obj.ia_confianza = 0.0
                obj.ia_metodo = "error"
                obj.ia_detalles = {"error": str(e)}

            # ============================
            # IA por líneas
            # ============================
            try:
                lineas_sospechosas, bloques_sospechosos = marcar_lineas_sospechosas(codigo)
                obj.lineas_sospechosas = lineas_sospechosas
                obj.bloques_sospechosos = bloques_sospechosos
            except Exception as e:
                logger.warning(f"Error al marcar líneas sospechosas: {e}")
                obj.lineas_sospechosas = []
                obj.bloques_sospechosos = []

            # ============================
            # Análisis sintáctico
            # ============================
            try:
                analisis = analizar_archivo_codigo(ruta)

                obj.ast_json = analisis.get("ast")
                obj.complejidad_ciclomatica = analisis.get("complejidad", 0)
                obj.variabilidad_funciones = analisis.get("variabilidad", 0)
                obj.patrones_control = analisis.get("patrones_control", {})
                obj.patrones_comunes = analisis.get("patrones_comunes", {})
                obj.idiosincrasias = analisis.get("idiosincrasias", {})
                obj.indice_predictibilidad = analisis.get("predict", 0)
            except Exception as e:
                logger.error(f"Error en análisis sintáctico: {e}")
                # Valores por defecto si falla el análisis
                obj.ast_json = None
                obj.complejidad_ciclomatica = 0
                obj.variabilidad_funciones = 0
                obj.patrones_control = {}
                obj.patrones_comunes = {}
                obj.idiosincrasias = {}
                obj.indice_predictibilidad = 0

            obj.save()

            return Response(AnalisisCodigoSerializer(obj).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error inesperado en SubirCodigoView: {e}", exc_info=True)
            return Response(
                {"error": "Error interno del servidor al procesar el archivo."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
