import os
import logging
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
from .models import AudioUpload
from .serializers import AudioUploadSerializer
from .ia_model import verificar_autenticidad
from .utils import generar_espectrograma
from .certificado_utils import generar_certificado_pdf

# Configuración del logger
logger = logging.getLogger(__name__)

class AudioUploadView(APIView):
    """
    Vista para manejar la subida y procesamiento de archivos de audio.
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            # Validar que se haya enviado un archivo
            if 'file' not in request.FILES:
                return Response(
                    {'error': 'No se ha proporcionado ningún archivo de audio'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar el archivo con el serializador
            file_serializer = AudioUploadSerializer(data=request.data)
            
            if not file_serializer.is_valid():
                return Response(
                    file_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Guardar el modelo
            audio_upload = file_serializer.save()
            
            try:
                # Procesar el audio con el modelo de IA
                audio_path = audio_upload.file.path
                logger.info(f"Procesando archivo de audio: {audio_path}")
                
                # Verificar autenticidad del audio
                result, probability = verificar_autenticidad(audio_path)
                
                # Generar espectrograma con el nombre original del archivo
                original_filename = audio_upload.original_filename or os.path.basename(audio_upload.file.name)
                spectrogram_path = generar_espectrograma(
                    audio_path, 
                    file_id=str(audio_upload.id),
                    original_filename=original_filename
                )
                
                # Actualizar el modelo con los resultados
                audio_upload.result = result
                audio_upload.probability = probability
                audio_upload.spectrogram = spectrogram_path
                audio_upload.save()
                
                logger.info(f"Análisis completado. Resultado: {result}, Probabilidad: {probability}")
                
                # Devolver los resultados
                return Response({
                    'status': 'success',
                    'data': AudioUploadSerializer(audio_upload).data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                # Registrar el error
                logger.error(f"Error al procesar el archivo de audio: {str(e)}", exc_info=True)
                
                # Limpiar archivos en caso de error
                if hasattr(audio_upload, 'file') and audio_upload.file and os.path.exists(audio_upload.file.path):
                    try:
                        os.remove(audio_upload.file.path)
                    except Exception as cleanup_error:
                        logger.error(f"Error al limpiar archivo subido: {str(cleanup_error)}")
                
                # Eliminar el registro de la base de datos
                audio_upload.delete()
                
                return Response(
                    {'error': 'Ocurrió un error al procesar el archivo de audio'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            logger.critical(f"Error inesperado en AudioUploadView: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, *args, **kwargs):
        # Obtener el historial de análisis
        uploads = AudioUpload.objects.all().order_by('-created_at')
        serializer = AudioUploadSerializer(uploads, many=True, context={'request': request})
        return Response(serializer.data)


class AudioAnalysisView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'audio/index.html')


class CertificadoAudioView(APIView):
    """
    Vista para generar y descargar el certificado de análisis de un audio.
    """
    def get(self, request, audio_id, *args, **kwargs):
        try:
            # Obtener el objeto AudioUpload
            audio_upload = get_object_or_404(AudioUpload, id=audio_id)
            
            # Generar el PDF del certificado
            pdf_content = generar_certificado_pdf(audio_upload)
            
            # Crear la respuesta con el PDF
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            filename = f"certificado_analisis_{audio_upload.original_filename or 'audio'}_{timestamp}.pdf"
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response.write(pdf_content)
            
            return response
            
        except Exception as e:
            logger.error(f"Error al generar el certificado: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Ocurrió un error al generar el certificado'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
