import os
import tempfile
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from texto.models import AnalisisTexto, ArchivoAnalisis  # Import absoluto
from texto.file_processor import FileProcessor  # Import absoluto

class FileUploadTestCase(TestCase):
    """Tests unitarios para funcionalidad de carga de archivos"""
    
    def setUp(self):
        self.client = Client()
    
    def test_upload_txt_file(self):
        """Test de subida de archivo TXT"""
        content = "Este es un texto de prueba para analizar si fue generado por inteligencia artificial. " \
                 "El contenido debe tener suficiente longitud para ser procesado correctamente por el sistema."
        txt_file = SimpleUploadedFile("test.txt", content.encode('utf-8'), content_type="text/plain")
        
        response = self.client.post('/analizar-archivo/', {
            'archivo': txt_file,
            'modelo': 'B'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('resultado', data)
        self.assertIn('archivo_info', data)
        self.assertEqual(data['archivo_info']['nombre'], 'test.txt')
        self.assertEqual(data['modelo_utilizado'], 'B')
        
        # Verificar que se guardó en la base de datos
        analisis = AnalisisTexto.objects.get(id=data['analisis_id'])
        self.assertEqual(analisis.tipo_entrada, 'ARCHIVO')
        self.assertEqual(analisis.nombre_archivo, 'test.txt')
        
    def test_file_too_large(self):
        """Test de archivo demasiado grande"""
        large_content = "A" * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile("large.txt", large_content.encode('utf-8'))
        
        response = self.client.post('/api/analizar-archivo/', {'archivo': large_file})
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('demasiado grande', data['error'])
        self.assertEqual(data['codigo'], 'ARCHIVO_INVALIDO')
    
    def test_unsupported_format(self):
        """Test de formato no soportado"""
        img_file = SimpleUploadedFile("test.jpg", b"fake image content", content_type="image/jpeg")
        
        response = self.client.post('/analizar-archivo/', {'archivo': img_file})
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('no soportado', data['error'])
        self.assertEqual(data['codigo'], 'ARCHIVO_INVALIDO')
    
    def test_no_file_provided(self):
        """Test sin archivo"""
        response = self.client.post('/analizar-archivo/', {'modelo': 'B'})
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['codigo'], 'ARCHIVO_FALTANTE')
    
    def test_compare_models_with_file(self):
        """Test de comparación de modelos con archivo"""
        content = "Este es un texto para comparar ambos modelos de detección de IA. " \
                 "Debe ser lo suficientemente largo para obtener resultados precisos de ambos modelos."
        txt_file = SimpleUploadedFile("compare.txt", content.encode('utf-8'), content_type="text/plain")
        
        response = self.client.post('/comparar-archivo/', {
            'archivo': txt_file
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('modelo_b', data)
        self.assertIn('modelo_n', data)
        self.assertIn('consenso', data)
        self.assertIn('archivo_info', data)
    
    def test_file_processor_validation(self):
        """Test del procesador de archivos"""
        # Test archivo válido
        valid_file = SimpleUploadedFile("test.txt", b"contenido valido", content_type="text/plain")
        is_valid, message = FileProcessor.validate_file(valid_file)
        self.assertTrue(is_valid)
        
        # Test archivo muy grande
        large_content = b"A" * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile("large.txt", large_content)
        is_valid, message = FileProcessor.validate_file(large_file)
        self.assertFalse(is_valid)
        self.assertIn('demasiado grande', message)
    
    def test_text_extraction(self):
        """Test de extracción de texto"""
        content = "Contenido de prueba para extracción"
        txt_file = SimpleUploadedFile("extract.txt", content.encode('utf-8'), content_type="text/plain")
        
        success, extracted_text = FileProcessor.extract_text(txt_file)
        self.assertTrue(success)
        self.assertEqual(extracted_text.strip(), content)