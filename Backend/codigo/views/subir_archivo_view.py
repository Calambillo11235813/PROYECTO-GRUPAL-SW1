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
from ..modelos.detector_hf import CodeDetectorHF

IA_MODEL = CodeDetectorHF()   # carga el modelo SOLO 1 VEZ

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
        # IA REAL (CodeBERT)
        # ============================
        ia = IA_MODEL.analizar(codigo)

        obj.ia_es_generado = ia["is_ai_generated"]
        obj.ia_confianza = ia["confidence"]
        obj.ia_metodo = ia["method_used"]
        obj.ia_detalles = ia


        # Guardar versión del modelo y timestamp
        obj.version_modelo = IA_MODEL.version
        obj.timestamp_modelo = IA_MODEL.timestamp
        
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
