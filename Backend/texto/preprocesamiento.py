import os
import pandas as pd
import re
from typing import List

# Funciones para cargar y limpiar textos

def load_texts_from_folder(folder_path: str) -> List[str]:
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                texts.append(f.read())
    return texts

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-záéíóúüñ\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Ejemplo de uso
if __name__ == "__main__":
    folder = "./data/human"
    texts = load_texts_from_folder(folder)
    cleaned_texts = [clean_text(t) for t in texts]
    df = pd.DataFrame({'text': cleaned_texts, 'label': 'human'})
    df.to_csv('human_texts_cleaned.csv', index=False)
