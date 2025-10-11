
"""
Ejemplos de uso del Sistema de Detección de Código IA
"""

import joblib
import json

def cargar_sistema():
    """Carga el sistema de detección"""
    try:
        detector = joblib.load('./code-detection-model/production_detector.pkl')
        print("✅ Sistema cargado exitosamente")
        return detector
    except Exception as e:
        print(f"❌ Error al cargar el sistema: {e}")
        return None

def ejemplos_basicos():
    """Ejemplos básicos de uso"""
    detector = cargar_sistema()
    if not detector:
        return
    
    ejemplos = [
        # Código simple humano
        """
        def suma(a, b):
            return a + b
        """,
        
        # Código IA típico
        """
        from typing import List, Optional
        import numpy as np
        
        def process_data(data: List[float]) -> Optional[float]:
            if not data:
                return None
            return np.mean(data)
        """,
        
        # Código humano con debug
        """
        def calcular_promedio(numeros):
            # TODO: Agregar validación de entrada
            print(f"Procesando {len(numeros)} números")
            if not numeros:
                return 0
            return sum(numeros) / len(numeros)
        """
    ]
    
    print("\n🧪 EJECUTANDO EJEMPLOS:")
    for i, codigo in enumerate(ejemplos, 1):
        resultado = detector.detect(codigo)
        print(f"\n📝 Ejemplo {i}:")
        print(f"   ¿Es IA?: {resultado['is_ai_generated']}")
        print(f"   Confianza: {resultado['confidence']:.1%}")
        print(f"   Método: {resultado['method_used']}")

if __name__ == "__main__":
    print("🚀 EJEMPLOS DE USO - DETECTOR DE CÓDIGO IA")
    print("=" * 50)
    ejemplos_basicos()
