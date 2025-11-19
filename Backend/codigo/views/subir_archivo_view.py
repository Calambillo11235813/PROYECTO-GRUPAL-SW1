# Backend/codigo/views/upload_view.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from ..models import AnalisisCodigo
from ..serializers import AnalisisCodigoSerializer
from ..utils.analizador_codigo import analizar_archivo_codigo
from ..utils.marcador_ia import marcar_lineas_sospechosas
from ..utils.detectar_lenguaje import detectar_lenguaje

# IMPORTANTE: usar el nuevo modelo
from ..modelos.production_code_detector import get_detector

class SubirCodigoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        archivo = request.FILES.get("archivo")
        if not archivo:
            return Response({"error": "Archivo requerido"}, 400)

        # Crear registro
        obj = AnalisisCodigo.objects.create(
            archivo=archivo,
            nombre_archivo=archivo.name,
            usuario=request.user if request.user.is_authenticated else None
        )

        ruta = obj.archivo.path

        # Leer código
        with open(ruta, "r", encoding="utf8") as f:
            codigo = f.read()
        # Detectar lenguaje del archivo
        obj.lenguaje = detectar_lenguaje(obj.nombre_archivo, codigo)

        # ============================
        # IA (CodeBERT) con fallback centralizado
        # ============================
        detector = get_detector()
        ia = detector.analizar(codigo)

        obj.ia_es_generado = ia.get("is_ai_generated", False)
        obj.ia_confianza = ia.get("confidence", 0.0)
        obj.ia_metodo = ia.get("method_used", "unknown")
        obj.ia_detalles = ia

        # Guardar versión del modelo y timestamp (si existen en el detector)
        obj.version_modelo = getattr(detector, "version", "none")
        obj.timestamp_modelo = getattr(detector, "timestamp", None)
        
        # ============================
        # IA por líneas ()
        # ============================
        lineas_sospechosas, bloques_sospechosos = marcar_lineas_sospechosas(codigo)
        obj.lineas_sospechosas = lineas_sospechosas
        obj.bloques_sospechosos = bloques_sospechosos

        # ============================
        # Análisis sintáctico
        # ============================
        analisis = analizar_archivo_codigo(ruta)

        obj.ast_json = analisis["ast"]
        obj.complejidad_ciclomatica = analisis["complejidad"]
        obj.variabilidad_funciones = analisis["variabilidad"]
        obj.patrones_control = analisis["patrones_control"]
        obj.patrones_comunes = analisis["patrones_comunes"]
        obj.idiosincrasias = analisis["idiosincrasias"]
        obj.indice_predictibilidad = analisis["predict"]



        obj.save()

        return Response(AnalisisCodigoSerializer(obj).data)
