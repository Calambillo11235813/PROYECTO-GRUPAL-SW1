# TruthScan AI Audio Detection API -- README

Este documento explica cómo integrar y utilizar la **TruthScan AI Audio
Detection API**, que permite detectar si un audio fue generado o
manipulado por IA. Incluye autenticación, carga de archivos, análisis,
consulta de resultados y manejo de errores.

## 🚀 Características principales

-   Detección de audio generado por IA.
-   Workflow en 3 pasos: presigned URL → upload → detect.
-   Consulta de estado.
-   Manejo de créditos.
-   Formatos soportados: MP3, WAV, M4A, FLAC, OGG.

## 🔐 Autenticación

Incluye tu API key en el body:

    {
      "key": "YOUR_API_KEY"
    }

------------------------------------------------------------------------

# 🎧 AI Audio Detector -- Flujo en 3 Pasos

## 1️⃣ Obtener Pre-signed Upload URL

GET
`https://detect-audio.truthscan.com/get-presigned-url?file_name=example.mp3`

El filename **no debe tener espacios**.

## 2️⃣ Subir el Audio (PUT a presigned_url)

Content-Type debe coincidir con el formato: `audio/mp3`, `audio/wav`,
etc.\
Tamaño permitido: **1KB -- 10MB**.

## 3️⃣ Enviar Audio para Detección

POST `https://detect-audio.truthscan.com/detect`

Incluye: - key\
- url (file_path)\
- analyzeUpToSeconds (opcional)

Retorna un ID para consultar resultados.

------------------------------------------------------------------------

# 🔍 Consultar Resultados

POST `https://detect-audio.truthscan.com/query`

Estados: - pending - analyzing - done - failed

------------------------------------------------------------------------

# 💳 Revisar Créditos

GET `https://detect-audio.truthscan.com/check-user-credits`

------------------------------------------------------------------------

# 🩺 Health Check

GET `https://detect-audio.truthscan.com/health`

------------------------------------------------------------------------

# ❗ Errores Comunes

-   400 -- Bad Request\
-   403 -- API key inválida o sin créditos\
-   404 -- No encontrado\
-   405 -- Método no permitido\
-   422 -- Body inválido\
-   429 -- Demasiadas solicitudes\
-   500 -- Error del servidor\
-   503 -- Servicio no disponible

------------------------------------------------------------------------

# 🛠 Solución a Problemas

### API Key inválida

-   Revisa o regenera tu clave.

### Sin créditos

-   Consulta `/check-user-credits`.

### Formato no soportado

-   Usar: MP3, WAV, M4A, FLAC, OGG.

### Archivo demasiado grande

-   Máx 10MB.

### Upload falla

-   Usa la presigned URL inmediatamente.
-   Elimina espacios del nombre.
