#!/usr/bin/env python
"""
Script para probar el detector con archivos reales.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from codigo.modelos.production_code_detector import get_detector

def probar_archivo(ruta, tipo_esperado):
    with open(ruta, 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    detector = get_detector()
    resultado = detector.analizar(codigo)
    
    print(f"\n📄 Archivo: {os.path.basename(ruta)}")
    print(f"   Tipo esperado: {tipo_esperado}")
    print(f"   Detectado como: {'IA' if resultado['is_ai_generated'] else 'HUMANO'}")
    print(f"   Confianza: {resultado['confidence']:.2%}")
    print(f"   Prob IA: {resultado.get('ai_prob', 0):.2%}")
    print(f"   Prob Humano: {resultado.get('human_prob', 0):.2%}")
    
    correcto = (tipo_esperado == "IA" and resultado['is_ai_generated']) or \
               (tipo_esperado == "HUMANO" and not resultado['is_ai_generated'])
    print(f"   ✅ Correcto" if correcto else f"   ❌ Incorrecto")
    
    return correcto

def main():
    base_path = "tests/test_samples"
    
    archivos_humano = [
        "codigo_humano_1.py",
        "codigo_humano_2.py",
        "codigo_humano_3.py",
    ]
    
    archivos_ia = [
        "codigo_ia_1.py",
        "codigo_ia_2.py",
        "codigo_ia_3.py",
    ]
    
    print("=" * 70)
    print("🧪 PROBANDO DETECTOR CON ARCHIVOS REALES")
    print("=" * 70)
    
    correctos = 0
    total = 0
    
    print("\n" + "=" * 70)
    print("🧑 CÓDIGO HUMANO")
    print("=" * 70)
    for archivo in archivos_humano:
        ruta = os.path.join(base_path, archivo)
        if os.path.exists(ruta):
            if probar_archivo(ruta, "HUMANO"):
                correctos += 1
            total += 1
    
    print("\n" + "=" * 70)
    print("🤖 CÓDIGO IA")
    print("=" * 70)
    for archivo in archivos_ia:
        ruta = os.path.join(base_path, archivo)
        if os.path.exists(ruta):
            if probar_archivo(ruta, "IA"):
                correctos += 1
            total += 1
    
    print("\n" + "=" * 70)
    print("📊 RESULTADO FINAL")
    print("=" * 70)
    print(f"Correctos: {correctos}/{total} ({correctos/total*100:.1f}%)")

if __name__ == "__main__":
    main()
