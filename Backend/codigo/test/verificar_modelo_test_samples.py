#!/usr/bin/env python
"""
Script para verificar el rendimiento del modelo usando los archivos de test_samples.
Analiza todos los archivos y muestra estadísticas de precisión.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from codigo.modelos.production_code_detector import get_detector
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}\n")

def print_result(nombre, esperado, resultado, confianza):
    """Imprime el resultado de un análisis"""
    is_ia = resultado.get('is_ai_generated', False)
    correcto = (esperado == 'IA' and is_ia) or (esperado == 'HUMANO' and not is_ia)
    
    status = f"{Colors.GREEN}✓ CORRECTO{Colors.RESET}" if correcto else f"{Colors.RED}✗ INCORRECTO{Colors.RESET}"
    esperado_str = f"{Colors.YELLOW}Esperado: {esperado}{Colors.RESET}"
    detectado_str = f"{Colors.RED}IA{Colors.RESET}" if is_ia else f"{Colors.GREEN}HUMANO{Colors.RESET}"
    conf_str = f"{confianza*100:.1f}%"
    
    print(f"{status} | {nombre:40} | {esperado_str:20} | Detectado: {detectado_str:10} | Confianza: {conf_str}")
    
    return correcto

def analizar_archivo(ruta_archivo, esperado):
    """Analiza un archivo y retorna el resultado"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        detector = get_detector()
        resultado = detector.analizar(codigo)
        
        return resultado
    except Exception as e:
        print(f"{Colors.RED}Error al analizar {ruta_archivo}: {e}{Colors.RESET}")
        return None

def main():
    print_header("🧪 VERIFICACIÓN DEL MODELO CON TEST_SAMPLES")
    
    # Obtener detector
    detector = get_detector()
    print(f"{Colors.BLUE}Detector cargado: {type(detector).__name__}{Colors.RESET}")
    print(f"{Colors.BLUE}Versión: {getattr(detector, 'version', 'N/A')}{Colors.RESET}\n")
    
    # Ruta a test_samples
    base_dir = Path(__file__).parent
    test_samples_dir = base_dir / 'test_samples'
    
    if not test_samples_dir.exists():
        print(f"{Colors.RED}Error: No se encontró la carpeta test_samples{Colors.RESET}")
        return
    
    # Definir qué archivos son IA y cuáles son humanos
    archivos_ia = [
        'codigo_ia_1.py',
        'codigo_ia_2.py',
        'codigo_ia_3.py',
        'codigo_ia_4.py',
        'codigo_ia_chatgpt_1.py',
        'codigo_ia_chatgpt_2.py',
        'codigo_ia_chatgpt_3.py',
        'codigo_ia_chatgpt_4.py',
        'codigo_ia_chatgpt_5.py',
        'codigo_ia_simple_1.py',
        'codigo_ia_simple_2.py',
        'codigo_ia_simple_3.py',
    ]
    
    archivos_humano = [
        'codigo_humano_1.py',
        'codigo_humano_2.py',
        'codigo_humano_3.py',
        'codigo_humano_4.py',
        'codigo_humano_5.py',
        'codigo_humano_simple_1.py',
        'codigo_humano_simple_2.py',
        'codigo_humano_simple_3.py',
    ]
    
    resultados = []
    correctos = 0
    total = 0
    
    print(f"{Colors.BOLD}Analizando archivos de código IA:{Colors.RESET}\n")
    for archivo in archivos_ia:
        ruta = test_samples_dir / archivo
        if ruta.exists():
            resultado = analizar_archivo(ruta, 'IA')
            if resultado:
                confianza = resultado.get('confidence', 0.0)
                correcto = print_result(archivo, 'IA', resultado, confianza)
                resultados.append({
                    'archivo': archivo,
                    'esperado': 'IA',
                    'detectado': 'IA' if resultado.get('is_ai_generated') else 'HUMANO',
                    'correcto': correcto,
                    'confianza': confianza
                })
                if correcto:
                    correctos += 1
                total += 1
    
    print(f"\n{Colors.BOLD}Analizando archivos de código HUMANO:{Colors.RESET}\n")
    for archivo in archivos_humano:
        ruta = test_samples_dir / archivo
        if ruta.exists():
            resultado = analizar_archivo(ruta, 'HUMANO')
            if resultado:
                confianza = resultado.get('confidence', 0.0)
                correcto = print_result(archivo, 'HUMANO', resultado, confianza)
                resultados.append({
                    'archivo': archivo,
                    'esperado': 'HUMANO',
                    'detectado': 'IA' if resultado.get('is_ai_generated') else 'HUMANO',
                    'correcto': correcto,
                    'confianza': confianza
                })
                if correcto:
                    correctos += 1
                total += 1
    
    # Estadísticas finales
    print_header("📊 ESTADÍSTICAS FINALES")
    
    if total > 0:
        precision = (correctos / total) * 100
        print(f"{Colors.BOLD}Total de archivos analizados: {total}{Colors.RESET}")
        print(f"{Colors.GREEN}Correctos: {correctos}{Colors.RESET}")
        print(f"{Colors.RED}Incorrectos: {total - correctos}{Colors.RESET}")
        print(f"{Colors.BOLD}Precisión: {precision:.2f}%{Colors.RESET}\n")
        
        # Confianza promedio
        confianzas = [r['confianza'] for r in resultados]
        if confianzas:
            confianza_promedio = sum(confianzas) / len(confianzas)
            print(f"{Colors.BLUE}Confianza promedio: {confianza_promedio*100:.2f}%{Colors.RESET}\n")
        
        # Análisis por categoría
        ia_correctos = sum(1 for r in resultados if r['esperado'] == 'IA' and r['correcto'])
        ia_total = sum(1 for r in resultados if r['esperado'] == 'IA')
        humano_correctos = sum(1 for r in resultados if r['esperado'] == 'HUMANO' and r['correcto'])
        humano_total = sum(1 for r in resultados if r['esperado'] == 'HUMANO')
        
        print(f"{Colors.BOLD}Por categoría:{Colors.RESET}")
        if ia_total > 0:
            precision_ia = (ia_correctos / ia_total) * 100
            print(f"  IA: {ia_correctos}/{ia_total} correctos ({precision_ia:.2f}%)")
        if humano_total > 0:
            precision_humano = (humano_correctos / humano_total) * 100
            print(f"  HUMANO: {humano_correctos}/{humano_total} correctos ({precision_humano:.2f}%)\n")
        
        # Mostrar errores
        errores = [r for r in resultados if not r['correcto']]
        if errores:
            print(f"{Colors.RED}Archivos con detección incorrecta:{Colors.RESET}")
            for error in errores:
                print(f"  - {error['archivo']}: Esperado {error['esperado']}, Detectado {error['detectado']} (Confianza: {error['confianza']*100:.1f}%)")
    else:
        print(f"{Colors.RED}No se encontraron archivos para analizar{Colors.RESET}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Análisis interrumpido por el usuario{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{Colors.RED}Error inesperado: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

