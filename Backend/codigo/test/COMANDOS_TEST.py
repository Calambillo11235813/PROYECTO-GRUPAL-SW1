"""
Script de comandos rápidos para ejecutar tests del detector de IA
=====================================================================

Este archivo contiene comandos útiles para probar el detector de código IA.
"""

# ============================================================================
# EJECUTAR TODOS LOS TESTS UNITARIOS
# ============================================================================

# Windows PowerShell:
python manage.py test codigo.test_detector_ia

# Linux/Mac:
python3 manage.py test codigo.test_detector_ia


# ============================================================================
# EJECUTAR TESTS ESPECÍFICOS
# ============================================================================

# Test de detector disponible:
python manage.py test codigo.test_detector_ia.CodigoIATestCase.test_detector_disponible

# Test de código humano:
python manage.py test codigo.test_detector_ia.CodigoIATestCase.test_codigo_simple_humano

# Test de código IA:
python manage.py test codigo.test_detector_ia.CodigoIATestCase.test_codigo_ia_generado

# Test de análisis sintáctico:
python manage.py test codigo.test_detector_ia.CodigoIATestCase.test_analisis_codigo_simple

# Test de marcado de líneas:
python manage.py test codigo.test_detector_ia.CodigoIATestCase.test_marcado_lineas_codigo_limpio

# Test comparativo:
python manage.py test codigo.test_detector_ia.CodigoComparativoTestCase.test_comparar_estilos_codigo


# ============================================================================
# EJECUTAR EJEMPLOS PRÁCTICOS (INTERACTIVO)
# ============================================================================

# Iniciar shell de Django:
python manage.py shell

# Dentro del shell, ejecutar:
"""
from codigo.test_ejemplos_practicos import ejecutar_ejemplos
ejecutar_ejemplos()
"""

# O probar código personalizado:
"""
from codigo.test_ejemplos_practicos import test_codigo_personalizado

mi_codigo = '''
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
'''

test_codigo_personalizado(mi_codigo)
"""

# Comparar dos códigos:
"""
from codigo.test_ejemplos_practicos import comparar_codigos

codigo_humano = "def f(x): return x*2"

codigo_ia = '''
def multiply_by_two(value: int) -> int:
    \"\"\"Multiply a value by two.\"\"\"
    return value * 2
'''

comparar_codigos(codigo_humano, codigo_ia, "Código Humano", "Código IA")
"""

# Analizar un archivo:
"""
from codigo.test_ejemplos_practicos import test_archivo
test_archivo('ruta/a/tu/archivo.py')
"""


# ============================================================================
# EJECUTAR TESTS CON VERBOSITY
# ============================================================================

# Modo verbose (muestra más detalles):
python manage.py test codigo.test_detector_ia --verbosity=2

# Modo muy verbose:
python manage.py test codigo.test_detector_ia --verbosity=3

# Modo silencioso:
python manage.py test codigo.test_detector_ia --verbosity=0


# ============================================================================
# EJECUTAR TESTS CON COBERTURA
# ============================================================================

# Instalar coverage:
pip install coverage

# Ejecutar con coverage:
coverage run --source='codigo' manage.py test codigo.test_detector_ia

# Ver reporte:
coverage report

# Generar reporte HTML:
coverage html
# Abrir htmlcov/index.html en el navegador


# ============================================================================
# EJECUTAR TESTS Y GUARDAR RESULTADOS
# ============================================================================

# Windows PowerShell:
python manage.py test codigo.test_detector_ia > test_results.txt 2>&1

# Linux/Mac:
python3 manage.py test codigo.test_detector_ia > test_results.txt 2>&1


# ============================================================================
# TESTS RÁPIDOS DE API (CURL)
# ============================================================================

# Subir archivo de código:
curl -X POST http://localhost:8000/api/codigo/subir/ \
  -F "archivo=@test.py"

# Ver historial:
curl http://localhost:8000/api/codigo/historial/

# Ver detalle de análisis:
curl http://localhost:8000/api/codigo/analisis/1/

# Comparar dos análisis:
curl "http://localhost:8000/api/codigo/historial/comparar/?id1=1&id2=2"


# ============================================================================
# EJECUTAR TESTS DE INTEGRACIÓN
# ============================================================================

# Crear archivo de prueba:
"""
# test_sample.py
def fibonacci(n: int) -> int:
    \"\"\"Calculate Fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""

# Subir y analizar con curl:
curl -X POST http://localhost:8000/api/codigo/subir/ \
  -F "archivo=@test_sample.py"


# ============================================================================
# DEBUGGING Y TROUBLESHOOTING
# ============================================================================

# Ver logs del detector:
python manage.py shell
"""
from codigo.modelos.production_code_detector import get_detector
detector = get_detector()
print(f"Tipo: {type(detector).__name__}")
print(f"Versión: {getattr(detector, 'version', 'N/A')}")
"""

# Verificar que el modelo está cargado:
"""
from codigo.modelos.detector_hf import CodeDetectorHF
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
modelo_path = os.path.join(BASE, "code_detection-model-complete")
print(f"Ruta del modelo: {modelo_path}")
print(f"Existe: {os.path.exists(modelo_path)}")
"""

# Test simple del detector:
"""
from codigo.modelos.production_code_detector import get_detector

detector = get_detector()
resultado = detector.analizar("def test(): pass")
print(resultado)
"""


# ============================================================================
# VARIABLES DE ENTORNO ÚTILES
# ============================================================================

# Forzar uso del detector fallback:
# Windows PowerShell:
$env:CODE_DETECTOR_FORCE_FALLBACK="1"
python manage.py test codigo.test_detector_ia

# Linux/Mac:
export CODE_DETECTOR_FORCE_FALLBACK=1
python3 manage.py test codigo.test_detector_ia

# Especificar implementación:
# Windows:
$env:CODE_DETECTOR_IMPL="hf"  # o "pkl"

# Linux/Mac:
export CODE_DETECTOR_IMPL=hf


# ============================================================================
# COMANDOS DE MANTENIMIENTO
# ============================================================================

# Limpiar archivos __pycache__:
# Windows:
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force

# Linux/Mac:
find . -type d -name "__pycache__" -exec rm -rf {} +

# Limpiar base de datos de pruebas:
python manage.py flush --no-input

# Recrear migraciones:
python manage.py makemigrations codigo
python manage.py migrate


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

# Test de rendimiento:
"""
import time
from codigo.modelos.production_code_detector import get_detector

detector = get_detector()
codigo = "def test(): return True"

inicio = time.time()
for i in range(100):
    detector.analizar(codigo)
fin = time.time()

print(f"Tiempo promedio: {(fin-inicio)/100:.4f} segundos")
"""


# ============================================================================
# CI/CD COMMANDS
# ============================================================================

# Ejecutar todos los tests (para CI):
python manage.py test --parallel --verbosity=2

# Ejecutar con timeout:
timeout 300 python manage.py test codigo.test_detector_ia


# ============================================================================
# NOTAS IMPORTANTES
# ============================================================================

"""
1. Asegúrate de que el modelo esté en la ruta correcta:
   Backend/codigo/code_detection-model-complete/

2. Si el modelo no se carga, el sistema usará un detector fallback
   que siempre retorna confianza 0.

3. Los tests requieren que Django esté configurado correctamente.

4. Para tests en producción, usa CODE_DETECTOR_FORCE_FALLBACK=1

5. El detector se cachea globalmente para mejorar rendimiento.
"""
