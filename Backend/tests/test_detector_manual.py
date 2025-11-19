#!/usr/bin/env python
"""
Script para probar manualmente el detector de código IA.
Prueba con ejemplos claros de código humano vs IA.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from codigo.modelos.production_code_detector import get_detector

# Código claramente humano (informal, con bugs)
CODIGO_HUMANO = """
def calc(x, y):
    # TODO: fix this later
    result = x + y
    print(result)  # debug
    return result

nums = [1,2,3, 4,5]
total=0
for n in nums:
    total+=n
"""

# Código claramente IA (documentación exhaustiva, type hints)
CODIGO_IA = """
from typing import List

def calculate_sum(numbers: List[int]) -> int:
    \"\"\"
    Calculate the sum of a list of numbers.
    
    Args:
        numbers: A list of integers to sum.
        
    Returns:
        The sum of all numbers in the list.
        
    Raises:
        ValueError: If the input list is empty.
    \"\"\"
    if not numbers:
        raise ValueError("Cannot calculate sum of empty list")
    
    return sum(numbers)
"""

def test_detector():
    print("🔍 Cargando detector...")
    detector = get_detector()
    
    print(f"\n✅ Detector cargado: {detector.version}")
    print(f"⏰ Timestamp: {detector.timestamp}\n")
    
    print("=" * 70)
    print("🧑 PRUEBA 1: CÓDIGO HUMANO (debería detectarse como HUMANO)")
    print("=" * 70)
    resultado_humano = detector.analizar(CODIGO_HUMANO)
    print(f"Resultado: {'IA' if resultado_humano['is_ai_generated'] else 'HUMANO'}")
    print(f"Confianza: {resultado_humano['confidence']:.2%}")
    print(f"Probabilidad IA: {resultado_humano.get('ai_prob', 0):.2%}")
    print(f"Probabilidad Humano: {resultado_humano.get('human_prob', 0):.2%}")
    print(f"Método: {resultado_humano['method_used']}")
    
    print("\n" + "=" * 70)
    print("🤖 PRUEBA 2: CÓDIGO IA (debería detectarse como IA)")
    print("=" * 70)
    resultado_ia = detector.analizar(CODIGO_IA)
    print(f"Resultado: {'IA' if resultado_ia['is_ai_generated'] else 'HUMANO'}")
    print(f"Confianza: {resultado_ia['confidence']:.2%}")
    print(f"Probabilidad IA: {resultado_ia.get('ai_prob', 0):.2%}")
    print(f"Probabilidad Humano: {resultado_ia.get('human_prob', 0):.2%}")
    print(f"Método: {resultado_ia['method_used']}")
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    
    if not resultado_humano['is_ai_generated']:
        print("✅ Código humano detectado correctamente")
    else:
        print("❌ ERROR: Código humano detectado como IA")
        
    if resultado_ia['is_ai_generated']:
        print("✅ Código IA detectado correctamente")
    else:
        print("❌ ERROR: Código IA detectado como humano")
    
    # Verificar si las etiquetas están invertidas
    print("\n" + "=" * 70)
    print("🔬 DIAGNÓSTICO DE ETIQUETAS")
    print("=" * 70)
    
    if resultado_humano.get('ai_prob', 0) > resultado_humano.get('human_prob', 0):
        print("⚠️  PROBLEMA: Para código humano, ai_prob > human_prob")
        print("   Las etiquetas del modelo están INVERTIDAS")
        print("   Label 0 probablemente es HUMANO, no IA")
    else:
        print("✅ Las probabilidades parecen correctas")

if __name__ == "__main__":
    test_detector()
