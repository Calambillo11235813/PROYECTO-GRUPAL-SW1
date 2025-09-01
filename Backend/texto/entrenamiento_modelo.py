"""
Entrenamiento de modelo de clasificación binaria para distinguir textos humanos de textos generados por IA
"""
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

# Cargar datos preprocesados (ajusta el path según tu flujo)
df = pd.read_csv('human_texts_cleaned.csv')  # Cambia por tu dataset combinado
texts = df['text'].tolist()
labels = df['label'].map({'human': 0, 'ia': 1}).tolist()  # Ajusta si tienes ambas clases

# Tokenización
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
encodings = tokenizer(texts, truncation=True, padding=True, max_length=256)

class TextDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)

# División en train/val
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=256)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=256)
train_dataset = TextDataset(train_encodings, train_labels)
val_dataset = TextDataset(val_encodings, val_labels)

# Modelo
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Entrenamiento
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=2,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    logging_dir='./logs',
    logging_steps=10,
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)
trainer.train()

# Guardar modelo
model.save_pretrained('./modelo_binario')
tokenizer.save_pretrained('./modelo_binario')
