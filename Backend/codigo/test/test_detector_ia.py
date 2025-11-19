"""
Tests para verificar la detección de código generado por IA vs código humano.

Este módulo contiene tests unitarios y de integración para validar:
- Detección de código generado por IA
- Detección de código escrito por humanos
- Análisis de patrones sintácticos
- Marcado de líneas sospechosas
- Generación de reportes
"""

import os
import tempfile
import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from codigo.models import AnalisisCodigo
from codigo.modelos.production_code_detector import get_detector
from codigo.utils.analizador_codigo import analizar_archivo_codigo
from codigo.utils.marcador_ia import marcar_lineas_sospechosas
from codigo.utils.detectar_lenguaje import detectar_lenguaje

User = get_user_model()


class CodigoIATestCase(TestCase):
    """Tests básicos para detección de código IA"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.detector = get_detector()
        self.client = Client()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    # ====================
    # TESTS DEL DETECTOR
    # ====================

    def test_detector_disponible(self):
        """Verificar que el detector está disponible"""
        self.assertIsNotNone(self.detector)
        self.assertTrue(hasattr(self.detector, 'analizar'))

    def test_codigo_simple_humano(self):
        """Test con código simple escrito por humano"""
        codigo_humano = """
# Función simple para calcular factorial
def factorial(n):
    # Caso base
    if n <= 1:
        return 1
    # Caso recursivo
    result = n * factorial(n - 1)
    return result

# Probar la función
print(factorial(5))
"""
        resultado = self.detector.analizar(codigo_humano)
        
        self.assertIn('is_ai_generated', resultado)
        self.assertIn('confidence', resultado)
        self.assertIn('method_used', resultado)
        
        # Verificar que la confianza es un número entre 0 y 1
        self.assertGreaterEqual(resultado['confidence'], 0.0)
        self.assertLessEqual(resultado['confidence'], 1.0)

    def test_codigo_ia_generado(self):
        """Test con código típicamente generado por IA"""
        codigo_ia = """
def calculate_fibonacci_sequence(n: int) -> list:
    \"\"\"
    Calculate the Fibonacci sequence up to the nth term.
    
    Args:
        n (int): The number of terms to generate
        
    Returns:
        list: A list containing the Fibonacci sequence
        
    Raises:
        ValueError: If n is negative
    \"\"\"
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    if n == 0:
        return []
    
    if n == 1:
        return [0]
    
    fibonacci_sequence = [0, 1]
    
    for i in range(2, n):
        next_value = fibonacci_sequence[i - 1] + fibonacci_sequence[i - 2]
        fibonacci_sequence.append(next_value)
    
    return fibonacci_sequence


