"""
Script actualizado para traducir dataset de inglés a español
usando la biblioteca 'translate' que es compatible con Python 3.11+
"""
import pandas as pd
from tqdm import tqdm
import time
import os
import random
from concurrent.futures import ThreadPoolExecutor
import signal
import sys
from translate import Translator

# Rutas de archivos
input_path = r'D:\1.CARRERA UNIVERSITARIA\9. DECIMO SEMESTRE\1.INGIENERIA SOFTWARE 1\3.PROYECTOS\PROYECTO-GRUPAL-SW1\Backend\texto\Dataset_traducidos\dataset_parte_traducida.csv'
output_path = 'dataset_parte_traducida_nuevo.csv'
error_log_path = 'errores_traduccion.log'

# Cargar y preparar el dataset
print("Cargando dataset...")
df = pd.read_csv(input_path)
df['text'] = df['text'].astype(str)

# Comprobar si ya existe un archivo de salida para continuar donde se quedó
if os.path.exists(output_path):
    df_existing = pd.read_csv(output_path)
    if 'text_es' in df_existing.columns:
        print(f"Encontrado archivo existente con {len(df_existing)} filas. Continuando desde ahí...")
        df = df_existing
else:
    df['text_es'] = ""  # Nueva columna para el texto traducido

# Configuración de procesamiento
block_size = 10  # Tamaño de bloque reducido para guardar más frecuentemente
delay_between_requests = 2.0  # Pausa entre solicitudes (más larga para evitar bloqueos)
max_retries = 3  # Número máximo de reintentos por texto
char_limit = 1000  # Límite de caracteres para traducción (reducido para esta API)

start_time = time.time()
total_translated = 0

# Abrir archivo de log
error_log = open(error_log_path, "a", encoding="utf-8")

# Caché para evitar traducir textos repetidos
translation_cache = {}

# Pool de traductores para evitar sobrecargar un solo cliente
# La biblioteca translate es más simple, no necesita múltiples instancias
translator = Translator(to_lang="es", from_lang="en")

# Función de traducción
def translate_text(text):
    """Traduce texto usando la biblioteca translate con manejo de errores"""
    global error_log, translation_cache
    
    # Verificar caché primero
    if text.strip() in translation_cache:
        return translation_cache[text.strip()]
    
    if not text.strip():
        return ""
    
    # Implementar backoff exponencial para manejar límites de API
    max_attempts = 5
    wait_time = 2  # segundos iniciales
    
    for attempt in range(max_attempts):
        try:
            # Dividir por párrafos si el texto es largo
            if len(text) > char_limit:
                paragraphs = text.split('\n')
                translated_parts = []
                
                for paragraph in paragraphs:
                    if paragraph.strip():
                        # Dividir párrafos largos en oraciones
                        sentences = [s.strip() + '.' for s in paragraph.split('.') if s.strip()]
                        paragraph_parts = []
                        
                        for sentence in sentences:
                            if len(sentence) > char_limit:
                                # Dividir aún más si es necesario
                                chunks = [sentence[i:i+char_limit] for i in range(0, len(sentence), char_limit)]
                                for chunk in chunks:
                                    translation = translator.translate(chunk)
                                    paragraph_parts.append(translation)
                                    time.sleep(1)  # Pausa entre chunks
                            else:
                                translation = translator.translate(sentence)
                                paragraph_parts.append(translation)
                                time.sleep(0.5)  # Pausa entre oraciones
                                
                        translated_parts.append(' '.join(paragraph_parts))
                
                result = '\n'.join(translated_parts)
            else:
                result = translator.translate(text.strip())
            
            # Guardar en caché y devolver
            translation_cache[text.strip()] = result
            return result
            
        except Exception as e:
            error_log.write(f"Error de traducción (intento {attempt+1}): {str(e)}\n")
            
            # Para cualquier error, esperar y reintentar
            wait_time *= 2  # Backoff exponencial
            time.sleep(wait_time)
    
    # Si todos los intentos fallan, devolver el texto original
    return text

# Función para traducir un lote de textos
def translate_batch(indices, dataframe):
    results = {}
    for idx in indices:
        source_text = str(dataframe.loc[idx, 'text']).strip()
        if source_text and (pd.isna(dataframe.loc[idx, 'text_es']) or dataframe.loc[idx, 'text_es'] == ""):
            try:
                results[idx] = translate_text(source_text)
                # Pausa para evitar límites de tasa
                time.sleep(random.uniform(1.0, 2.0))
            except Exception as e:
                results[idx] = f"ERROR: {str(e)}"
    return results

# Manejar señales de interrupción para guardar progreso
def signal_handler(sig, frame):
    print("\nInterrupción detectada, guardando progreso...")
    df.to_csv(output_path, index=False)
    print(f"Progreso guardado en {output_path}. Saliendo...")
    if 'error_log' in locals() and not error_log.closed:
        error_log.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    # Código principal
    print(f"Iniciando traducción con biblioteca 'translate'...")
    with ThreadPoolExecutor(max_workers=1) as executor:  # Un solo hilo para evitar bloqueos
        for i in tqdm(range(0, len(df), block_size), desc="Bloques procesados"):
            block_indices = list(range(i, min(i+block_size, len(df))))
            
            # Con un solo hilo, procesamos todos los índices directamente
            futures = [executor.submit(translate_batch, block_indices, df)]
            
            # Recoger resultados
            block_modified = False
            for future in tqdm(futures, desc="Procesando bloque", leave=False):
                results = future.result()
                for idx, translated_text in results.items():
                    if translated_text is None:
                        error_log.write(f"Error en fila {idx}: Resultado de traducción nulo\n")
                        df.loc[idx, 'text_es'] = "ERROR: Traducción fallida"
                    elif not isinstance(translated_text, str) or not translated_text.startswith("ERROR:"):
                        df.loc[idx, 'text_es'] = translated_text
                        block_modified = True
                        total_translated += 1
                    else:
                        error_log.write(f"Error en fila {idx}: {translated_text}\n")
            
            # Guardar después de cada bloque
            if block_modified:
                df.to_csv(output_path, index=False)
                print(f"Bloque {i//block_size+1} guardado. {total_translated} textos traducidos hasta ahora.")
            
            # Pausa entre bloques para evitar límites de API
            time.sleep(3)
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f'Traducción completa. Dataset guardado como {output_path}')
    print(f'Tiempo total de procesamiento: {elapsed:.2f} segundos')
    print(f'Total de textos traducidos: {total_translated}')

except Exception as e:
    print(f"Error en la ejecución: {str(e)}")
    # Guardar progreso en caso de error
    df.to_csv(output_path, index=False)
    print(f"Progreso guardado en {output_path} debido a un error.")

finally:
    # Cerrar archivo de log
    if 'error_log' in locals() and not error_log.closed:
        error_log.close()
    print(f'Errores de traducción guardados en {error_log_path}')