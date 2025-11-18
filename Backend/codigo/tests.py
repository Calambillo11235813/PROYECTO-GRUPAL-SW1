from django.test import TestCase

# Create your tests here.
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ArchivoCodigo

class ArchivoCodigoTest(TestCase):
    def test_subida_codigo(self):
        file = SimpleUploadedFile("test.py", b"print('hola')")
        upload = ArchivoCodigo.objects.create(file=file, filename="test.py")
        self.assertTrue(upload.pk)
