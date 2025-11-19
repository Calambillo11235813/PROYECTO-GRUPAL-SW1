"""
Script para probar manualmente el detector de código IA vs Humano
con ejemplos prácticos y visualización de resultados.

Uso:
    python manage.py shell
    >>> from codigo.test_ejemplos_practicos import ejecutar_ejemplos
    >>> ejecutar_ejemplos()
"""

import os
import sys
from colorama import init, Fore, Style

# Inicializar colorama para colores en terminal
try:
    init(autoreset=True)
except:
    pass


def print_titulo(texto):
    """Imprime un título destacado"""
    print("\n" + "="*80)
    print(f"  {texto}")
    print("="*80 + "\n")


def print_resultado(resultado, codigo_preview=""):
    """Imprime el resultado del análisis de forma legible"""
    is_ia = resultado.get('is_ai_generated', False)
    confianza = resultado.get('confidence', 0.0)
    metodo = resultado.get('method_used', 'unknown')
    
    # Colores según el resultado
    if is_ia:
        color = Fore.RED if hasattr(Fore, 'RED') else ''
        etiqueta = "🤖 CÓDIGO GENERADO POR IA"
    else:
        color = Fore.GREEN if hasattr(Fore, 'GREEN') else ''
        etiqueta = "👨‍💻 CÓDIGO ESCRITO POR HUMANO"
    
    print(f"\n{color}{etiqueta}")
    print(f"├─ Confianza: {confianza*100:.2f}%")
    print(f"├─ Método: {metodo}")
    
    if 'ai_prob' in resultado and resultado['ai_prob'] is not None:
        print(f"├─ Probabilidad IA: {resultado['ai_prob']*100:.2f}%")
        print(f"└─ Probabilidad Humano: {resultado['human_prob']*100:.2f}%")
    
    if codigo_preview:
        print(f"\n📄 Preview del código:")
        print("-" * 80)
        print(codigo_preview[:300] + ("..." if len(codigo_preview) > 300 else ""))
        print("-" * 80)


def ejecutar_ejemplos():
    """Ejecuta una serie de ejemplos prácticos"""
    from codigo.modelos.production_code_detector import get_detector
    
    print_titulo("🧪 TEST DE DETECTOR DE CÓDIGO IA vs HUMANO")
    
    detector = get_detector()
    print(f"✓ Detector cargado: {type(detector).__name__}")
    print(f"  Versión: {getattr(detector, 'version', 'N/A')}")
    
    ejemplos = [
        {
            "nombre": "Ejemplo 1: Código minimalista (típico humano)",
            "codigo": """
def fib(n):
    if n<2:return n
    return fib(n-1)+fib(n-2)

print(fib(10))
"""
        },
        {
            "nombre": "Ejemplo 2: Código con documentación completa (típico IA)",
            "codigo": """
def calculate_fibonacci_sequence(n: int) -> list:
    \"\"\"
    Calculate the Fibonacci sequence up to the nth term.
    
    This function generates the Fibonacci sequence, where each number
    is the sum of the two preceding ones.
    
    Args:
        n (int): The number of terms to generate in the sequence
        
    Returns:
        list: A list containing the Fibonacci sequence up to n terms
        
    Raises:
        ValueError: If n is negative
        
    Example:
        >>> calculate_fibonacci_sequence(5)
        [0, 1, 1, 2, 3]
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
"""
        },
        {
            "nombre": "Ejemplo 3: Script rápido con variables cortas (humano)",
            "codigo": """
x = [1,2,3,4,5]
y = sum(x)
print(y)
"""
        },
        {
            "nombre": "Ejemplo 4: Clase con type hints y docstrings (IA)",
            "codigo": """
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class User:
    \"\"\"
    Represents a user in the system.
    
    Attributes:
        id: Unique identifier for the user
        name: Full name of the user
        email: Email address of the user
    \"\"\"
    id: int
    name: str
    email: str
    
    def validate_email(self) -> bool:
        \"\"\"
        Validate if the email address is in correct format.
        
        Returns:
            bool: True if email is valid, False otherwise
        \"\"\"
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None
"""
        },
        {
            "nombre": "Ejemplo 5: Script pragmático con comentarios básicos (humano)",
            "codigo": """
# cargar datos
import json
with open('data.json') as f:
    data = json.load(f)

# procesar
results = [item['value'] for item in data if item['active']]

# guardar
with open('output.json', 'w') as f:
    json.dump(results, f)
"""
        },
        {
            "nombre": "Ejemplo 6: Código con manejo exhaustivo de errores (IA)",
            "codigo": """
def safe_divide(numerator: float, denominator: float) -> Optional[float]:
    \"\"\"
    Safely divide two numbers with comprehensive error handling.
    
    Args:
        numerator: The number to be divided
        denominator: The number to divide by
        
    Returns:
        The result of the division, or None if division is not possible
        
    Example:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0)
        None
    \"\"\"
    try:
        if not isinstance(numerator, (int, float)):
            raise TypeError("Numerator must be a number")
        if not isinstance(denominator, (int, float)):
            raise TypeError("Denominator must be a number")
        if denominator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        result = numerator / denominator
        return result
        
    except TypeError as e:
        print(f"Type error: {e}")
        return None
    except ZeroDivisionError as e:
        print(f"Division error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
"""
        }
    ]
    
    resultados_resumen = []
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print_titulo(f"TEST {i}/{len(ejemplos)}: {ejemplo['nombre']}")
        
        try:
            resultado = detector.analizar(ejemplo['codigo'])
            print_resultado(resultado, ejemplo['codigo'])
            
            resultados_resumen.append({
                'nombre': ejemplo['nombre'],
                'is_ia': resultado.get('is_ai_generated', False),
                'confianza': resultado.get('confidence', 0.0)
            })
            
        except Exception as e:
            print(f"❌ Error al analizar: {str(e)}")
    
    # Resumen final
    print_titulo("📊 RESUMEN DE RESULTADOS")
    
    ia_detectados = sum(1 for r in resultados_resumen if r['is_ia'])
    humano_detectados = len(resultados_resumen) - ia_detectados
    
    print(f"Total de ejemplos analizados: {len(resultados_resumen)}")
    print(f"├─ Detectados como IA: {ia_detectados}")
    print(f"└─ Detectados como Humano: {humano_detectados}\n")
    
    print("Detalle por ejemplo:")
    for i, res in enumerate(resultados_resumen, 1):
        tipo = "🤖 IA" if res['is_ia'] else "👨‍💻 HUMANO"
        print(f"{i}. {tipo} ({res['confianza']*100:.1f}% confianza) - {res['nombre']}")
    
    print("\n" + "="*80)
    print("✅ Análisis completado")
    print("="*80 + "\n")


