"""
Configuración de tests para el proyecto de detección de IA

Este módulo contiene todos los tests organizados por funcionalidad:
- test_file_upload.py: Tests de integración para carga de archivos
- test_api_endpoints.py: Tests de endpoints REST
- test_predictor.py: Tests del sistema de predicción
- test_file_processor.py: Tests de procesamiento de archivos
- test_models.py: Tests de modelos de base de datos
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_django():
    """Configurar Django para tests que lo requieran"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
    django.setup()

def run_tests():
    """Ejecutar todos los tests"""
    setup_django()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    return failures