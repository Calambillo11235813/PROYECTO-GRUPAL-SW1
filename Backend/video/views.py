from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404


from .models import VideoUpload, AnalysisResult
from .serializers import VideoUploadSerializer, AnalysisResultSerializer
from .deepfake_utils import DeepfakeDetector


class VideoUploadViewSet(viewsets.ModelViewSet):
	"""Puntos de entrada para subir videos y listar cargas/historial."""
	queryset = VideoUpload.objects.all().order_by('-uploaded_at')
	serializer_class = VideoUploadSerializer
	parser_classes = [MultiPartParser, FormParser]

	@action(detail=False, methods=['delete'], url_path='delete-all')
	def delete_all(self, request):
		"""Eliminar todos los videos del historial."""
		count = VideoUpload.objects.all().count()
		VideoUpload.objects.all().delete()
		return Response({'deleted': count}, status=status.HTTP_200_OK)

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
		"""Disparar el análisis real de deepfake sobre el video subido."""
		upload = get_object_or_404(VideoUpload, pk=pk)
		video_path = upload.file.path
		detector = DeepfakeDetector()
		try:
			score, verdict, suspicious_frames = detector.predict(video_path)
			details = {
				"total_frames_analyzed": len(suspicious_frames) if verdict == 'DEEPFAKE' else 0,
				"suspicious_frames": suspicious_frames,
				"note": "Análisis completado con detección de timestamps"
			}
		except Exception as e:
			score = 0.0
			verdict = 'ERROR'
			details = {"error": str(e), "suspicious_frames": []}
		result = AnalysisResult.objects.create(
			video=upload,
			model_name='modelo_deepfake_final_corregido.h5',
			score=score,
			verdict=verdict,
			details=details
		)
		serializer = AnalysisResultSerializer(result)
		upload.status = 'done' if verdict in ['REAL', 'DEEPFAKE'] else 'error'
		upload.save(update_fields=['status'])
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnalysisResultViewSet(viewsets.ModelViewSet):
	"""Puntos de entrada para los resultados de análisis (con eliminación)."""
	queryset = AnalysisResult.objects.all().order_by('-created_at')
	serializer_class = AnalysisResultSerializer
	http_method_names = ['get', 'delete']  # Solo GET y DELETE

	@action(detail=False, methods=['delete'], url_path='delete-all')
	def delete_all(self, request):
		"""Eliminar todos los resultados del historial."""
		count = AnalysisResult.objects.all().count()
		AnalysisResult.objects.all().delete()
		return Response({'deleted': count}, status=status.HTTP_200_OK)