def main():
    \"\"\"Main function to demonstrate Fibonacci sequence generation.\"\"\"
    try:
        result = calculate_fibonacci_sequence(10)
        print(f"Fibonacci sequence: {result}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
"""
        resultado = self.detector.analizar(codigo_ia)
        
        self.assertIn('is_ai_generated', resultado)
        self.assertIn('confidence', resultado)
        
        # Este código tiene características de IA:
        # - Docstrings detallados
        # - Type hints
        # - Manejo de excepciones
        # - Estructura muy clara

    def test_codigo_vacio(self):
        """Test con código vacío"""
        resultado = self.detector.analizar("")
        
        self.assertIn('is_ai_generated', resultado)
        self.assertIn('confidence', resultado)

    def test_codigo_con_comentarios_excesivos(self):
        """Test con código que tiene muchos comentarios (típico de IA)"""
        codigo_comentado = """
# Import necessary libraries
import math

# Define a function to calculate the area of a circle
def calculate_circle_area(radius: float) -> float:
    \"\"\"
    Calculate the area of a circle given its radius.
    
    Args:
        radius: The radius of the circle
        
    Returns:
        The area of the circle
    \"\"\"
    # Check if radius is valid
    if radius < 0:
        # Raise an error for negative radius
        raise ValueError("Radius cannot be negative")
    
    # Calculate the area using the formula: area = π * r²
    area = math.pi * radius ** 2
    
    # Return the calculated area
    return area

# Test the function
result = calculate_circle_area(5)
# Print the result
print(f"Area: {result}")
"""
        resultado = self.detector.analizar(codigo_comentado)
        
        self.assertIn('is_ai_generated', resultado)
        self.assertIsInstance(resultado['confidence'], (int, float))

    # ====================
    # TESTS DE ANÁLISIS SINTÁCTICO
    # ====================

    def test_analisis_codigo_simple(self):
        """Test de análisis sintáctico con código simple"""
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf8') as f:
            f.write("""
def suma(a, b):
    return a + b

x = suma(1, 2)
""")
            temp_path = f.name
        
        try:
            analisis = analizar_archivo_codigo(temp_path)
            
            self.assertIn('ast', analisis)
            self.assertIn('complejidad', analisis)
            self.assertIn('variabilidad', analisis)
            self.assertIn('patrones_control', analisis)
            self.assertIn('predict', analisis)
            
            # Verificar que la complejidad es razonable
            self.assertGreaterEqual(analisis['complejidad'], 0)
            
        finally:
            os.unlink(temp_path)

    def test_analisis_codigo_complejo(self):
        """Test de análisis con código más complejo"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf8') as f:
            f.write("""
def proceso_complejo(datos):
    resultado = []
    for item in datos:
        if item > 0:
            if item % 2 == 0:
                resultado.append(item * 2)
            else:
                resultado.append(item * 3)
        else:
            resultado.append(0)
    return resultado

class MiClase:
    def __init__(self):
        self.valor = 0
    
    def incrementar(self):
        self.valor += 1
        
    def obtener(self):
        return self.valor
""")
            temp_path = f.name
        
        try:
            analisis = analizar_archivo_codigo(temp_path)
            
            # Código más complejo debe tener mayor complejidad ciclomática
            self.assertGreater(analisis['complejidad'], 0)
            
            # Debe detectar patrones de control
            self.assertIn('ifs', analisis['patrones_control'])
            self.assertIn('loops', analisis['patrones_control'])
            
        finally:
            os.unlink(temp_path)

    # ====================
    # TESTS DE MARCADO DE LÍNEAS
    # ====================

    def test_marcado_lineas_codigo_limpio(self):
        """Test de marcado con código limpio (humano)"""
        codigo = """
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b
"""
        lineas, bloques = marcar_lineas_sospechosas(codigo, umbral=0.80)
        
        self.assertIsInstance(lineas, list)
        self.assertIsInstance(bloques, list)

    def test_marcado_lineas_codigo_sospechoso(self):
        """Test de marcado con código potencialmente generado por IA"""
        codigo = """
def calculate_fibonacci(n: int) -> int:
    \"\"\"Calculate the nth Fibonacci number using recursion.\"\"\"
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
"""
        lineas, bloques = marcar_lineas_sospechosas(codigo, umbral=0.50)
        
        self.assertIsInstance(lineas, list)
        self.assertIsInstance(bloques, list)
        
        # Verificar estructura de bloques
        for bloque in bloques:
            self.assertIn('inicio', bloque)
            self.assertIn('fin', bloque)
            self.assertIn('score', bloque)

    # ====================
    # TESTS DE DETECCIÓN DE LENGUAJE
    # ====================

    def test_detectar_lenguaje_python(self):
        """Test de detección de lenguaje Python"""
        codigo_python = "def test(): pass"
        lenguaje = detectar_lenguaje("test.py", codigo_python)
        self.assertEqual(lenguaje, "python")

    def test_detectar_lenguaje_javascript(self):
        """Test de detección de lenguaje JavaScript"""
        codigo_js = "function test() { return true; }"
        lenguaje = detectar_lenguaje("test.js", codigo_js)
        self.assertEqual(lenguaje, "javascript")

    def test_detectar_lenguaje_java(self):
        """Test de detección de lenguaje Java"""
        codigo_java = "public class Test { }"
        lenguaje = detectar_lenguaje("Test.java", codigo_java)
        self.assertEqual(lenguaje, "java")

    # ====================
    # TESTS DE INTEGRACIÓN (API)
    # ====================

    def test_subir_codigo_python(self):
        """Test de subida de archivo Python"""
        codigo = b"""
def test_function():
    return "Hello World"

print(test_function())
"""
        archivo = SimpleUploadedFile("test.py", codigo, content_type="text/x-python")
        
        response = self.client.post('/api/codigo/subir/', {
            'archivo': archivo
        })
        
        # Debe retornar 200 o 201
        self.assertIn(response.status_code, [200, 201])
        
        if response.status_code in [200, 201]:
            data = response.json()
            self.assertIn('id', data)
            self.assertIn('ia_es_generado', data)
            self.assertIn('ia_confianza', data)

    def test_historial_analisis(self):
        """Test de obtención del historial"""
        response = self.client.get('/api/codigo/historial/')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, (list, dict))

    # ====================
    # TESTS DE CASOS EDGE
    # ====================

    def test_codigo_con_caracteres_especiales(self):
        """Test con código que contiene caracteres especiales"""
        codigo = """
# Código con ñ, tildes y caracteres especiales
def función_española(parámetro):
    \"\"\"Función con caracteres españoles\"\"\"
    return f"Hola {parámetro}"

# Emojis y símbolos
resultado = función_española("mundo") + " 🚀"
print(resultado)
"""
        resultado = self.detector.analizar(codigo)
        self.assertIn('is_ai_generated', resultado)

    def test_codigo_muy_largo(self):
        """Test con código muy largo"""
        codigo = "\n".join([f"variable_{i} = {i}" for i in range(1000)])
        
        resultado = self.detector.analizar(codigo)
        self.assertIn('is_ai_generated', resultado)

    def test_codigo_con_multiples_lenguajes(self):
        """Test con código que mezcla comentarios en varios idiomas"""
        codigo = """
# English comment
def calculate(x):
    # Comentario en español
    # Commentaire en français
    return x * 2
"""
        resultado = self.detector.analizar(codigo)
        self.assertIn('is_ai_generated', resultado)

    # ====================
    # TESTS DE MODELOS
    # ====================

    def test_crear_analisis_modelo(self):
        """Test de creación de modelo AnalisisCodigo"""
        analisis = AnalisisCodigo.objects.create(
            nombre_archivo="test.py",
            lenguaje="python",
            ia_es_generado=True,
            ia_confianza=0.85,
            complejidad_ciclomatica=5.0
        )
        
        self.assertEqual(analisis.nombre_archivo, "test.py")
        self.assertEqual(analisis.lenguaje, "python")
        self.assertTrue(analisis.ia_es_generado)
        self.assertEqual(analisis.ia_confianza, 0.85)

    def test_filtrar_analisis_por_ia(self):
        """Test de filtrado de análisis generados por IA"""
        # Crear análisis de prueba
        AnalisisCodigo.objects.create(
            nombre_archivo="ia_code.py",
            ia_es_generado=True,
            ia_confianza=0.9
        )
        AnalisisCodigo.objects.create(
            nombre_archivo="human_code.py",
            ia_es_generado=False,
            ia_confianza=0.2
        )
        
        # Filtrar solo código IA
        ia_codes = AnalisisCodigo.objects.filter(ia_es_generado=True)
        self.assertGreaterEqual(ia_codes.count(), 1)
        
        # Filtrar solo código humano
        human_codes = AnalisisCodigo.objects.filter(ia_es_generado=False)
        self.assertGreaterEqual(human_codes.count(), 1)


