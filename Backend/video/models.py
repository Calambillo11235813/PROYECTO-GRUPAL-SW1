from django.db import models
from django.conf import settings
import os


def video_upload_path(instance, filename):
	return os.path.join(getattr(settings, 'RUTA_SUBIDA_VIDEOS', 'videos/'), filename)


class VideoUpload(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('processing', 'Processing'),
		('done', 'Done'),
		('error', 'Error'),
	]

	file = models.FileField(upload_to=video_upload_path)
	original_filename = models.CharField(max_length=512, blank=True)
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	size = models.BigIntegerField(null=True, blank=True)
	duration_seconds = models.FloatField(null=True, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	notes = models.TextField(blank=True)

	def __str__(self):
		return f"VideoUpload(id={self.id}, file={self.file.name})"


class VideoFrame(models.Model):
	video = models.ForeignKey(VideoUpload, related_name='frames', on_delete=models.CASCADE)
	frame_number = models.PositiveIntegerField()
	image = models.ImageField(upload_to='frames/')
	extracted_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('video', 'frame_number')

	def __str__(self):
		return f"Frame(video_id={self.video_id}, frame={self.frame_number})"


class AnalysisResult(models.Model):
	video = models.ForeignKey(VideoUpload, related_name='analysis', on_delete=models.CASCADE)
	model_name = models.CharField(max_length=256, default='modelo_deepfake_final_corregido.h5')
	score = models.FloatField()
	verdict = models.CharField(max_length=16)  # e.g., REAL or DEEPFAKE
	created_at = models.DateTimeField(auto_now_add=True)
	details = models.JSONField(blank=True, null=True)

	def __str__(self):
		return f"Analysis(video_id={self.video_id}, score={self.score})"