def test_codigo_personalizado(codigo_str):
    """
    Permite probar código personalizado
    
    Uso:
        >>> from codigo.test_ejemplos_practicos import test_codigo_personalizado
        >>> mi_codigo = '''
        ... def mi_funcion():
        ...     return "Hola"
        ... '''
        >>> test_codigo_personalizado(mi_codigo)
    """
    from codigo.modelos.production_code_detector import get_detector
    
    print_titulo("🔍 ANÁLISIS DE CÓDIGO PERSONALIZADO")
    
    detector = get_detector()
    resultado = detector.analizar(codigo_str)
    
    print_resultado(resultado, codigo_str)
    
    return resultado


def comparar_codigos(codigo1, codigo2, nombre1="Código 1", nombre2="Código 2"):
    """
    Compara dos fragmentos de código
    
    Uso:
        >>> from codigo.test_ejemplos_practicos import comparar_codigos
        >>> codigo_a = "def f(x): return x*2"
        >>> codigo_b = "def multiply_by_two(value: int) -> int: return value * 2"
        >>> comparar_codigos(codigo_a, codigo_b)
    """
    from codigo.modelos.production_code_detector import get_detector
    
    print_titulo(f"⚖️  COMPARACIÓN DE CÓDIGOS")
    
    detector = get_detector()
    
    print(f"\n📝 {nombre1}")
    print("-" * 80)
    print(codigo1)
    print("-" * 80)
    resultado1 = detector.analizar(codigo1)
    print_resultado(resultado1)
    
    print(f"\n📝 {nombre2}")
    print("-" * 80)
    print(codigo2)
    print("-" * 80)
    resultado2 = detector.analizar(codigo2)
    print_resultado(resultado2)
    
    # Comparación
    print("\n" + "="*80)
    print("COMPARACIÓN:")
    print("="*80)
    
    conf1 = resultado1.get('confidence', 0) * 100
    conf2 = resultado2.get('confidence', 0) * 100
    
    if resultado1.get('is_ai_generated') == resultado2.get('is_ai_generated'):
        print(f"✓ Ambos códigos clasificados como: {'IA' if resultado1.get('is_ai_generated') else 'HUMANO'}")
    else:
        print(f"✗ Clasificaciones diferentes:")
        print(f"  - {nombre1}: {'IA' if resultado1.get('is_ai_generated') else 'HUMANO'} ({conf1:.1f}%)")
        print(f"  - {nombre2}: {'IA' if resultado2.get('is_ai_generated') else 'HUMANO'} ({conf2:.1f}%)")
    
    print(f"\nDiferencia de confianza: {abs(conf1 - conf2):.2f}%")
    print("="*80 + "\n")


def test_archivo(ruta_archivo):
    """
    Analiza un archivo de código completo
    
    Uso:
        >>> from codigo.test_ejemplos_practicos import test_archivo
        >>> test_archivo('mi_script.py')
    """
    from codigo.modelos.production_code_detector import get_detector
    
    if not os.path.exists(ruta_archivo):
        print(f"❌ Error: El archivo '{ruta_archivo}' no existe")
        return
    
    print_titulo(f"📁 ANÁLISIS DE ARCHIVO: {os.path.basename(ruta_archivo)}")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        print(f"✓ Archivo leído exitosamente")
        print(f"  Tamaño: {len(codigo)} caracteres")
        print(f"  Líneas: {len(codigo.splitlines())}")
        
        detector = get_detector()
        resultado = detector.analizar(codigo)
        
        print_resultado(resultado, codigo)
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error al leer/analizar el archivo: {str(e)}")


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     🧪 DETECTOR DE CÓDIGO GENERADO POR IA vs HUMANO - EJEMPLOS PRÁCTICOS   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Para ejecutar estos tests, usa:

    python manage.py shell
    
Y luego ejecuta:

    >>> from codigo.test_ejemplos_practicos import ejecutar_ejemplos
    >>> ejecutar_ejemplos()

Otras funciones disponibles:

    - test_codigo_personalizado(codigo_str)
    - comparar_codigos(codigo1, codigo2)
    - test_archivo(ruta_archivo)

Ejemplo:
    >>> from codigo.test_ejemplos_practicos import test_codigo_personalizado
    >>> mi_codigo = '''
    ... def saludar(nombre):
    ...     return f"Hola {nombre}"
    ... '''
    >>> test_codigo_personalizado(mi_codigo)

""")
