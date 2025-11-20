#!/usr/bin/env python
"""Script para analizar las probabilidades reales del modelo"""

import os
import sys
from pathlib import Path

# Agregar Backend al path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

try:
    import django
    django.setup()
except:
    pass

from codigo.modelos.production_code_detector import get_detector

detector = get_detector()

# Leer archivos de test
test_samples_dir = Path(__file__).parent / 'test_samples'

archivos_ia = [
    'codigo_ia_1.py',
    'codigo_ia_chatgpt_1.py',
    'codigo_ia_simple_1.py',
]

archivos_humano = [
    'codigo_humano_1.py',
    'codigo_humano_simple_1.py',
    'codigo_humano_2.py',
]

print("="*80)
print("ANÁLISIS DE PROBABILIDADES DEL MODELO")
print("="*80)

if hasattr(detector, 'model') and hasattr(detector, 'tokenizer'):
    import torch
    
    print("\n📊 CÓDIGO IA (debería dar alta prob en Label 0):\n")
    for archivo in archivos_ia:
        ruta = test_samples_dir / archivo
        if ruta.exists():
            with open(ruta, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
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
            
            resultado = detector.analizar(codigo)
            print(f"{archivo}:")
            print(f"  Label 0 (IA según config): {probs[0].item()*100:.2f}%")
            print(f"  Label 1 (Humano según config): {probs[1].item()*100:.2f}%")
            print(f"  Detector dice: {'IA' if resultado['is_ai_generated'] else 'HUMANO'} (conf: {resultado['confidence']*100:.1f}%)")
            print()
    
    print("\n📊 CÓDIGO HUMANO (debería dar alta prob en Label 1):\n")
    for archivo in archivos_humano:
        ruta = test_samples_dir / archivo
        if ruta.exists():
            with open(ruta, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
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
            
            resultado = detector.analizar(codigo)
            print(f"{archivo}:")
            print(f"  Label 0 (IA según config): {probs[0].item()*100:.2f}%")
            print(f"  Label 1 (Humano según config): {probs[1].item()*100:.2f}%")
            print(f"  Detector dice: {'IA' if resultado['is_ai_generated'] else 'HUMANO'} (conf: {resultado['confidence']*100:.1f}%)")
            print()

print("="*80)
print("CONCLUSIÓN:")
print("="*80)
print("Si Label 0 es alto para código IA → config.json correcto")
print("Si Label 1 es alto para código humano → config.json correcto")
print("Si ambos dan Label 0 alto → modelo sesgado o etiquetas invertidas")
print("="*80)

