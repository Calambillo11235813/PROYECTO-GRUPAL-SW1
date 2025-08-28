# Módulo de Detección de Texto IA

## Paso 1: Definición del Problema y Objetivos

**Objetivo:**
Crear un modelo de clasificación binaria que, dado un texto, lo etiquete como "Humano" o "Generado por IA".

**Modelos de IA a detectar:**
- GPT-3.5
- GPT-4
- Llama 2
- Claude

**Tipos de texto a analizar:**
- Ensayos académicos
- Noticias
- Posts de redes sociales
- Correos electrónicos

**Métricas clave:**
- Precisión (Precision): De todos los textos que el modelo dijo ser IA, ¿cuántos realmente lo eran?
- Exhaustividad (Recall): De todos los textos que son IA, ¿cuántos logró encontrar el modelo?
- Puntuación F1 (F1-Score): Media armónica de Precisión y Exhaustividad.
- Área bajo la curva ROC (AUC-ROC): Mide la capacidad del modelo para distinguir entre las dos clases.

**Importancia:**
Priorizar la minimización de falsos positivos (texto humano marcado como IA), ya que pueden acusar erróneamente a una persona.

---

## Paso 2: Recopilación y Preparación de Datos

La calidad de los datos es fundamental para el éxito del modelo. Este paso incluye:

### 1. Fuentes de Datos Humanos
- Libros y artículos (ej. Proyecto Gutenberg, arXiv, Wikipedia).
- Redes sociales (posts y comentarios de Reddit, Twitter, cumpliendo políticas de privacidad).
- Conjuntos de datos públicos (ej. HC3, datasets de ensayos estudiantiles).

### 2. Fuentes de Datos Generados por IA
- Generación propia usando APIs de OpenAI (GPT), Anthropic (Claude), Meta (Llama).
- Para cada prompt, generar texto humano y texto IA para crear pares equilibrados.
- Conjuntos de datos públicos (ej. HC3, datasets en Hugging Face).

### 3. Preprocesamiento y Etiquetado
- Limpieza: Normalizar texto, eliminar caracteres especiales (con cuidado).
- Tokenización: Dividir texto en palabras/subpalabras (ej. BertTokenizer, GPT2Tokenizer).
- Balanceo: Asegurar número similar de ejemplos por clase.
- División: Separar datos en entrenamiento (70-80%), validación (10-15%) y pruebas (10-15%).

---

## Paso 3: Ingeniería de Características

Además del texto crudo, se recomienda extraer características específicas para mejorar el rendimiento del modelo:

### Características Estilísticas
- Perplejidad: Mide cuán "sorprendido" está un modelo de lenguaje al ver el texto. Los textos de IA suelen tener perplejidad más baja.
- Burstiness: Variación en longitud y estructura de oraciones. El texto humano tiende a ser más variable.
- Diversidad léxica: Ratio de palabras únicas sobre el total de palabras (TTR).
- Longitud promedio de palabras y oraciones.

### Características Estadísticas
- Frecuencia de palabras funcionales (el, de, que, y, en...).
- Patrones de posicionamiento de palabras.

### Embeddings de Texto
- Usar modelos preentrenados como BERT o Sentence-Transformers para convertir textos en vectores numéricos densos.

---

## Instalación de dependencias y entorno virtual

1. **Crea y activa un entorno virtual (recomendado):**

En Windows PowerShell:
```powershell

python -m venv venv
.\venv\Scripts\Activate
```

2. **Instala las dependencias usando el archivo `requirements.txt`:**

Agrega las siguientes líneas al archivo `requirements.txt`:
```
pandas
numpy
scikit-learn
transformers
torch
```
Luego instala todo con:
```powershell
pip install -r requirements.txt
```

Asegúrate de tener Python 3.8 o superior.

---

## Contexto actual del desarrollo

Hasta este punto se han realizado los siguientes avances:
- Definición clara del problema y objetivos del módulo de detección de texto IA.
- Documentación de las fuentes de datos, preprocesamiento y balanceo de clases.
- Ingeniería de características recomendada para el modelo.
- Instrucciones para la creación de entorno virtual y la instalación de dependencias usando `requirements.txt`.
- Archivo `requirements.txt` actualizado con todas las librerías necesarias.
- Script inicial de preprocesamiento creado.

**Próximo paso:**
Documentar y desarrollar la elección y entrenamiento del modelo de clasificación binaria (por ejemplo, usando BERT, RoBERTa, etc.)

Este contexto servirá como referencia para continuar el desarrollo mañana.

---

En el siguiente paso se documentará la elección y entrenamiento del modelo.

Este archivo se irá actualizando conforme avancemos en el desarrollo del módulo.
