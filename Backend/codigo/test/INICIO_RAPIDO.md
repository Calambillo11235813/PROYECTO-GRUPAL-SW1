# 🎯 GUÍA RÁPIDA: Tests del Detector de Código IA

## 📋 ¿Qué se creó?

He creado una suite completa de tests para verificar si el código está hecho por IA o por humanos:

### Archivos creados:

1. **`test_detector_ia.py`** - Suite completa de tests unitarios (25+ tests)
2. **`test_ejemplos_practicos.py`** - Tests interactivos con ejemplos visuales
3. **`run_tests.py`** - Script de menú interactivo para ejecutar tests
4. **`ejemplos_codigo.py`** - Base de datos de ejemplos de código
5. **`TEST_README.md`** - Documentación completa
6. **`COMANDOS_TEST.py`** - Referencia de comandos

---

## 🚀 INICIO RÁPIDO - 3 Formas de Ejecutar

### Opción 1: Menú Interactivo (MÁS FÁCIL) ⭐

```bash
cd Backend
python codigo/run_tests.py
```

Verás un menú como este:
```
╔══════════════════════════════════════════════════════════════╗
║     🧪 DETECTOR DE CÓDIGO IA vs HUMANO - SUITE DE TESTS     ║
╚══════════════════════════════════════════════════════════════╝

Selecciona una opción:

1. Ejecutar TODOS los tests unitarios
2. Ejecutar ejemplos prácticos (interactivo)
3. Probar código personalizado
4. Comparar dos códigos
5. Ejecutar tests específicos
6. Ver información del detector
0. Salir

Opción:
```

### Opción 2: Tests Unitarios (COMPLETO)

```bash
cd Backend
python manage.py test codigo.test_detector_ia --verbosity=2
```

Esto ejecutará ~25 tests que verifican:
- ✅ Detector funciona correctamente
- ✅ Detecta código humano
- ✅ Detecta código IA
- ✅ Análisis sintáctico
- ✅ Marcado de líneas sospechosas
- ✅ Casos especiales (vacío, largo, etc.)

### Opción 3: Ejemplos Prácticos (VISUAL)

```bash
cd Backend
python manage.py shell
```

Luego en el shell:
```python
from codigo.test_ejemplos_practicos import ejecutar_ejemplos
ejecutar_ejemplos()
```

Esto mostrará análisis de 6 ejemplos con resultados visuales en colores.

---

## 🎨 EJEMPLO DE SALIDA

Cuando ejecutas los ejemplos prácticos, verás algo como:

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

================================================================================
  TEST 2/6: Ejemplo 2: Código con documentación completa (típico IA)
================================================================================

🤖 CÓDIGO GENERADO POR IA
├─ Confianza: 92.30%
├─ Método: codebert
├─ Probabilidad IA: 92.30%
└─ Probabilidad Humano: 7.70%
```

---

## 💡 PROBAR TU PROPIO CÓDIGO

### Método 1: Desde el menú interactivo

```bash
python codigo/run_tests.py
# Selecciona opción 3
# Escribe tu código
# Escribe FIN en una línea sola
```

### Método 2: Desde shell de Django

```python
from codigo.test_ejemplos_practicos import test_codigo_personalizado

mi_codigo = '''
def saludar(nombre):
    return f"Hola {nombre}"
'''

test_codigo_personalizado(mi_codigo)
```

---

## ⚖️ COMPARAR DOS CÓDIGOS

```python
from codigo.test_ejemplos_practicos import comparar_codigos

codigo_humano = "def f(x): return x*2"

codigo_ia = '''
def multiply_by_two(value: int) -> int:
    """Multiply a value by two."""
    return value * 2
'''

comparar_codigos(codigo_humano, codigo_ia)
```

---

## 📊 TESTS INCLUIDOS

### Tests del Detector (Básicos)
- ✅ `test_detector_disponible` - Verifica que el detector está disponible
- ✅ `test_codigo_simple_humano` - Detecta código humano simple
- ✅ `test_codigo_ia_generado` - Detecta código con características de IA
- ✅ `test_codigo_vacio` - Maneja código vacío
- ✅ `test_codigo_con_comentarios_excesivos` - Detecta comentarios típicos de IA

### Tests de Análisis Sintáctico
- ✅ `test_analisis_codigo_simple` - Analiza complejidad ciclomática
- ✅ `test_analisis_codigo_complejo` - Detecta patrones de control
- ✅ `test_detectar_lenguaje_python` - Detecta lenguaje correctamente

### Tests de Marcado de Líneas
- ✅ `test_marcado_lineas_codigo_limpio` - Marca líneas sospechosas
- ✅ `test_marcado_lineas_codigo_sospechoso` - Identifica bloques IA

### Tests de Integración (API)
- ✅ `test_subir_codigo_python` - Sube archivo a la API
- ✅ `test_historial_analisis` - Obtiene historial de análisis

### Tests de Casos Edge
- ✅ `test_codigo_con_caracteres_especiales` - Maneja ñ, tildes, emojis
- ✅ `test_codigo_muy_largo` - Procesa código extenso
- ✅ `test_codigo_con_multiples_lenguajes` - Comentarios multiidioma

### Tests Comparativos
- ✅ `test_comparar_estilos_codigo` - Compara código minimalista vs documentado
- ✅ `test_comparar_complejidades` - Compara código simple vs complejo

### Tests de Performance
- ✅ `test_tiempo_analisis_rapido` - Verifica análisis < 5 segundos
- ✅ `test_cache_detector` - Verifica caché del detector

---

## 🎯 CASOS DE USO

### Caso 1: Desarrollador verifica su código
```bash
# Ejecutar menú y seleccionar opción 3
python codigo/run_tests.py
# > 3. Probar código personalizado
# > [Pegar tu código]
# > FIN
```

### Caso 2: Comparar código antes/después de refactoring
```python
from codigo.test_ejemplos_practicos import comparar_codigos

