"""
Script optimizado para completar la traducción del dataset
con mejor manejo de errores y verificación de líneas
"""
import pandas as pd
import time
import os
import sys
import random
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator

# Configuración
input_path = r'D:\1.CARRERA UNIVERSITARIA\9. DECIMO SEMESTRE\1.INGIENERIA SOFTWARE 1\3.PROYECTOS\PROYECTO-GRUPAL-SW1\Backend\texto\dataset_para_completar.csv'
output_path = 'dataset_binario_español_completo.csv'
error_log_path = 'errores_traduccion_continuacion.log'
forzar_retraduccion = False  # Cambiar a True para retraducir textos marcados como ERROR

# Configuración de procesamiento
num_threads = 4
block_size = 20  # Antes era 50
delay_between_requests = 0.5
max_retries = 3
char_limit = 5000

# Inicializar traductor
translator_google = GoogleTranslator(source='en', target='es')

# Crear manejador de señal para Ctrl+C
def signal_handler(sig, frame):
    print("\nInterrupción detectada, guardando progreso...")
    df.to_csv(output_path, index=False)
    print(f"Progreso guardado en {output_path}. Saliendo...")
    sys.exit(0)

import signal
signal.signal(signal.SIGINT, signal_handler)

# Función de traducción mejorada
def translate_text(text):
    """Traduce texto con mejor manejo de tamaño y errores"""
    if not text or not text.strip():
        return ""
    
    try:
        # Para textos largos, dividir en párrafos
        if len(text) > char_limit:
            paragraphs = text.split('\n')
            translated = []
            
            for para in paragraphs:
                if para.strip():
                    try:
                        translated.append(translator_google.translate(para.strip()))
                        time.sleep(0.3)  # Pausa breve entre párrafos
                    except Exception as e:
                        translated.append(f"[ERROR PÁRRAFO: {str(e)}] {para}")
            
            return '\n'.join(translated)
        else:
            return translator_google.translate(text)
    except Exception as e:
        return f"ERROR: {str(e)}"

# Función para procesar un lote de textos
def translate_batch(indices, dataframe):
    results = {}
    for idx in indices:
        source_text = str(dataframe.loc[idx, 'text']).strip()
        current_translation = str(dataframe.loc[idx, 'text_es']).strip()
        
        # Determinar si necesita traducción:
        # 1. Si está vacío, o
        # 2. Si contiene "ERROR" y forzar_retraduccion=True, o
        # 3. Si contiene texto en inglés (texto original igual a text_es)
        if (not current_translation or 
            (forzar_retraduccion and "ERROR" in current_translation) or
            current_translation == source_text):
            
            if source_text:  # Solo traducir si hay texto original
                retries = 0
                success = False
                
                while retries < max_retries and not success:
                    try:
                        translated = translate_text(source_text)
                        results[idx] = translated
                        success = True
                    except Exception as e:
                        retries += 1
                        time.sleep(random.uniform(1, 3))
                        if retries == max_retries:
                            results[idx] = f"ERROR: {str(e)}"
                
                time.sleep(delay_between_requests)  # Pausa entre traducciones
    
    return results

# Cargar dataset
print("Cargando dataset...")
df = pd.read_csv(input_path)

# Verificar columnas y tipos de datos
if 'text' not in df.columns:
    print("Error: No se encontró la columna 'text' en el dataset")
    sys.exit(1)

if 'text_es' not in df.columns:
    print("Agregando columna 'text_es' al dataset")
    df['text_es'] = ""

df['text'] = df['text'].astype(str)
df['text_es'] = df['text_es'].astype(str)

# Análisis previo del dataset
total_rows = len(df)
empty_translations = df['text_es'].isna().sum() + (df['text_es'] == '').sum()
error_translations = df['text_es'].str.contains('ERROR', na=False).sum()

print(f"Total de filas en el dataset: {total_rows}")
print(f"Traducciones vacías: {empty_translations}")
print(f"Traducciones con error: {error_translations}")
print(f"Traducciones pendientes estimadas: {empty_translations + error_translations}")

# Abrir archivo de log
error_log = open(error_log_path, "a", encoding="utf-8")

try:
    # Hora de inicio
    start_time = time.time()
    total_translated = 0
    
    # Procesar en bloques con ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Crear lista de índices a procesar (enfocándose en filas sin traducción primero)
        indices_to_process = []
        
        for idx in range(len(df)):
            current_text = str(df.loc[idx, 'text_es']).strip()
            if not current_text or (forzar_retraduccion and "ERROR" in current_text):
                indices_to_process.append(idx)
        
        # Si se necesita, agregar otras filas para revisión
        if not indices_to_process:
            for idx in range(len(df)):
                source = str(df.loc[idx, 'text']).strip()
                current = str(df.loc[idx, 'text_es']).strip()
                # Verificar si la traducción parece ser el mismo texto en inglés
                if current and current == source:
                    indices_to_process.append(idx)
        
        print(f"Se procesarán {len(indices_to_process)} filas")
        
        # Dividir en bloques para procesamiento
        for i in tqdm(range(0, len(indices_to_process), block_size), desc="Bloques procesados"):
            block_indices = indices_to_process[i:min(i+block_size, len(indices_to_process))]
            block_modified = False
            
            # Dividir el bloque en sub-bloques para los hilos
            sub_block_size = max(1, len(block_indices) // num_threads)
            sub_blocks = [block_indices[j:j+sub_block_size] for j in range(0, len(block_indices), sub_block_size)]
            
            # Enviar cada sub-bloque a un hilo diferente
            futures = [executor.submit(translate_batch, sub_block, df) for sub_block in sub_blocks]
            
            # Recoger resultados
            for future in tqdm(futures, desc="Procesando sub-bloques", leave=False):
                results = future.result()
                for idx, translated_text in results.items():
                    if translated_text is None:
                        error_log.write(f"Error en fila {idx}: Resultado de traducción nulo\n")
                        df.loc[idx, 'text_es'] = "ERROR: Traducción fallida"
                    elif not translated_text.startswith("ERROR:"):
                        df.loc[idx, 'text_es'] = translated_text
                        block_modified = True
                        total_translated += 1
                    else:
                        error_log.write(f"Error en fila {idx}: {translated_text}\n")
            
            # Guardar después de cada bloque
            if block_modified:
                df.to_csv(output_path, index=False)
                print(f"Bloque {i//block_size+1} guardado. {total_translated} textos traducidos hasta ahora.")
    
    # Finalizar y mostrar estadísticas
    end_time = time.time()
    elapsed = end_time - start_time
    print(f'Traducción completa. Dataset guardado como {output_path}')
    print(f'Tiempo total de procesamiento: {elapsed:.2f} segundos')
    print(f'Total de textos traducidos en esta ejecución: {total_translated}')

except Exception as e:
    print(f"Error en la ejecución: {str(e)}")
    # Guardar el progreso en caso de error
    df.to_csv(output_path, index=False)
    print(f"Progreso guardado en {output_path} debido a un error.")

finally:
    # Cerrar archivo de log
    error_log.close()