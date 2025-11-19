import os
import sys

# Añadir el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audio.ia_model import verificar_autenticidad

def test_audio_analysis(audio_path):
    """
    Prueba el análisis de un archivo de audio.
    """
    if not os.path.exists(audio_path):
        print(f"Error: El archivo {audio_path} no existe.")
        return
    
    print(f"Analizando archivo: {audio_path}")
    
    try:
        # Llamar a la función de verificación
        resultado, probabilidad = verificar_autenticidad(audio_path)
        
        print("\n--- Resultados del análisis ---")
        print(f"Resultado: {resultado.upper()}")
        print(f"Probabilidad: {probabilidad:.4f}")
        print("----------------------------")
        
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python test_rf_model.py <ruta_al_archivo_de_audio>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    test_audio_analysis(audio_path)
