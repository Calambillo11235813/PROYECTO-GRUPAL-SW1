from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import VideoUpload, AnalysisResult
import io


class VideoUploadTests(APITestCase):
	def test_upload_video_creates_videoupload(self):
		"""HU-11: Subir archivo de video crea un registro VideoUpload"""
		url = reverse('videoupload-list')
		# crear un archivo de video falso (contenido pequeño)
		video_file = SimpleUploadedFile('test.mp4', b'\x00\x00\x00\x18ftyp', content_type='video/mp4')
		data = {'file': video_file}
		response = self.client.post(url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(VideoUpload.objects.filter(id=response.data['id']).exists())


class AnalysisFlowTests(APITestCase):
	def setUp(self):
		# crear un VideoUpload para análisis
		f = SimpleUploadedFile('test.mp4', b'\x00\x00\x00\x18ftyp', content_type='video/mp4')
		self.upload = VideoUpload.objects.create(file=f, original_filename='test.mp4')

	def test_trigger_analyze_creates_analysisresult(self):
		"""HU-12: Disparar análisis crea un AnalysisResult placeholder"""
		url = reverse('videoupload-analyze', args=[self.upload.id])
		response = self.client.post(url)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(AnalysisResult.objects.filter(video=self.upload).exists())

	def test_history_list_returns_results(self):
		"""HU-14: Consultar historial de videos analizados (read-only)"""
		# crear un resultado de ejemplo
		AnalysisResult.objects.create(video=self.upload, model_name='m.h5', score=0.8, verdict='DEEPFAKE')
		url = reverse('analysisresult-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreaterEqual(len(response.data), 1)

