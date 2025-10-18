from django.test import TestCase
<<<<<<< HEAD
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CodigoUpload

class CodigoUploadTest(TestCase):
    def test_subida_codigo(self):
        file = SimpleUploadedFile("test.py", b"print('hola mundo')")
        upload = CodigoUpload.objects.create(file=file, filename="test.py")
        self.assertTrue(upload.pk)
=======

# Create your tests here.
>>>>>>> UNION
