import requests
import json
import os
import sys

# Agregar el directorio padre para imports de Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_file_upload():
    """Test completo de funcionalidad de carga de archivos"""
    
    base_url = "http://127.0.0.1:8000/api/texto"
    
    print("🚀 Iniciando pruebas de carga de archivos...")
    print("=" * 50)
    
    # Crear archivo TXT de prueba en fixtures
    fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    os.makedirs(fixtures_dir, exist_ok=True)
    
    test_content = """
Este es un documento de prueba para verificar el sistema de detección de contenido generado por IA.
El sistema debe ser capaz de analizar este texto y determinar si fue escrito por un humano o generado 
por inteligencia artificial. Este texto contiene suficientes palabras para que el modelo BERT pueda 
realizar un análisis preciso y proporcionar probabilidades confiables sobre el origen del contenido.
Además, incluiremos más texto para asegurar que supere el límite mínimo de caracteres requerido.
"""
    
    # Test 1: Archivo TXT
    print("🧪 TEST 1: Analizando archivo TXT...")
    test_file_path = os.path.join(fixtures_dir, "test_document.txt")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        with open(test_file_path, "rb") as f:
            files = {"archivo": ("test_document.txt", f, "text/plain")}
            data = {"modelo": "B"}

            response = requests.post(f"{base_url}/analizar-archivo/", files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            print("✅ Análisis TXT exitoso:")
            print(f"   📊 Resultado: {result['resultado']}")
            print(f"   🤖 Prob. IA: {result['probabilidad_ia']}")
            print(f"   👤 Prob. Humano: {result['probabilidad_humano']}")
            print(f"   📁 Archivo: {result['archivo_info']['nombre']}")
            print(f"   📏 Tamaño: {result['archivo_info']['tamano']} bytes")
            print(f"   🆔 ID Análisis: {result['analisis_id']}")
        else:
            print(f"❌ Error en análisis TXT: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Servidor no disponible.")
        print("   💡 Solución: Ejecuta 'python manage.py runserver' en otra terminal")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    # Test 2: Comparación de modelos
    print("\n🧪 TEST 2: Comparando modelos...")
    try:
        with open(test_file_path, "rb") as f:
            files = {"archivo": ("test_document.txt", f, "text/plain")}

            response = requests.post(f"{base_url}/comparar-archivo/", files=files)

        if response.status_code == 200:
            result = response.json()
            print("✅ Comparación exitosa:")
            print(f"   🅱️ Modelo B: {result['modelo_b']['resultado']} (IA: {result['modelo_b']['probabilidad_ia']}%)")
            print(f"   🅽️ Modelo N: {result['modelo_n']['resultado']} (IA: {result['modelo_n']['probabilidad_ia']}%)")
            print(f"   🤝 Consenso: {result['consenso']}")
        else:
            print(f"❌ Error en comparación: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en comparación: {e}")
    
    # Test 3: Validación de tamaño
    print("\n🧪 TEST 3: Validación de archivo grande...")
    large_content = "A" * 20000  # 20KB, debería funcionar
    
    with open("large_test.txt", "w", encoding="utf-8") as f:
        f.write(large_content)
    
    try:
        with open("large_test.txt", "rb") as f:
            files = {"archivo": ("large_test.txt", f, "text/plain")}
            data = {"modelo": "B"}

            response = requests.post(f"{base_url}/analizar-archivo/", files=files, data=data)

        if response.status_code == 200:
            print("✅ Archivo grande procesado correctamente")
        else:
            result = response.json()
            print(f"⚠️ Validación funcionando: {result.get('error', 'Error desconocido')}")
            
    except Exception as e:
        print(f"❌ Error con archivo grande: {e}")
    
    # Test 4: Formato no soportado
    print("\n🧪 TEST 4: Validación de formato...")
    with open("test.jpg", "wb") as f:
        f.write(b"fake image content")
    
    try:
        with open("test.jpg", "rb") as f:
            files = {"archivo": ("test.jpg", f, "image/jpeg")}
            data = {"modelo": "B"}

            response = requests.post(f"{base_url}/analizar-archivo/", files=files, data=data)

        if response.status_code == 400:
            result = response.json()
            print(f"✅ Validación de formato funcionando: {result.get('error')}")
        else:
            print("⚠️ Debería rechazar formatos no soportados")
            
    except Exception as e:
        print(f"❌ Error en validación: {e}")
    
    # Test 5: Sin archivo
    print("\n🧪 TEST 5: Validación sin archivo...")
    try:
        data = {"modelo": "B"}
        response = requests.post(f"{base_url}/analizar-archivo/", data=data)
        
        if response.status_code == 400:
            result = response.json()
            print(f"✅ Validación sin archivo funcionando: {result.get('error')}")
        else:
            print("⚠️ Debería requerir archivo")
            
    except Exception as e:
        print(f"❌ Error en validación sin archivo: {e}")
    
    # Limpiar archivos de prueba
    print("\n🧹 Limpiando archivos de prueba...")
    test_files = ["test_document.txt", "large_test.txt", "test.jpg"]
    for filename in test_files:
        file_path = os.path.join(fixtures_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"   🗑️ Eliminado: {filename}")
    
    print("\n🎉 ¡Todas las pruebas completadas!")
    print("=" * 50)
    return True

def test_existing_endpoints():
    """Test de endpoints existentes para verificar compatibilidad"""
    
    base_url = "http://127.0.0.1:8000/api/texto"
    
    print("\n🔄 Verificando endpoints existentes...")
    
    # Test análisis de texto directo - CORREGIR NOMBRE DE ENDPOINT
    try:
        data = {
            "texto": "Este es un texto de prueba para verificar que los endpoints existentes siguen funcionando correctamente."
        }
        # CAMBIO: usar /analizar/ en lugar de /analizar-texto/
        response = requests.post(f"{base_url}/analizar/", json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Endpoint /analizar/ funcionando: {result['prediccion']}")
        else:
            print(f"⚠️ Problema con /analizar/: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en endpoint existente: {e}")

if __name__ == "__main__":
    success = test_file_upload()
    if success:
        test_existing_endpoints()