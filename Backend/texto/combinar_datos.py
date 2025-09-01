"""
Script para combinar y etiquetar textos humanos e IA en un solo dataset para entrenamiento
"""
import os
import pandas as pd
from preprocesamiento import clean_text
from docx import Document
import pdfplumber

# Configura las rutas a tus carpetas de datos
human_folder = './data/human'  # Cambia según tu estructura
ia_folder = './data/ia'        # Cambia según tu estructura

# Función para cargar textos de una carpeta y asignar etiqueta
def load_and_label(folder_path, label):
    texts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        text = None
        if filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif filename.endswith('.docx'):
            try:
                doc = Document(file_path)
                text = '\n'.join([para.text for para in doc.paragraphs])
            except Exception as e:
                print(f'Error leyendo {filename}: {e}')
        elif filename.endswith('.pdf'):
            try:
                with pdfplumber.open(file_path) as pdf:
                    text = '\n'.join([page.extract_text() or '' for page in pdf.pages])
            except Exception as e:
                print(f'Error leyendo {filename}: {e}')
        if text:
            text = clean_text(text)
            texts.append({'text': text, 'label': label})
    return texts

# Cargar textos humanos e IA
human_texts = load_and_label(human_folder, 'human')
ia_texts = load_and_label(ia_folder, 'ia')

# Combinar y guardar en un solo CSV
all_texts = human_texts + ia_texts

df = pd.DataFrame(all_texts)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Mezclar aleatoriamente

df.to_csv('dataset_binario.csv', index=False)
print('Dataset combinado guardado como dataset_binario.csv')