codigo_antes = "..."
codigo_despues = "..."

comparar_codigos(codigo_antes, codigo_despues, "Antes", "Después")
```

### Caso 3: Validar que los tests pasan (CI/CD)
```bash
python manage.py test codigo.test_detector_ia --verbosity=2
```

### Caso 4: Analizar archivo completo
```python
from codigo.test_ejemplos_practicos import test_archivo
test_archivo('mi_script.py')
```

---

## 🔍 CARACTERÍSTICAS DEL DETECTOR

El detector analiza varios aspectos del código:

### Código Típicamente HUMANO:
- ✅ Nombres de variables cortos (`x`, `y`, `i`)
- ✅ Sin type hints
- ✅ Comentarios mínimos o pragmáticos
- ✅ Código compacto/minimalista
- ✅ Estilo informal

### Código Típicamente IA:
- 🤖 Docstrings detallados con Args/Returns/Examples
- 🤖 Type hints en todo (`: int`, `-> str`)
- 🤖 Manejo exhaustivo de errores
- 🤖 Comentarios excesivos explicando lo obvio
- 🤖 Validaciones de tipos extensas
- 🤖 Nombres de funciones muy descriptivos
- 🤖 Código muy "limpio" y estructurado

---

## 🐛 TROUBLESHOOTING

### Error: "Modelo no encontrado"
```bash
# Verifica que el modelo esté en la ruta correcta
python manage.py shell
>>> import os
>>> from codigo.modelos.production_code_detector import get_detector
>>> detector = get_detector()
>>> print(type(detector).__name__)
```

Si ves `_DummyDetector`, el modelo no se cargó. Verifica:
- Que existe `Backend/codigo/code_detection-model-complete/`
- Que contiene `model.safetensors`

### Tests muy lentos
```bash
# Usa el detector fallback para tests rápidos
export CODE_DETECTOR_FORCE_FALLBACK=1  # Linux/Mac
$env:CODE_DETECTOR_FORCE_FALLBACK="1"  # Windows PowerShell

python manage.py test codigo.test_detector_ia
```

### Error de encoding
Los tests ya manejan UTF-8 automáticamente. Si persiste:
```python
with open(archivo, 'r', encoding='utf-8') as f:
    codigo = f.read()
```

---

## 📈 PRÓXIMOS PASOS

1. **Ejecuta los tests** para verificar que todo funciona:
   ```bash
   python codigo/run_tests.py
   ```

2. **Prueba con tu código** usando la opción 3 del menú

3. **Revisa ejemplos prácticos** con la opción 2

4. **Lee la documentación completa** en `TEST_README.md`

---

## 📚 ARCHIVOS DE REFERENCIA

- **`TEST_README.md`** - Documentación completa y detallada
- **`COMANDOS_TEST.py`** - Todos los comandos disponibles
- **`ejemplos_codigo.py`** - Base de datos de ejemplos
- **`test_detector_ia.py`** - Código fuente de los tests
- **`test_ejemplos_practicos.py`** - Tests interactivos

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] Tests unitarios pasan: `python manage.py test codigo.test_detector_ia`
- [ ] Menú interactivo funciona: `python codigo/run_tests.py`
- [ ] Ejemplos prácticos se ejecutan correctamente
- [ ] Puedes probar código personalizado
- [ ] Detector responde con confianza entre 0-100%
- [ ] Marcado de líneas funciona

---

## 🎓 RESUMEN

Has creado con éxito una suite completa de tests que incluye:

✅ **25+ tests unitarios** automatizados
✅ **6 ejemplos prácticos** con análisis visual
✅ **Menú interactivo** fácil de usar
✅ **Comparador de códigos** lado a lado
✅ **Base de ejemplos** categorizados
✅ **Documentación completa** y clara

**¡Todo listo para usar!** 🚀

Comienza con:
```bash
cd Backend
python codigo/run_tests.py
```

---

**Creado**: 19 de Noviembre de 2025  
**Versión**: 1.0.0  
**Tests**: 25+ casos  
**Ejemplos**: 15+ fragmentos de código