class CodigoComparativoTestCase(TestCase):
    """Tests comparativos entre código IA y humano"""

    def setUp(self):
        self.detector = get_detector()

    def test_comparar_estilos_codigo(self):
        """Comparar diferentes estilos de código"""
        
        # Estilo 1: Código minimalista (típico humano)
        codigo_minimalista = """
def f(n):
    if n<2:return n
    return f(n-1)+f(n-2)
"""
        
        # Estilo 2: Código documentado (típico IA)
        codigo_documentado = """
def fibonacci(n: int) -> int:
    \"\"\"
    Calculate the nth Fibonacci number.
    
    Args:
        n: Position in the Fibonacci sequence
        
    Returns:
        The nth Fibonacci number
    \"\"\"
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""
        
        resultado_min = self.detector.analizar(codigo_minimalista)
        resultado_doc = self.detector.analizar(codigo_documentado)
        
        self.assertIn('confidence', resultado_min)
        self.assertIn('confidence', resultado_doc)
        
        # Ambos deben tener una confianza válida
        self.assertGreaterEqual(resultado_min['confidence'], 0.0)
        self.assertGreaterEqual(resultado_doc['confidence'], 0.0)

    def test_comparar_complejidades(self):
        """Comparar código simple vs complejo"""
        
        # Código simple
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf8') as f:
            f.write("x = 1 + 1")
            simple_path = f.name
        
        # Código complejo
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf8') as f:
            f.write("""
