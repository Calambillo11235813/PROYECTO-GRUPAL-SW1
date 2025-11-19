"""
Ejemplos de código para usar en tests del detector IA vs Humano

Este archivo contiene fragmentos de código categorizados como:
- Código típicamente escrito por humanos
- Código típicamente generado por IA
"""

# ==============================================================================
# CÓDIGO TÍPICAMENTE HUMANO
# ==============================================================================

CODIGO_HUMANO_MINIMALISTA = """
def fib(n):
    if n<2:return n
    return fib(n-1)+fib(n-2)
"""

CODIGO_HUMANO_PRAGMATICO = """
# quick script to process data
import json
data = json.load(open('data.json'))
results = [x['value'] for x in data if x['active']]
print(results)
"""

CODIGO_HUMANO_COMENTARIOS_SIMPLES = """
def calc_total(items):
    # sum all prices
    total = 0
    for item in items:
        total += item.price
    return total
"""

CODIGO_HUMANO_VARIABLES_CORTAS = """
def process(x):
    y = x * 2
    z = y + 10
    return z

res = process(5)
print(res)
"""

CODIGO_HUMANO_SIN_TIPOS = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

CODIGO_HUMANO_ESTILO_COMPACTO = """
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def dist(self):
        return (self.x**2+self.y**2)**0.5
"""


# ==============================================================================
# CÓDIGO TÍPICAMENTE GENERADO POR IA
# ==============================================================================

CODIGO_IA_DOCUMENTADO = """
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

CODIGO_IA_TYPE_HINTS = """
from typing import List, Optional, Union

def process_data(
    data: List[dict],
    filter_key: str,
    filter_value: Union[str, int],
    default: Optional[str] = None
) -> List[dict]:
    \"\"\"
    Process and filter a list of dictionaries based on a key-value pair.
    
    Args:
        data: List of dictionaries to process
        filter_key: Key to filter by
        filter_value: Value to match
        default: Default value if key not found
        
    Returns:
        Filtered list of dictionaries
    \"\"\"
    result = []
    
    for item in data:
        if item.get(filter_key, default) == filter_value:
            result.append(item)
    
    return result
"""

CODIGO_IA_MANEJO_ERRORES_COMPLETO = """
def safe_divide(numerator: float, denominator: float) -> Optional[float]:
    \"\"\"
    Safely divide two numbers with comprehensive error handling.
    
    Args:
        numerator: The number to be divided
        denominator: The number to divide by
        
    Returns:
        The result of the division, or None if division is not possible
    \"\"\"
    try:
        # Validate input types
        if not isinstance(numerator, (int, float)):
            raise TypeError("Numerator must be a number")
        
        if not isinstance(denominator, (int, float)):
            raise TypeError("Denominator must be a number")
        
        # Check for zero division
        if denominator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        # Perform the division
        result = numerator / denominator
        
        return result
        
    except TypeError as e:
        print(f"Type error occurred: {e}")
        return None
        
    except ZeroDivisionError as e:
        print(f"Division error occurred: {e}")
        return None
        
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return None
"""

CODIGO_IA_CLASE_COMPLETA = """
from dataclasses import dataclass
from typing import ClassVar, List
from datetime import datetime

@dataclass
class Employee:
    \"\"\"
    Represents an employee in the organization.
    
    Attributes:
        id: Unique identifier for the employee
        name: Full name of the employee
        email: Email address of the employee
        department: Department where the employee works
        hire_date: Date when the employee was hired
    \"\"\"
    
    # Class variable
    company_name: ClassVar[str] = "Tech Corp"
    
    # Instance variables
    id: int
    name: str
    email: str
    department: str
    hire_date: datetime
    
    def __post_init__(self) -> None:
        \"\"\"Validate employee data after initialization.\"\"\"
        if not self.validate_email():
            raise ValueError(f"Invalid email address: {self.email}")
    
    def validate_email(self) -> bool:
        \"\"\"
        Validate if the email address is in correct format.
        
        Returns:
            bool: True if email is valid, False otherwise
        \"\"\"
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None
    
    def years_of_service(self) -> int:
        \"\"\"
        Calculate the number of years the employee has been working.
        
        Returns:
            int: Number of complete years of service
        \"\"\"
        today = datetime.now()
        delta = today - self.hire_date
        years = delta.days // 365
        return years
    
    def get_info(self) -> dict:
        \"\"\"
        Get employee information as a dictionary.
        
        Returns:
            dict: Dictionary containing employee information
        \"\"\"
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "hire_date": self.hire_date.isoformat(),
            "years_of_service": self.years_of_service()
        }
"""

CODIGO_IA_COMENTARIOS_EXCESIVOS = """
# Import the math library for mathematical operations
import math

