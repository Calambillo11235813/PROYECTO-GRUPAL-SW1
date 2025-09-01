# backend/audio/views.py
import os
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import AudioUpload
from .serializers import AudioUploadSerializer
from .ia_model import verificar_autenticidad
from .utils import generar_espectrograma

class AudioUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = AudioUploadSerializer(data=request.data)
        
        if file_serializer.is_valid():
            audio_upload = file_serializer.save()
            
            try:
                # Procesar el audio con el modelo de IA
                audio_path = audio_upload.file.path
                result, probability = verificar_autenticidad(audio_path)
                spectrogram_path = generar_espectrograma(audio_path, str(audio_upload.id))
                
                # Actualizar el modelo con los resultados
                audio_upload.result = result
                audio_upload.probability = probability
                audio_upload.spectrogram = spectrogram_path
                audio_upload.save()
                
                # Devolver los resultados
                return Response({
                    'status': 'success',
                    'data': AudioUploadSerializer(audio_upload).data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                # En caso de error, eliminar el archivo subido
                if os.path.exists(audio_upload.file.path):
                    os.remove(audio_upload.file.path)
                audio_upload.delete()
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # Obtener el historial de análisis
        uploads = AudioUpload.objects.all().order_by('-uploaded_at')
        serializer = AudioUploadSerializer(uploads, many=True)
        return Response(serializer.data)


class AudioAnalysisView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'audio/index.html')