def complejo(n):
    for i in range(n):
        if i % 2 == 0:
            for j in range(i):
                if j % 3 == 0:
                    print(j)
""")
            complejo_path = f.name
        
        try:
            analisis_simple = analizar_archivo_codigo(simple_path)
            analisis_complejo = analizar_archivo_codigo(complejo_path)
            
            # El código complejo debe tener mayor complejidad
            self.assertGreater(
                analisis_complejo['complejidad'],
                analisis_simple['complejidad']
            )
            
        finally:
            os.unlink(simple_path)
            os.unlink(complejo_path)


class CodigoReporteTestCase(TestCase):
    """Tests para generación de reportes"""

    def test_estructura_reporte(self):
        """Verificar estructura del reporte de análisis"""
        # Crear un análisis completo
        analisis = AnalisisCodigo.objects.create(
            nombre_archivo="test.py",
            lenguaje="python",
            ia_es_generado=True,
            ia_confianza=0.87,
            ia_metodo="codebert",
            complejidad_ciclomatica=5.5,
            lineas_sospechosas=[1, 2, 3],
            bloques_sospechosos=[{"inicio": 1, "fin": 3, "score": 0.9}]
        )
        
        # Verificar que se creó correctamente
        self.assertIsNotNone(analisis.id)
        self.assertEqual(analisis.ia_confianza, 0.87)
        self.assertTrue(analisis.ia_es_generado)


# ====================
# SUITE DE TESTS DE RENDIMIENTO
# ====================

class CodigoPerformanceTestCase(TestCase):
    """Tests de rendimiento del detector"""

    def test_tiempo_analisis_rapido(self):
        """Verificar que el análisis es rápido para código pequeño"""
        import time
        
        codigo = "def test(): return True"
        
        inicio = time.time()
        get_detector().analizar(codigo)
        fin = time.time()
        
        # El análisis debe tomar menos de 5 segundos
        self.assertLess(fin - inicio, 5.0)

    def test_cache_detector(self):
        """Verificar que el detector se cachea correctamente"""
        detector1 = get_detector()
        detector2 = get_detector()
        
        # Deben ser la misma instancia
        self.assertIs(detector1, detector2)


# ====================
# RUNNER PERSONALIZADO
# ====================

def run_tests():
    """Función helper para ejecutar tests manualmente"""
    from django.test.runner import DiscoverRunner
    
    runner = DiscoverRunner(verbosity=2)
    failures = runner.run_tests(["codigo.test_detector_ia"])
    
    if failures:
        print(f"\n❌ {failures} tests fallaron")
    else:
        print("\n✅ Todos los tests pasaron exitosamente")
    
    return failures


if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
    django.setup()
    run_tests()
