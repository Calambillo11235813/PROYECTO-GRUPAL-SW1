


## Preparación y estructura del dataset binario

Para entrenar el modelo de clasificación, es necesario contar con un dataset combinado que incluya textos humanos y textos generados por IA, cada uno correctamente etiquetado.

**Formato recomendado:**
- Archivo CSV con dos columnas: `text` (texto limpio) y `label` (`human` o `ia`).

**Script de combinación:**
Se ha creado el script `combinar_datos.py` en la carpeta `Backend/texto/` que:
1. Carga los textos desde las carpetas `data/human` y `data/ia`.
2. Limpia cada texto usando la función `clean_text`.
3. Asigna la etiqueta correspondiente.
4. Combina y mezcla aleatoriamente los textos.
5. Guarda el resultado en `dataset_binario.csv`.

**Uso:**
1. Coloca los archivos `.txt` de textos humanos en `data/human` y los de IA en `data/ia`.
2. Ejecuta el script para generar el dataset listo para entrenamiento.

Este proceso asegura que el modelo reciba datos balanceados y correctamente etiquetados.
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

**Próximo paso completado:**

### Elección y entrenamiento del modelo de clasificación binaria

Se ha creado el script `entrenamiento_modelo.py` que realiza el entrenamiento de un modelo BERT para distinguir textos humanos de textos generados por IA. El proceso incluye:

1. **Selección del modelo base:** Se utiliza `bert-base-uncased` de Hugging Face Transformers.
2. **Carga de datos:** Se emplea el dataset preprocesado (`human_texts_cleaned.csv` o el dataset combinado).
3. **Tokenización:** Los textos se tokenizan y preparan para el modelo.
4. **División de datos:** Separación en conjuntos de entrenamiento y validación.
5. **Entrenamiento:** Se ajusta el modelo usando la clase `Trainer` de Transformers.
6. **Guardado:** El modelo y el tokenizador se guardan en la carpeta `modelo_binario`.

#### Script de referencia
El script se encuentra en `Backend/texto/entrenamiento_modelo.py` y puede adaptarse según el dataset y los parámetros específicos del proyecto.

**Siguientes pasos:**
- Evaluar el modelo entrenado y documentar los resultados.
- Integrar el modelo en una API REST para predicción en tiempo real.

Este archivo se irá actualizando conforme avancemos en el desarrollo del módulo.

---

# Proyecto de Procesamiento de Textos

## Estado Actual del Desarrollo

El proyecto se encuentra actualmente en la fase de preparación de datos para el entrenamiento del modelo. A continuación se detalla el progreso hasta la fecha y los próximos pasos a seguir.

### Progreso Actual

1. ✅ Obtención del dataset inicial en inglés (`Dataset/Training_Essay_Data.csv`)
2. ✅ Creación de scripts para traducción del dataset al español
3. ✅ División del dataset en partes traducidas y pendientes:
   - `dataset_parte_traducida.csv`: Contiene ~3,028 filas ya traducidas
   - `dataset_parte_pendiente.csv`: Contiene ~26,117 filas pendientes de traducir

### Punto de Parada

El desarrollo se ha detenido temporalmente debido a:
- Limitaciones en las APIs gratuitas de traducción que impiden procesar grandes volúmenes de texto
- Errores de compatibilidad entre las bibliotecas de traducción y la versión de Python (3.11+)

## Cómo Continuar el Desarrollo

### 1. Completar la Traducción del Dataset

Para continuar con la traducción del dataset pendiente, siga estos pasos:

```bash
# Activar el entorno virtual
cd Backend
.\venv\Scripts\activate

# Ejecutar el script de traducción mejorado
cd texto\Dataset_traducidos
python traducir_dataset_mejorado.py
```
