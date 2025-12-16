# Especificaciones Técnicas: Modelo de Detección de Deepfakes (Versión "B")

**ID del Modelo:** `modelo_deepfake_final_corregido.h5`  
**Tipo:** Red Neuronal Convolucional (CNN) con Transfer Learning  
**Arquitectura Base:** Xception  
**Estado:** Producción (Ganador del Benchmark Sprint 3)  
**Fecha de Entrenamiento:** Diciembre 2025  

---

## 1. Resumen Ejecutivo
El "Modelo B" es un clasificador binario diseñado para distinguir entre rostros humanos reales y rostros manipulados digitalmente (*Deepfakes*). Utiliza una estrategia de **Aprendizaje por Transferencia (Transfer Learning)** basada en la arquitectura Xception, optimizada mediante un proceso de entrenamiento en dos fases (Warm-up + Fine-Tuning) para mitigar el sobreajuste y mejorar la generalización en videos de alta compresión.

## 2. Arquitectura del Modelo

### 2.1. Backbone (Extractor de Características)
* **Red Base:** **Xception** (Extreme Inception).
* **Pesos Iniciales:** Pre-entrenados en **ImageNet**.
* **Justificación:** Xception es el estándar académico para la detección de manipulaciones faciales debido a su capacidad para identificar artefactos de compresión y patrones de ruido imperceptibles para el ojo humano.
* **Capas:** 126 capas profundas (Depthwise Separable Convolutions).

### 2.2. Cabezal de Clasificación (Custom Head)
Se sustituyó la capa final de ImageNet por una estructura personalizada para este problema:
1.  **GlobalAveragePooling2D:** Reducción de dimensionalidad espacial.
2.  **Dense Layer:** 256 neuronas (Activación: `ReLU`).
3.  **Dropout:** Tasa de `0.5` (50%) para regularización y prevención de *overfitting*.
4.  **Output Layer:** 1 neurona (Activación: `Sigmoid`).
    * `0.0` $\rightarrow$ Real
    * `1.0` $\rightarrow$ Fake

## 3. Estrategia de Entrenamiento

A diferencia de un entrenamiento estándar, este modelo utilizó una estrategia quirúrgica de dos etapas para maximizar la estabilidad:

### Fase 1: Calentamiento (Warm-Up)
* **Configuración:** Backbone Xception **totalmente congelado**.
* **Objetivo:** Entrenar exclusivamente el cabezal de clasificación para que los pesos aleatorios iniciales no destruyan el conocimiento pre-entrenado de la red base.
* **Optimizador:** Adam (`lr=0.001`).

### Fase 2: Sintonía Fina (Fine-Tuning)
* **Configuración:** Se descongelaron las **últimas 15 capas** de Xception.
* **Objetivo:** Adaptar los detectores de características de alto nivel a las texturas específicas de los deepfakes (bordes difusos, inconsistencias de iluminación).
* **Optimizador:** Adam con tasa de aprendizaje reducida (`lr=1e-5`) para ajustes microscópicos.
* **Callback:** `EarlyStopping` para detener el entrenamiento al detectar divergencia en la validación.

## 4. Dataset de Entrenamiento

El modelo fue entrenado con un dataset híbrido (~4,300 imágenes) procesado mediante **MTCNN**:

| Clase | Fuente | Descripción |
| :--- | :--- | :--- |
| **0 (Real)** | FaceForensics++ (YouTube) | Videos originales de noticias y entrevistas. |
| **1 (Fake)** | Deepfakes (Clásico) | Generación mediante Autoencoders (2017). |
| **1 (Fake)** | FaceShifter (Moderno) | Generación de alta fidelidad con gestión de oclusiones. |
| **1 (Fake)** | Manual Injection | Inclusión de casos extremos ("Video Morgan Freeman"). |

## 5. Métricas de Desempeño (Prueba de Inferencia)

Resultados obtenidos en el test de validación final con videos no vistos durante el entrenamiento:

### Comportamiento General
* **Robustez en Reales:** El modelo es conservador. Ante videos legítimos, mantiene puntuaciones muy bajas (< 0.20), minimizando los Falsos Positivos.
* **Decisión en Fakes:** Muestra alta confianza (> 0.75) en deepfakes evidentes y modernos.

### Tabla de Resultados (Muestra Representativa)
| Video de Prueba | Tipo Real | Predicción Promedio | Veredicto | Confianza |
| :--- | :--- | :--- | :--- | :--- |
| `654.mp4` | REAL | **0.17** | ✅ CORRECTO | Alta |
| `716.mp4` | REAL | **0.06** | ✅ CORRECTO | Muy Alta |
| `134_192.mp4` | FAKE | **0.78** | ✅ CORRECTO | Alta |
| `481_469.mp4` | FAKE | **0.90** | ✅ CORRECTO | Muy Alta |

## 6. Especificaciones de Entrada/Salida

Para integrar este modelo en el Backend (Django):

* **Input Shape:** `(224, 224, 3)` (RGB).
* **Preprocesamiento Requerido:**
    1.  Detección y recorte de rostro.
    2.  Resize a `224x224`.
    3.  Normalización de píxeles: `imagen / 255.0` (Valores entre 0 y 1).
* **Interpretación de Salida:**
    * Score $< 0.5$ $\rightarrow$ **VIDEO REAL**
    * Score $\ge 0.5$ $\rightarrow$ **DEEPFAKE**

## 7. Dependencias de Software
* TensorFlow / Keras >= 2.10
* OpenCV (para extracción de frames)
* MTCNN (para detección facial)
* H5py (para carga del modelo)