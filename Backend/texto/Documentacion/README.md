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

## Paso 1: Definición del Problema y Objetivos ✓

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

## Paso 2: Recopilación y Preparación de Datos ✓

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

## Paso 3: Ingeniería de Características ✓

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

## Paso 4: Entrenamiento del Modelo ✓

**Estado:** ✅ Completado en Google Colab

### Infraestructura
- **Hardware:** GPU Tesla T4
- **Batch size:** 32

### Datos
- **Dataset:** 26,117 muestras
- **Archivos utilizados:**
  - `Training_Essay_Data.csv`
  - `dataset_completo_traducido.csv`

### Modelo
- **Base:** BERT Multilingüe (`bert-base-multilingual-cased`)
- **Arquitectura:** Modelo BERT con capa de clasificación binaria
- **Tokenizer:** Tokenizador BERT estándar

### Proceso de Entrenamiento
- **Épocas:** 4
- **Pasos totales:** 2,612
- **Tiempo de entrenamiento:** 42 minutos 15 segundos

### Métricas Finales
Los resultados del entrenamiento fueron excepcionales:
- **Precisión (Accuracy):** 0.9939 (99.39%)
- **Loss:** 0.0310
- **Métricas adicionales en último paso:**
  - **F1-Score:** ~0.992
  - **Precision:** ~0.993
  - **Recall:** ~0.992

### Artefactos Generados
El modelo y sus componentes se guardaron en la carpeta `modelo_deteccion_ia/`:
- `config.json`: Configuración del modelo
- `model.safetensors`: Pesos del modelo entrenado
- `special_tokens_map.json`: Mapeo de tokens especiales
- `tokenizer.json`: Configuración del tokenizador
- `vocab.txt`: Vocabulario del modelo

---

## Instalación de dependencias y entorno virtual

1. **Crea y activa un entorno virtual (recomendado):**

En Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

