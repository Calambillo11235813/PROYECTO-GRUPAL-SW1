<<<<<<< HEAD
import os
import logging
import traceback
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import CodigoUpload
from .serializers import CodigoUploadSerializer
from .utils_analysis import analizar_codigo
from .utils_report import generar_reporte

# 🔹 Logger configurado para esta app
logger = logging.getLogger('codigo')


def panel(request):
    """
    Renderiza el panel principal de análisis de código.
    """
    return render(request, 'codigo/panel.html')


class CodigoUploadView(APIView):
    """
    Sube un archivo de código, ejecuta el análisis sintáctico y predictivo,
    y almacena todas las métricas resultantes.
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        logger.info("📤 Solicitud recibida para subir un archivo de código.")

        # 🔹 Obtener archivo
        file = request.FILES.get('file')
        if not file:
            logger.warning("⚠️ No se envió ningún archivo.")
            return Response({'error': 'No se envió ningún archivo'}, status=400)

        # 🔹 Validar extensión
        if not file.name.endswith('.py'):
            logger.warning(f"⚠️ Archivo rechazado (no .py): {file.name}")
            return Response({'error': 'Solo se permiten archivos .py'}, status=400)

        # 🔹 Guardar registro en base de datos
        serializer = CodigoUploadSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            file_path = instance.file.path
            logger.info(f"✅ Archivo guardado temporalmente en: {file_path}")

            try:
                # 🔹 Analizar el archivo
                resultado = analizar_codigo(file_path)

                # 🔹 Guardar métricas del análisis
                instance.ast_json = resultado['ast']
                instance.complejidad = resultado['complejidad']
                instance.predict_score = resultado['predict_score']
                instance.naming_score = resultado.get('naming_score')
                instance.repetitividad = resultado.get('repetitividad')
                instance.tipo_codigo = resultado.get('tipo_codigo')
                instance.save()

                logger.info(
                    f"🎯 Análisis completado para {file.name} → "
                    f"CC={instance.complejidad}, Naming={instance.naming_score}, "
                    f"Repetitividad={instance.repetitividad}, Tipo={instance.tipo_codigo}"
                )

                return Response({
                    'status': 'success',
                    'mensaje': 'Análisis completado exitosamente',
                    'data': CodigoUploadSerializer(instance).data
                }, status=201)

            except Exception as e:
                # 🔹 Capturar y registrar errores de análisis
                logger.error("❌ Error durante el análisis de código", exc_info=True)
                print("❌ ERROR EN TERMINAL:")
                traceback.print_exc()

                instance.delete()
                return Response({'error': str(e)}, status=500)

        # 🔹 Si el serializer falla
        logger.error(f"❌ Error en serializer: {serializer.errors}")
        return Response(serializer.errors, status=400)


class CodigoHistorialView(APIView):
    """
    Devuelve el historial de análisis realizados.
    """
    def get(self, request):
        logger.info("📋 Solicitando historial de análisis de código...")
        data = CodigoUpload.objects.all().order_by('-created_at')
        return Response(CodigoUploadSerializer(data, many=True).data)


class CodigoReporteView(APIView):
    """
    Genera un reporte PDF detallado con las métricas del análisis.
    """
    def get(self, request, codigo_id):
        logger.info(f"🧾 Generando reporte PDF para código ID={codigo_id}")

        try:
            codigo = CodigoUpload.objects.get(id=codigo_id)
        except CodigoUpload.DoesNotExist:
            logger.warning(f"⚠️ Código ID={codigo_id} no encontrado.")
            return Response({'error': 'Análisis no encontrado'}, status=404)

        pdf = generar_reporte(codigo)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=\"reporte_{codigo.filename}.pdf\"'
        logger.info(f"📑 Reporte generado correctamente para {codigo.filename}")
        return response
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> UNION
