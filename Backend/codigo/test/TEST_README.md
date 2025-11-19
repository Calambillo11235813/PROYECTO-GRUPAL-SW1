# 🧪 Tests del Detector de Código IA vs Humano

Este directorio contiene una suite completa de tests para verificar el detector de código generado por IA.

## 📁 Archivos de Test

### `test_detector_ia.py`
Suite completa de tests unitarios que incluye:

- **Tests del Detector**: Verifican funcionamiento básico del detector
- **Tests de Código Humano**: Validan detección de código escrito por personas
- **Tests de Código IA**: Validan detección de código generado por IA
- **Tests de Análisis Sintáctico**: Verifican cálculo de complejidad, AST, etc.
- **Tests de Marcado de Líneas**: Validan identificación de líneas sospechosas
- **Tests Comparativos**: Comparan diferentes estilos de código
- **Tests de Integración**: Prueban endpoints de la API
- **Tests de Casos Edge**: Validan manejo de casos especiales
- **Tests de Performance**: Verifican rendimiento del sistema

### `test_ejemplos_practicos.py`
Script interactivo con ejemplos prácticos que permite:

- Ejecutar análisis con ejemplos predefinidos
- Probar código personalizado
- Comparar dos fragmentos de código
- Analizar archivos completos
- Visualizar resultados con colores

### `COMANDOS_TEST.py`
Documentación de comandos útiles para ejecutar tests.

---

## 🚀 Cómo Ejecutar los Tests

### 1️⃣ Tests Unitarios (Recomendado para desarrollo)

```bash
# Ejecutar todos los tests
python manage.py test codigo.test_detector_ia

# Con más detalle (verbose)
python manage.py test codigo.test_detector_ia --verbosity=2

# Test específico
python manage.py test codigo.test_detector_ia.CodigoIATestCase.test_detector_disponible
```

### 2️⃣ Ejemplos Prácticos (Recomendado para demostración)

```bash
# Iniciar shell de Django
python manage.py shell
```

Dentro del shell:

```python
# Ejecutar todos los ejemplos
from codigo.test_ejemplos_practicos import ejecutar_ejemplos
ejecutar_ejemplos()

# Probar código personalizado
from codigo.test_ejemplos_practicos import test_codigo_personalizado
mi_codigo = '''
def saludar(nombre):
    return f"Hola {nombre}"
'''
test_codigo_personalizado(mi_codigo)

# Comparar dos códigos
from codigo.test_ejemplos_practicos import comparar_codigos
codigo1 = "def f(x): return x*2"
codigo2 = "def multiply_by_two(value: int) -> int: return value * 2"
comparar_codigos(codigo1, codigo2)
```

---

## 📊 Casos de Test Incluidos

### ✅ Código Humano (Esperado: Detectar como HUMANO)

```python
# Código minimalista
def fib(n):
    if n<2:return n
    return fib(n-1)+fib(n-2)

# Script pragmático
x = [1,2,3,4,5]
y = sum(x)
print(y)
```

### 🤖 Código IA (Esperado: Detectar como IA)

```python
# Código con documentación exhaustiva
def calculate_fibonacci_sequence(n: int) -> list:
    """
    Calculate the Fibonacci sequence up to the nth term.
    
    Args:
        n (int): The number of terms to generate
        
    Returns:
        list: A list containing the Fibonacci sequence
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    # ... más código
```

---

## 🎯 Tests Principales

### Test 1: Detector Disponible
```python
def test_detector_disponible(self):
    """Verificar que el detector está disponible"""
    self.assertIsNotNone(self.detector)
    self.assertTrue(hasattr(self.detector, 'analizar'))
```

### Test 2: Código Simple Humano
```python
def test_codigo_simple_humano(self):
    """Test con código simple escrito por humano"""
    codigo_humano = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
    resultado = self.detector.analizar(codigo_humano)
    self.assertIn('is_ai_generated', resultado)
    self.assertIn('confidence', resultado)
```

### Test 3: Código Generado por IA
```python
def test_codigo_ia_generado(self):
    """Test con código típicamente generado por IA"""
    # Código con type hints, docstrings detallados, etc.
    resultado = self.detector.analizar(codigo_ia)
    self.assertIn('is_ai_generated', resultado)
```

### Test 4: Análisis Sintáctico
```python
def test_analisis_codigo_simple(self):
    """Test de análisis sintáctico"""
    analisis = analizar_archivo_codigo(temp_path)
    self.assertIn('complejidad', analisis)
    self.assertIn('patrones_control', analisis)
```

