# Backend —visión general y puntos clave

## Apps principales
- texto: detección de IA en texto. Contiene `views.py`, `predictor.py`, `file_processor.py`, `models.py`.
- audio: subida y análisis de audio (espectrogramas, RF model). Contiene `rf_model.py`, `ia_model.py`, `utils.py`.
- usuario: endpoints de usuario y serializers (auth / perfiles).

## ML / Artefactos
- content/rf_v1/model_rf.joblib — modelo RandomForest.
- modelo_deteccion_ia_* — carpetas con modelos/configs por versión.

## Flujo de datos (simplificado)
1. Frontend realiza POST a `/api/texto/...` o upload a audio endpoint.
2. Serializer valida request y crea/almacena el archivo si aplica.
3. File processor / utils extraen texto o generan espectrograma.
4. Predictor / rf_model cargan modelo y calculan probabilidades.
5. Resultado se devuelve como JSON y se persiste metadatos en la BD.

## Archivos importantes
- Backend/settings.py — configuración global (cargar vars de .env).
- Backend/urls.py — punto de entrada de rutas.
- texto/predictor.py, audio/rf_model.py — lógica de inferencia.
- logs/audio_analysis.log — registro de actividades.

## Integración con frontend
- Endpoints esperados: `/api/texto/analizar/`, `/api/texto/analizar-archivo/`, `/api/texto/comparar/`, `/api/texto/estado/`.
- Asegurar VITE_API_URL en frontend y CORS en backend.

## Recomendaciones rápidas
- Añadir `Backend/.env.example` con VITE_API_URL, TIMEOUT, MAX_UPLOAD_SIZE.
- Documentar API (curl + examples) en `docs/API_BACKEND.md`.
- Añadir validación estricta de archivos (size/type) y límites en settings.
- Añadir health-check para modelos y endpoint `/api/texto/estado/`.
- Añadir pruebas unitarias para predictor y manejo de edge-cases (texto vacío, archivos corruptos).
- Considerar mover inferencia pesada a tareas asíncronas (Celery) para evitar timeouts.
