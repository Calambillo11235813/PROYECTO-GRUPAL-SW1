#!/usr/bin/env python
"""
Script rápido para ejecutar tests del detector de código IA
Uso: python run_tests.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           🧪 DETECTOR DE CÓDIGO IA vs HUMANO - SUITE DE TESTS              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("Selecciona una opción:\n")
    print("1. Ejecutar TODOS los tests unitarios")
    print("2. Ejecutar ejemplos prácticos (interactivo)")
    print("3. Probar código personalizado")
    print("4. Comparar dos códigos")
    print("5. Ejecutar tests específicos")
    print("6. Ver información del detector")
    print("0. Salir\n")
    
    opcion = input("Opción: ").strip()
    
    if opcion == "1":
        ejecutar_tests_unitarios()
    elif opcion == "2":
        ejecutar_ejemplos_practicos()
    elif opcion == "3":
        probar_codigo_personalizado()
    elif opcion == "4":
        comparar_codigos()
    elif opcion == "5":
        menu_tests_especificos()
    elif opcion == "6":
        ver_info_detector()
    elif opcion == "0":
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)
    else:
        print("\n❌ Opción inválida")
        main()


def ejecutar_tests_unitarios():
    """Ejecuta todos los tests unitarios"""
    print("\n" + "="*80)
    print("🏃 Ejecutando tests unitarios...")
    print("="*80 + "\n")
    
    from django.core.management import call_command
    call_command('test', 'codigo.test_detector_ia', verbosity=2)
    
    input("\n\nPresiona ENTER para volver al menú...")
    main()


def ejecutar_ejemplos_practicos():
    """Ejecuta los ejemplos prácticos"""
    print("\n" + "="*80)
    print("🎨 Ejecutando ejemplos prácticos...")
    print("="*80 + "\n")
    
    from Backend.codigo.test.test_ejemplos_practicos import ejecutar_ejemplos
    ejecutar_ejemplos()
    
    input("\n\nPresiona ENTER para volver al menú...")
    main()


def probar_codigo_personalizado():
    """Permite probar código personalizado"""
    print("\n" + "="*80)
    print("✏️  PROBAR CÓDIGO PERSONALIZADO")
    print("="*80 + "\n")
    
    print("Ingresa tu código (escribe 'FIN' en una línea sola para terminar):\n")
    
    lineas = []
    while True:
        linea = input()
        if linea.strip() == 'FIN':
            break
        lineas.append(linea)
    
    codigo = '\n'.join(lineas)
    
    if not codigo.strip():
        print("\n❌ No se ingresó código")
        input("Presiona ENTER para continuar...")
        main()
        return
    
    from Backend.codigo.test.test_ejemplos_practicos import test_codigo_personalizado
    test_codigo_personalizado(codigo)
    
    input("\n\nPresiona ENTER para volver al menú...")
    main()


def comparar_codigos():
    """Compara dos fragmentos de código"""
    print("\n" + "="*80)
    print("⚖️  COMPARAR DOS CÓDIGOS")
    print("="*80 + "\n")
    
    print("Ingresa el PRIMER código (escribe 'FIN' para terminar):\n")
    lineas1 = []
    while True:
        linea = input()
        if linea.strip() == 'FIN':
            break
        lineas1.append(linea)
    
    codigo1 = '\n'.join(lineas1)
    
    print("\nIngresa el SEGUNDO código (escribe 'FIN' para terminar):\n")
    lineas2 = []
    while True:
        linea = input()
        if linea.strip() == 'FIN':
            break
        lineas2.append(linea)
    
    codigo2 = '\n'.join(lineas2)
    
    if not codigo1.strip() or not codigo2.strip():
        print("\n❌ Ambos códigos deben tener contenido")
        input("Presiona ENTER para continuar...")
        main()
        return
    
    from Backend.codigo.test.test_ejemplos_practicos import comparar_codigos as comp
    comp(codigo1, codigo2, "Código 1", "Código 2")
    
    input("\n\nPresiona ENTER para volver al menú...")
    main()


def menu_tests_especificos():
    """Menú de tests específicos"""
    print("\n" + "="*80)
    print("🎯 TESTS ESPECÍFICOS")
    print("="*80 + "\n")
    
    print("1. Test: Detector disponible")
    print("2. Test: Código simple humano")
    print("3. Test: Código generado por IA")
    print("4. Test: Análisis sintáctico")
    print("5. Test: Marcado de líneas")
    print("6. Test: Comparación de estilos")
    print("0. Volver\n")
    
    opcion = input("Opción: ").strip()
    
    tests = {
        "1": "codigo.test_detector_ia.CodigoIATestCase.test_detector_disponible",
        "2": "codigo.test_detector_ia.CodigoIATestCase.test_codigo_simple_humano",
        "3": "codigo.test_detector_ia.CodigoIATestCase.test_codigo_ia_generado",
        "4": "codigo.test_detector_ia.CodigoIATestCase.test_analisis_codigo_simple",
        "5": "codigo.test_detector_ia.CodigoIATestCase.test_marcado_lineas_codigo_limpio",
        "6": "codigo.test_detector_ia.CodigoComparativoTestCase.test_comparar_estilos_codigo",
    }
    
    if opcion == "0":
        main()
        return
    
    if opcion in tests:
        from django.core.management import call_command
        call_command('test', tests[opcion], verbosity=2)
        input("\n\nPresiona ENTER para continuar...")
    else:
        print("\n❌ Opción inválida")
    
    menu_tests_especificos()


def ver_info_detector():
    """Muestra información del detector"""
    print("\n" + "="*80)
    print("ℹ️  INFORMACIÓN DEL DETECTOR")
    print("="*80 + "\n")
    
    from codigo.modelos.production_code_detector import get_detector
    
    try:
        detector = get_detector()
        
        print(f"✓ Tipo: {type(detector).__name__}")
        print(f"✓ Versión: {getattr(detector, 'version', 'N/A')}")
        print(f"✓ Timestamp: {getattr(detector, 'timestamp', 'N/A')}")
        
        # Probar con código simple
        print("\n🧪 Probando con código de ejemplo...")
        resultado = detector.analizar("def test(): return True")
        
        print(f"\n✓ Detector funcionando correctamente")
        print(f"  - Método usado: {resultado.get('method_used', 'N/A')}")
        print(f"  - Confianza: {resultado.get('confidence', 0)*100:.2f}%")
        
    except Exception as e:
        print(f"❌ Error al cargar el detector: {str(e)}")
    
    input("\n\nPresiona ENTER para volver al menú...")
    main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