### Test 5: Marcado de Líneas Sospechosas
```python
def test_marcado_lineas_codigo_limpio(self):
    """Test de marcado con código limpio"""
    lineas, bloques = marcar_lineas_sospechosas(codigo)
    self.assertIsInstance(lineas, list)
    self.assertIsInstance(bloques, list)
```

---

## 📈 Resultados Esperados

Cuando ejecutas los tests, deberías ver algo como:

```
test_codigo_ia_generado (codigo.test_detector_ia.CodigoIATestCase) ... ok
test_codigo_simple_humano (codigo.test_detector_ia.CodigoIATestCase) ... ok
test_detector_disponible (codigo.test_detector_ia.CodigoIATestCase) ... ok
test_analisis_codigo_simple (codigo.test_detector_ia.CodigoIATestCase) ... ok
test_marcado_lineas_codigo_limpio (codigo.test_detector_ia.CodigoIATestCase) ... ok

----------------------------------------------------------------------
Ran 25 tests in 12.345s

OK
```

---

## 🔧 Configuración

### Variables de Entorno

```bash
# Forzar detector fallback (para tests sin modelo)
export CODE_DETECTOR_FORCE_FALLBACK=1

# Especificar implementación
export CODE_DETECTOR_IMPL=hf  # o 'pkl' o 'auto'
```

### Requisitos

- Django configurado
- Modelo de detección en `codigo/code_detection-model-complete/`
- Python 3.8+
- Dependencias instaladas: `transformers`, `torch`, `radon`

---

## 🐛 Troubleshooting

### Problema: "Modelo no encontrado"
```bash
# Verificar ruta del modelo
python manage.py shell
>>> import os
>>> from codigo.modelos.production_code_detector import get_detector
>>> detector = get_detector()
>>> print(type(detector).__name__)
```

### Problema: Tests muy lentos
```bash
# Usar detector fallback para tests
export CODE_DETECTOR_FORCE_FALLBACK=1
python manage.py test codigo.test_detector_ia
```

### Problema: Errores de encoding
Los tests manejan automáticamente archivos UTF-8. Si tienes problemas:
```python
# En tu código de test
with open(archivo, 'r', encoding='utf-8') as f:
    contenido = f.read()
```

---

## 📝 Agregar Nuevos Tests

Para agregar un nuevo test:

```python
class MiNuevoTestCase(TestCase):
    def setUp(self):
        self.detector = get_detector()
    
    def test_mi_caso(self):
        """Descripción del test"""
        codigo = "..."
        resultado = self.detector.analizar(codigo)
        self.assertEqual(resultado['is_ai_generated'], True)
```

---

## 🎨 Visualización de Resultados

Los ejemplos prácticos incluyen visualización con colores:

- 🤖 **ROJO**: Código detectado como IA
- 👨‍💻 **VERDE**: Código detectado como Humano
- **Confianza**: Porcentaje de certeza del modelo

Ejemplo de salida:

```
================================================================================
  TEST 1/6: Ejemplo 1: Código minimalista (típico humano)
================================================================================

👨‍💻 CÓDIGO ESCRITO POR HUMANO
├─ Confianza: 78.50%
├─ Método: codebert
├─ Probabilidad IA: 21.50%
└─ Probabilidad Humano: 78.50%

📄 Preview del código:
--------------------------------------------------------------------------------
def fib(n):
    if n<2:return n
    return fib(n-1)+fib(n-2)
--------------------------------------------------------------------------------
```

---

## 🔬 Tests de Cobertura

```bash
# Instalar coverage
pip install coverage

# Ejecutar tests con coverage
coverage run --source='codigo' manage.py test codigo.test_detector_ia

# Ver reporte
coverage report

# Generar HTML
coverage html
# Abrir: htmlcov/index.html
```

---

## 📚 Documentación Adicional

- **Modelo**: Ver `code_detection-model-complete/README.md`
- **API**: Ver `../ARCHITECTURE.md`
- **Guía del Usuario**: Ver `../README.md`

---

## 🤝 Contribuir

Para contribuir con nuevos tests:

1. Añade el test en `test_detector_ia.py`
2. Documenta qué valida el test
3. Asegúrate de que pasa: `python manage.py test codigo.test_detector_ia`
4. Haz commit con mensaje descriptivo

---

## ✅ Checklist de Tests

- [ ] Detector se carga correctamente
- [ ] Detecta código humano simple
- [ ] Detecta código IA con docstrings
- [ ] Análisis sintáctico funciona
- [ ] Marcado de líneas funciona
- [ ] Maneja casos edge (vacío, largo, caracteres especiales)
- [ ] API endpoints responden correctamente
- [ ] Performance aceptable (< 5s para código pequeño)

---

**Última actualización**: 19 de Noviembre de 2025
