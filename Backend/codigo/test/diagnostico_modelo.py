#!/usr/bin/env python
"""Script de diagnóstico para ver las probabilidades reales del modelo"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from codigo.modelos.production_code_detector import get_detector
from pathlib import Path
import torch

detector = get_detector()

# Código de ejemplo IA
codigo_ia = """
def calculate_fibonacci_sequence(n: int) -> list:
    \"\"\"
    Calculate the Fibonacci sequence up to the nth term.
    
    Args:
        n (int): The number of terms to generate
        
    Returns:
        list: A list containing the Fibonacci sequence
    \"\"\"
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    return [0, 1, 1, 2, 3]
"""

# Código de ejemplo humano
codigo_humano = """
def fib(n):
    if n<2:return n
    return fib(n-1)+fib(n-2)
"""

print("="*80)
print("DIAGNÓSTICO DEL MODELO")
print("="*80)

# Obtener probabilidades crudas del modelo
if hasattr(detector, 'model') and hasattr(detector, 'tokenizer'):
    print("\n📊 Probabilidades crudas del modelo:\n")
    
    for nombre, codigo in [("Código IA", codigo_ia), ("Código Humano", codigo_humano)]:
        inputs = detector.tokenizer(
            codigo,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        ).to(detector.device)
        
        with torch.no_grad():
            logits = detector.model(**inputs).logits
            probs = torch.softmax(logits, dim=1)[0]
        
        print(f"{nombre}:")
        print(f"  Label 0 (según config: 'Ai_generated'): {probs[0].item()*100:.2f}%")
        print(f"  Label 1 (según config: 'Human_written'): {probs[1].item()*100:.2f}%")
        print(f"  Resultado detector: {detector.analizar(codigo)}")
        print()

print("="*80)
print("INTERPRETACIÓN:")
print("="*80)
print("Si Label 0 tiene alta probabilidad para código IA → config.json es correcto")
print("Si Label 1 tiene alta probabilidad para código IA → etiquetas están invertidas")
print("="*80)

