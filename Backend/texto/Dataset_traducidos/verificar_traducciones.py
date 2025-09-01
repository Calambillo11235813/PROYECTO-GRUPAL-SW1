"""
Script para verificar y corregir el estado de las traducciones
"""
import pandas as pd
import re
from tqdm import tqdm
import langdetect
from langdetect.lang_detect_exception import LangDetectException

# Rutas
input_path = r'D:\1.CARRERA UNIVERSITARIA\9. DECIMO SEMESTRE\1.INGIENERIA SOFTWARE 1\3.PROYECTOS\PROYECTO-GRUPAL-SW1\Backend\texto\dataset_binario_español.csv'
output_path = 'dataset_para_completar.csv'

# Cargar dataset
print(f"Cargando dataset desde {input_path}...")
df = pd.read_csv(input_path)
total_rows = len(df)
print(f"Total de filas: {total_rows}")

# Función para detectar idioma (con manejo de errores)
def detect_language(text, default='unknown'):
    if not isinstance(text, str) or not text.strip():
        return default
    
    try:
        return langdetect.detect(text[:1000])  # Usar solo los primeros 1000 caracteres
    except LangDetectException:
        return default

# Iniciar análisis detallado
print("\nAnalizando estado de las traducciones...")

# Crear nuevas columnas para análisis
df['es_vacio'] = df['text_es'].apply(lambda x: not isinstance(x, str) or not str(x).strip())
df['tiene_error'] = df['text_es'].apply(lambda x: isinstance(x, str) and 'ERROR' in str(x))

# Detectar idioma para una muestra de textos (para evitar que sea muy lento)
print("\nDetectando idioma en una muestra de textos...")
sample_indices = list(range(0, total_rows, 50))  # Analizar 1 de cada 50 filas
df['idioma_detectado'] = 'no_analizado'

for idx in tqdm(sample_indices):
    if idx < len(df):
        texto_es = str(df.loc[idx, 'text_es']).strip()
        if texto_es:
            df.loc[idx, 'idioma_detectado'] = detect_language(texto_es, default='desconocido')

# Encontrar casos donde la traducción es sospechosa (mismas palabras en inglés)
print("\nIdentificando traducciones sospechosas...")
df['es_sospechoso'] = False

for idx in tqdm(range(len(df))):
    texto_original = str(df.loc[idx, 'text']).strip().lower()
    texto_es = str(df.loc[idx, 'text_es']).strip().lower()
    
    if texto_es and len(texto_es) > 10:  # Solo verificar si hay contenido
        # Verificar si hay palabras en inglés que solo deberían estar en español
        english_indicators = ['the', 'and', 'this', 'with', 'that', 'for', 'you', 'have']
        english_count = sum(1 for word in english_indicators if f" {word} " in f" {texto_es} ")
        
        # Si tiene más de 2 indicadores de inglés, marcar como sospechoso
        if english_count >= 2:
            df.loc[idx, 'es_sospechoso'] = True
            
        # Si el texto original y la traducción son idénticos, marcar como sospechoso
        if texto_original == texto_es:
            df.loc[idx, 'es_sospechoso'] = True

# Estadísticas
vacios = df['es_vacio'].sum()
con_error = df['tiene_error'].sum()
sospechosos = df['es_sospechoso'].sum()
en_ingles = sum(1 for lang in df['idioma_detectado'] if lang == 'en')

print("\n=== RESULTADOS DEL ANÁLISIS ===")
print(f"Total de filas: {total_rows}")
print(f"Traducciones vacías: {vacios}")
print(f"Traducciones con error: {con_error}")
print(f"Traducciones sospechosas: {sospechosos}")
print(f"Muestra detectada en inglés: {en_ingles} de {len(sample_indices)} analizadas")

# Marcar filas que necesitan revisión
df['necesita_traduccion'] = df['es_vacio'] | df['tiene_error'] | df['es_sospechoso'] | (df['idioma_detectado'] == 'en')

pendientes = df['necesita_traduccion'].sum()
print(f"\nTotal de traducciones que necesitan revisión: {pendientes}")

# Guardar resultados para completar traducción
if pendientes > 0:
    print(f"\nGuardando dataset con marcadores para completar traducción en {output_path}")
    # Eliminar columnas temporales de análisis
    df_final = df.drop(columns=['es_vacio', 'tiene_error', 'es_sospechoso', 'idioma_detectado', 'necesita_traduccion'])
    # Marcar para retraducción (opcional, comentar si no quieres modificar el dataset)
    indices_a_retraducir = df[df['necesita_traduccion']].index
    for idx in indices_a_retraducir:
        df_final.loc[idx, 'text_es'] = ""  # Vaciar para que se retraduzca
    
    df_final.to_csv(output_path, index=False)
    print(f"Archivo guardado. Ejecuta el script de traducción nuevamente con este archivo.")
else:
    print("\nNo se encontraron traducciones pendientes según el análisis.")