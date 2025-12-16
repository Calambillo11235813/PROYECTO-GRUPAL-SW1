from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import VideoUpload, AnalysisResult
from .serializers import VideoUploadSerializer, AnalysisResultSerializer


class VideoUploadViewSet(viewsets.ModelViewSet):
	"""Endpoints for uploading videos and listing uploads/history."""
	queryset = VideoUpload.objects.all().order_by('-uploaded_at')
	serializer_class = VideoUploadSerializer
	parser_classes = [MultiPartParser, FormParser]

	def perform_create(self, serializer):
		# Save uploaded_by if request.user is authenticated
		user = self.request.user if self.request.user.is_authenticated else None
		instance = serializer.save(uploaded_by=user)
		# Fill size field if file is available
		try:
			instance.size = instance.file.size
			instance.original_filename = getattr(instance.file, 'name', '')
			instance.save(update_fields=['size', 'original_filename'])
		except Exception:
			pass

	@action(detail=True, methods=['post'])
	def analyze(self, request, pk=None):
		"""Trigger analysis for an uploaded video (creates AnalysisResult placeholder).
		Actual analysis implementation should be handled asynchronously.
		"""
		upload = get_object_or_404(VideoUpload, pk=pk)
		# Placeholder: create a pending AnalysisResult and return it
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
	"""Read-only endpoints for analysis results."""
	queryset = AnalysisResult.objects.all().order_by('-created_at')
	serializer_class = AnalysisResultSerializer

