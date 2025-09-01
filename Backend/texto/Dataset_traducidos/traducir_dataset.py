"""
Script para traducir dataset_binario.csv (inglés) a español usando DeepL
"""
import pandas as pd
from tqdm import tqdm
import time
import deepl
import os

# Tu clave de API de DeepL
DEEPL_AUTH_KEY = "0b88b"  # Reemplaza con tu clave

translator = deepl.Translator(DEEPL_AUTH_KEY)

input_path = r'D:\1.CARRERA UNIVERSITARIA\9. DECIMO SEMESTRE\1.INGIENERIA SOFTWARE 1\3.PROYECTOS\PROYECTO-GRUPAL-SW1\Backend\texto\Dataset\Training_Essay_Data.csv'
output_path = 'dataset_binario_español.csv'
error_log_path = 'errores_traduccion.log'

df = pd.read_csv(input_path)

# Asegura que la columna 'text' sea tipo string y no vacía
df['text'] = df['text'].astype(str)
df['text_es'] = ""  # Nueva columna para el texto traducido

block_size = 1000  # Ajusta según tu preferencia

start_time = time.time()

with open(error_log_path, "a", encoding="utf-8") as error_log:
    for i in range(0, len(df), block_size):
        block_indices = list(range(i, min(i+block_size, len(df))))
        for idx in block_indices:
            source_text = str(df.loc[idx, 'text'])
            # Solo traduce si el texto original no está vacío y aún no ha sido traducido
            if source_text.strip() != "" and (df.loc[idx, 'text_es'] == "" or pd.isna(df.loc[idx, 'text_es'])):
                try:
                    result = translator.translate_text(source_text, target_lang="ES")
                    df.loc[idx, 'text_es'] = result.text
                except Exception as e:
                    df.loc[idx, 'text_es'] = "ERROR"
                    error_log.write(f"Fila {idx}: {e}\nTexto: {source_text}\n\n")
        df.to_csv(output_path, index=False)
        print(f"Bloque {i//block_size+1} traducido y guardado.")

end_time = time.time()
elapsed = end_time - start_time
print(f'Traducción completa. Dataset guardado como {output_path}')
print(f'Tiempo total de procesamiento: {elapsed:.2f} segundos')
print(f'Errores de traducción guardados en {error_log_path}')