# Define a function to calculate the area of a circle
def calculate_circle_area(radius: float) -> float:
    \"\"\"
    Calculate the area of a circle given its radius.
    
    This function uses the mathematical formula: area = π * r²
    
    Args:
        radius: The radius of the circle
        
    Returns:
        The area of the circle
    \"\"\"
    # First, check if the radius is valid
    if radius < 0:
        # If radius is negative, raise an error
        raise ValueError("Radius cannot be negative")
    
    # Use the mathematical constant pi from the math library
    pi = math.pi
    
    # Calculate the area using the formula: area = π * r²
    # Square the radius first
    radius_squared = radius ** 2
    
    # Multiply by pi to get the area
    area = pi * radius_squared
    
    # Return the calculated area
    return area

# Test the function with a sample radius
test_radius = 5.0

# Call the function and store the result
result = calculate_circle_area(test_radius)

# Print the result to the console
print(f"The area of a circle with radius {test_radius} is {result}")
"""


# ==============================================================================
# CÓDIGO AMBIGUO (PUEDE SER HUMANO O IA)
# ==============================================================================

CODIGO_AMBIGUO_1 = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""

CODIGO_AMBIGUO_2 = """
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
"""


# ==============================================================================
# CASOS ESPECIALES
# ==============================================================================

CODIGO_VACIO = ""

CODIGO_SOLO_COMENTARIOS = """
# This is just a comment
# Another comment
# Yet another comment
"""

CODIGO_MUY_CORTO = "x = 1"

CODIGO_UNA_LINEA = "def f(x): return x * 2"

CODIGO_CARACTERES_ESPECIALES = """
# Código con ñ, tildes y símbolos especiales
def función_española(parámetro):
    \"\"\"Función con caracteres españoles\"\"\"
    resultado = f"Hola {parámetro} 🚀"
    return resultado
"""


# ==============================================================================
# DICCIONARIO PARA ACCESO FÁCIL
# ==============================================================================

EJEMPLOS = {
    # Humanos
    'humano_minimalista': CODIGO_HUMANO_MINIMALISTA,
    'humano_pragmatico': CODIGO_HUMANO_PRAGMATICO,
    'humano_simple': CODIGO_HUMANO_COMENTARIOS_SIMPLES,
    'humano_corto': CODIGO_HUMANO_VARIABLES_CORTAS,
    'humano_sin_tipos': CODIGO_HUMANO_SIN_TIPOS,
    'humano_compacto': CODIGO_HUMANO_ESTILO_COMPACTO,
    
    # IA
    'ia_documentado': CODIGO_IA_DOCUMENTADO,
    'ia_type_hints': CODIGO_IA_TYPE_HINTS,
    'ia_errores': CODIGO_IA_MANEJO_ERRORES_COMPLETO,
    'ia_clase': CODIGO_IA_CLASE_COMPLETA,
    'ia_comentarios': CODIGO_IA_COMENTARIOS_EXCESIVOS,
    
    # Ambiguos
    'ambiguo_quicksort': CODIGO_AMBIGUO_1,
    'ambiguo_calculator': CODIGO_AMBIGUO_2,
    
    # Especiales
    'vacio': CODIGO_VACIO,
    'solo_comentarios': CODIGO_SOLO_COMENTARIOS,
    'muy_corto': CODIGO_MUY_CORTO,
    'una_linea': CODIGO_UNA_LINEA,
    'caracteres_especiales': CODIGO_CARACTERES_ESPECIALES,
}


def obtener_ejemplo(nombre):
    """
    Obtiene un ejemplo de código por nombre.
    
    Args:
        nombre: Nombre del ejemplo (ver EJEMPLOS.keys())
        
    Returns:
        str: Código del ejemplo
    """
    return EJEMPLOS.get(nombre, "")


def listar_ejemplos():
    """Lista todos los ejemplos disponibles."""
    print("Ejemplos disponibles:")
    print("\nCÓDIGO HUMANO:")
    for key in EJEMPLOS.keys():
        if key.startswith('humano'):
            print(f"  - {key}")
    
    print("\nCÓDIGO IA:")
    for key in EJEMPLOS.keys():
        if key.startswith('ia'):
            print(f"  - {key}")
    
    print("\nCÓDIGO AMBIGUO:")
    for key in EJEMPLOS.keys():
        if key.startswith('ambiguo'):
            print(f"  - {key}")
    
    print("\nCASOS ESPECIALES:")
    for key in EJEMPLOS.keys():
        if not any(key.startswith(p) for p in ['humano', 'ia', 'ambiguo']):
            print(f"  - {key}")


if __name__ == '__main__':
    listar_ejemplos()
