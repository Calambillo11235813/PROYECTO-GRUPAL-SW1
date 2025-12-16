from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import VideoUpload, AnalysisResult
from .serializers import VideoUploadSerializer, AnalysisResultSerializer


class VideoUploadViewSet(viewsets.ModelViewSet):
	"""Puntos de entrada para subir videos y listar cargas/historial."""
	queryset = VideoUpload.objects.all().order_by('-uploaded_at')
	serializer_class = VideoUploadSerializer
	parser_classes = [MultiPartParser, FormParser]

	def perform_create(self, serializer):
		# Guardar `uploaded_by` si el usuario está autenticado
		user = self.request.user if self.request.user.is_authenticated else None
		instance = serializer.save(uploaded_by=user)
		# Rellenar el campo `size` y `original_filename` si el archivo está disponible
		try:
			instance.size = instance.file.size
			instance.original_filename = getattr(instance.file, 'name', '')
			instance.save(update_fields=['size', 'original_filename'])
		except Exception:
			# En caso de error al obtener el tamaño/nombre, ignorar para no bloquear la subida
			pass

	@action(detail=True, methods=['post'])
	def analyze(self, request, pk=None):
		"""Disparar el análisis de un video subido (crea un placeholder `AnalysisResult`).
		La implementación real del análisis debe manejarse de forma asíncrona (tareas/worker).
		"""
		upload = get_object_or_404(VideoUpload, pk=pk)
		# Placeholder: crear un AnalysisResult en estado pendiente y devolverlo
		result = AnalysisResult.objects.create(
			video=upload,
			model_name='modelo_deepfake_final_corregido.h5',
			score=0.0,
			verdict='PENDING',
			details={}
		)
		serializer = AnalysisResultSerializer(result)
		upload.status = 'processing'
		upload.save(update_fields=['status'])
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnalysisResultViewSet(viewsets.ReadOnlyModelViewSet):
	"""Puntos de entrada solo-lectura para los resultados de análisis."""
	queryset = AnalysisResult.objects.all().order_by('-created_at')
	serializer_class = AnalysisResultSerializer

