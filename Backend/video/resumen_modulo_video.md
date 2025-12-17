# Resumen del Módulo `video`

## Responsabilidades
- Gestión de subidas de video (`VideoUpload`) y su estado.
- Extracción de rostros por frames y análisis de deepfake mediante un modelo Keras (`modelo_deepfake_final_corregido.h5`).
- Exposición de endpoints REST para subir, listar y disparar análisis, además de consultar resultados.

## Rutas (DRF Router)
- `videoupload/` → CRUD de cargas de video (`VideoUploadViewSet`).
  - Acción `POST videoupload/{id}/analyze/` para ejecutar el análisis.
- `analysisresult/` → lectura de resultados (`AnalysisResultViewSet`).

## Modelos
- `VideoUpload`: archivo subido, metadatos (`size`, `duration_seconds`, `original_filename`), usuario (`uploaded_by`) y estado (`pending|processing|done|error`). Ruta de subida controlada por `settings.RUTA_SUBIDA_VIDEOS`.
- `VideoFrame`: frames extraídos (imagen en `media/frames/`), únicos por `video+frame_number`.
- `AnalysisResult`: resultado del modelo (`score`, `verdict`, `details`, `created_at`, `model_name`).

## Serializers
- `VideoUploadSerializer`: expone campos clave y deja `uploaded_by`, `size`, `status` como solo lectura.
- `VideoFrameSerializer`: CRUD de frames.
- `AnalysisResultSerializer`: lectura de resultados.

## Vistas
- `VideoUploadViewSet`:
  - `perform_create`: guarda `uploaded_by` si hay usuario, intenta setear `size` y `original_filename`.
  - `@action analyze`: ejecuta `DeepfakeDetector.predict(video_path)`, crea `AnalysisResult`, actualiza estado del `VideoUpload`.
- `AnalysisResultViewSet`: solo lectura, ordenado por `created_at` descendente.

## Utilidades (`deepfake_utils.py`)
- `DeepfakeDetector`:
  - Carga modelo Keras desde `Model_deepfake/modelo_deepfake_final_corregido.h5`.
  - Usa `MTCNN` para detectar rostros.
  - `extract_faces(video_path, max_frames=32)`: muestrea frames uniformemente, recorta y normaliza a 224x224.
  - `predict(video_path)`: normaliza `[0,1]`, predice por lote, promedia → `score` y `verdict` (`DEEPFAKE` si `score>=0.5`, si no `REAL`).

## Flujo de Datos
1) Subida de video (`videoupload/`) → persistencia en `media/videos/` (o ruta definida).
2) Acción `analyze` → extracción de rostros → predicción con modelo Keras.
3) Creación de `AnalysisResult` y actualización del estado del `VideoUpload`.
4) Consulta de resultados via `analysisresult/`.

## Dependencias y Consideraciones
- Requiere `tensorflow.keras`, `opencv-python`, `mtcnn`, `numpy`.
- Carga de modelo en cada instancia del detector; considerar cacheo único o carga perezosa para rendimiento.
- `duration_seconds` no se calcula actualmente; opcionalmente extraer con OpenCV.
- `uploaded_by` opcional, pero ideal proteger endpoints con JWT (`IsAuthenticated`).
- Manejo de errores básico; considerar registro en `logs/` y estados detallados (`processing`).

## Riesgos/Optimización
- Coste de CPU/GPU en extracción MTCNN; añadir límite de tamaño/duración y colas de tareas.
- Validar tipo MIME y tamaño como en `settings.TIPOS_VIDEO_PERMITIDOS`/`TAMANO_MAXIMO_VIDEO`.
- Persistir frames representativos en `VideoFrame` para auditoría.
- Endpoint de healthcheck del modelo (load ok, pesos presentes).
- Soporte de batch y reintentos si falla lectura de frames.
