# ANÁLISIS PROFUNDO DEL BACKEND - PROYECTO KLDC
**Fecha:** 19 de Noviembre de 2025  
**Rama:** codigo  
**Propósito:** Documentación completa de la arquitectura, flujos y patrones del backend

---

## 📋 ÍNDICE
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura General](#arquitectura-general)
3. [Componentes Principales](#componentes-principales)
4. [Flujos de Datos](#flujos-de-datos)
5. [Modelos de Base de Datos](#modelos-de-base-de-datos)
6. [APIs y Endpoints](#apis-y-endpoints)
7. [Integración con ML/IA](#integracion-con-ml-ia)
8. [Seguridad y Autenticación](#seguridad-y-autenticacion)
9. [Configuración y Deployment](#configuracion-y-deployment)
10. [Patrones y Buenas Prácticas](#patrones-y-buenas-practicas)
11. [Áreas de Mejora](#areas-de-mejora)

---

## 🎯 RESUMEN EJECUTIVO

### Propósito del Sistema
Backend Django REST Framework para detección de contenido generado por IA en tres modalidades:
- **Texto:** Análisis de documentos y texto directo
- **Audio:** Verificación de autenticidad de archivos de audio
- **Código:** Detección de código generado por IA (implementado)

### Stack Tecnológico
- **Framework:** Django 5.2.8 + Django REST Framework
- **Base de Datos:** PostgreSQL 14
- **ML/IA:** PyTorch, Transformers (BERT), Scikit-learn (Random Forest)
- **Procesamiento:** Librosa (audio), PyPDF2, python-docx (documentos)
- **Autenticación:** JWT (Simple JWT)
- **Contenedores:** Docker + Docker Compose

---

## 🏗️ ARQUITECTURA GENERAL

### Estructura Modular (Apps Django)

```
Backend/
├── Backend/              # Configuración principal del proyecto
│   ├── settings.py       # Configuración global
│   ├── urls.py          # Enrutamiento principal
│   ├── wsgi.py          # WSGI application
│   └── asgi.py          # ASGI application (async)
│
├── usuario/             # Gestión de usuarios y autenticación
│   ├── models.py        # CustomUser, UserProfile
│   ├── views.py         # Register, Login, Logout
│   └── serializers.py   # Validación de datos
│
├── texto/               # Detección de IA en texto
│   ├── models.py        # AnalisisTexto, ArchivoAnalisis
│   ├── views.py         # Endpoints de análisis
│   ├── predictor.py     # Lógica de predicción con BERT
│   ├── file_processor.py # Extracción de texto (PDF, DOCX, TXT)
│   └── preprocesamiento.py # Limpieza y normalización
│
├── audio/               # Detección de IA en audio
│   ├── models.py        # AudioUpload
│   ├── views.py         # Subida y análisis
│   ├── rf_model.py      # Random Forest Detector
│   ├── ia_model.py      # Verificación de autenticidad
│   ├── utils.py         # Generación de espectrogramas
│   └── certificado_utils.py # Generación de PDFs
│
├── codigo/              # Detección de IA en código (implementado)
│   ├── models.py        # AnalisisCodigo (registro completo de análisis)
│   ├── views/           # Subir, historial, comparar, reporte, detalle
│   ├── serializers.py   # Serializadores para salida detallada
│   └── utils/           # Analizador AST, detector HF, heurísticas línea
│
├── content/             # Modelos ML preentrenados
│   └── rf_v1/           # Random Forest v1
│       ├── model_rf.joblib
│       └── manifest.json
│
└── tests/               # Tests del sistema
    ├── test_env.py
    ├── test_file_upload.py
    └── test_upload_complete.py
```

### Patrones de Diseño Identificados

1. **MVC/MVT Pattern** (Model-View-Template de Django)
   - Separación clara entre modelos, vistas y lógica de negocio

2. **Repository Pattern**
   - Acceso a datos mediante Django ORM
   - Abstracción de consultas en managers

3. **Service Layer Pattern**
   - `predictor.py`: Servicios de predicción
   - `file_processor.py`: Servicios de procesamiento
   - `rf_model.py`: Servicios de ML

4. **Singleton Pattern**
   - Cache de modelos ML en memoria (predictors globales)
   - Evita recargar modelos pesados en cada request

5. **Factory Pattern**
  - `get_predictor(model_type)`: Factory para crear predictores

---

## 🔗 Interacciones Entre Componentes

- **Usuario ↔ Audio:** `AudioUpload.user` referencia a `usuario.CustomUser`. En guardados se actualiza el conteo en `UserProfile.total_analyses` (intención del modelo); endpoints de audio requieren JWT (`IsAuthenticated`).
- **Usuario ↔ Texto:** `AnalisisTexto`/`ArchivoAnalisis` se crean sin usuario (público), pero el modelo soporta asociar usuario si se agrega autenticación en vistas de `texto/`.
- **Usuario ↔ Código:** `AnalisisCodigo.usuario` asocia análisis al usuario si está autenticado al subir.
- **Core Settings:** `settings.py` centraliza validaciones (tipos MIME, tamaños), logging (logger "audio"), CORS y JWT. `AUTH_USER_MODEL='usuario.CustomUser'` definido antes de migraciones.
- **ML Compartido:** Carga perezosa y cacheada: `texto/predictor.get_predictor` y `audio/rf_model`. Fallbacks de tokenizador/modelo para robustez.
- **Media/Logs:** Archivos y espectrogramas por usuario en `media/audios/user_{id}/` y `media/plots/user_{id}/`. Logs en `logs/audio_analysis.log`.

---

## 🔧 COMPONENTES PRINCIPALES

### 1. USUARIO - Sistema de Autenticación

#### Modelo de Datos
```python
CustomUser (AbstractUser):
  - email: EmailField (unique, USERNAME_FIELD)
  - username: CharField
  - first_name, last_name: CharField
  - is_verified: Boolean
  - created_at, updated_at: DateTimeField

UserProfile (1-to-1 con CustomUser):
  - bio: TextField
  - avatar: ImageField
  - total_analyses: IntegerField
  - premium_until: DateTimeField
```

#### Endpoints
```
POST /api/auth/register/     - Registro de usuarios
POST /api/auth/login/        - Autenticación
POST /api/auth/logout/       - Cierre de sesión
GET  /api/auth/profile/      - Obtener perfil
GET  /api/auth/users/        - Listar usuarios
```

#### Flujo de Autenticación
```
1. Cliente envía email + password
2. UserLoginSerializer valida credenciales
3. Se genera RefreshToken y AccessToken (JWT)
4. Se retorna user data + tokens
5. Cliente almacena tokens (localStorage)
6. Requests subsecuentes incluyen: Authorization: Bearer <token>
```

---

### 2. TEXTO - Detección de IA en Documentos

#### Modelos ML Disponibles
- **Modelo B (Principal):** `modelo_deteccion_ia_B/`
  - Base: BERT fine-tuned
  - Vocab size: ~30K tokens
  - Max length: 512 tokens

- **Modelo N (Experimental):** `modelo_deteccion_ia_N/`
  - Base: BERT alternativo
  - Configuración experimental

#### Arquitectura del Predictor

```python
TextoPredictor:
  __init__(model_type='B'):
    - Carga modelo y tokenizer
    - Configura device (CPU/GPU)
    - Max length: 512 tokens
  
  predict(text):
    1. Tokenización con padding/truncation
    2. Forward pass (sin gradientes)
    3. Softmax sobre logits
    4. Extracción de probabilidades
    5. Retorno de resultado estructurado
```

#### Flujo de Análisis

**Análisis de Texto Directo:**
```
POST /api/texto/analizar/
├── Validar texto no vacío
├── get_predictor(modelo_tipo)
├── predictor.predict(texto)
├── Calcular confianza (ALTA/MEDIA/BAJA)
├── Crear registro en AnalisisTexto
└── Retornar resultado JSON
```

**Análisis de Archivo:**
```
POST /api/texto/analizar-archivo/
├── Validar archivo (tipo, tamaño)
├── FileProcessor.extract_text()
│   ├── TXT: Múltiples encodings
│   ├── PDF: PyPDF2.PdfReader
│   └── DOCX: python-docx
├── Dividir en fragmentos (300 palabras)
├── Predicción por fragmento
├── Consenso: mayoría de fragmentos
├── Calcular hash SHA256
├── Guardar AnalisisTexto + ArchivoAnalisis
└── Retornar resultado agregado
```

**Comparación de Modelos:**
```
POST /api/texto/comparar/
├── Obtener predictor_N y predictor_B
├── Predicción paralela con ambos
├── Calcular diferencia de probabilidades
├── Determinar consenso (SI/NO)
└── Retornar comparativa detallada
```

#### Características Clave

1. **Multi-encoding Support:** UTF-8, Latin-1, CP1252
2. **Fragment Processing:** Textos largos divididos en chunks
3. **Confidence Calculation:**
   - ALTA: ≥80% probabilidad
   - MEDIA: 60-79%
   - BAJA: <60%
4. **File Hash:** Prevención de duplicados
5. **Model Fallback:** Sistema robusto de carga de modelos

---

### 3. AUDIO - Verificación de Autenticidad

#### Modelo de Machine Learning

**Random Forest Audio Detector** (`rf_model.py`)
```python
RFAudioDetector:
  Configuración:
    - sr: 16000 Hz (sample rate)
    - window_size: 3.0s
    - hop_size: 1.5s
    - n_mfcc: 20
    - n_mels: 64
    
  Feature Extraction (144 features):
    - 20 MFCCs + deltas + delta-deltas (120 features)
    - Zero Crossing Rate (ZCR)
    - Spectral Centroid
    - Spectral Flatness
    - RMS Energy
    - Spectral Rolloff (85%, 95%)
    - Spectral Flux
    
  Decision Logic:
    - Segmentación del audio
    - Predicción por segmento
    - Umbrales: ia_thresh_seg=0.55, ia_thresh_audio=0.60
    - Decisión final: AND logic (avg_ia Y pct_segments)
```

#### Flujo de Análisis de Audio

```
POST /api/audio/upload/
├── Validación MultiPartParser
├── AudioUploadSerializer.validate_file()
│   ├── Tipo de archivo (TIPOS_AUDIO_PERMITIDOS)
│   ├── Tamaño (MAX: 50MB)
│   └── Renombrado seguro (UUID)
├── Guardar archivo en media/audios/user_{id}/
├── verificar_autenticidad(audio_path)
│   ├── Cargar audio con librosa
│   ├── Segmentar (ventanas de 3s, hop 1.5s)
│   ├── Extraer features por segmento
│   ├── Predicción RF por segmento
│   ├── Calcular avg_ia, avg_real, pct_ia
│   └── Decisión final (IA/REAL)
├── generar_espectrograma()
│   ├── Mel-spectrogram con librosa
│   ├── Guardar en media/plots/user_{id}/
│   └── Matplotlib backend: Agg (sin GUI)
├── Actualizar AudioUpload con resultados
└── Retornar AudioUploadSerializer
```

#### Generación de Certificados

```python
generar_certificado_pdf(audio_upload):
  - ReportLab para generación PDF
  - Información del análisis
  - Timestamp y ID único
  - Resultado y probabilidad
  - Imagen del espectrograma embebida
```

#### Endpoints
```
POST /api/audio/upload/            - Subir y analizar audio
GET  /api/audio/                   - Historial del usuario autenticado
GET  /api/audio/upload/            - Historial global (admin/depuración)
GET  /api/audio/certificado/<id>/  - Descargar certificado PDF
POST /api/audio/token/             - Obtener JWT (duplicado respecto a /api/auth/)
POST /api/audio/token/refresh/     - Refrescar JWT
```

---

### 4. CÓDIGO - Detección de IA en Código (Implementado)

#### Estado Actual
- Implementado con modelo `AnalisisCodigo` que almacena: metadatos de archivo, resultado IA (bool + confianza + método + detalles), análisis sintáctico (AST, complejidad, patrones), líneas/bloques sospechosos y reportes (PDF/JSON), con `usuario` opcional (FK).
- Vistas separadas: subir archivo, historial con filtros, comparador, estadísticas, exportación JSON, reporte PDF/JSON y detalle profesional.
- Detector HF cargado de forma perezosa (`CodeDetectorHF`) con fallback seguro si faltan pesos.

#### Endpoints (`/api/codigo/`)
```
GET  /                    - Panel HTML (vista principal)
POST /subir/              - Subir archivo y analizar
GET  /analisis/<id>/      - Detalle profesional del análisis
GET  /historial/          - Historial con filtros (nombre, lenguaje, IA, fechas)
GET  /historial/comparar/ - Comparar 2 análisis vía query (?id1=&id2=)
POST /historial/comparar/ - Comparar lista de IDs (JSON {ids:[]})
GET  /historial/estadisticas/ - KPIs y promedios
GET  /historial/exportar/ - Exportación JSON del historial
GET  /reporte/pdf/<id>/   - Reporte en PDF
GET  /reporte/json/<id>/  - Reporte JSON
```

#### Recursos de Modelo
```
codigo/code_detection-model-complete/
├── config.json
├── model.safetensors
├── tokenizer.json
├── vocab.json
└── USAGE_EXAMPLES.py
```

---

## 🔄 FLUJOS DE DATOS

### Flujo Completo: Análisis de Archivo de Texto

```
┌─────────────┐
│   Frontend  │
│  (React)    │
└──────┬──────┘
       │ POST /api/texto/analizar-archivo/
       │ FormData: {archivo: File, modelo: 'B'}
       ▼
┌──────────────────────────────────────────┐
│   Backend: texto/views.py                │
│   @csrf_exempt                           │
│   @require_http_methods(["POST"])        │
└──────┬───────────────────────────────────┘
       │
       ├─► Validar archivo en request.FILES
       │
       ├─► FileProcessor.validate_file()
       │   ├─ Verificar extensión (.txt, .pdf, .docx)
       │   ├─ Verificar tamaño (< 10MB)
       │   └─ Validar headers del archivo
       │
       ├─► FileProcessor.extract_text()
       │   ├─ .txt → decode con múltiples encodings
       │   ├─ .pdf → PyPDF2.PdfReader.extract_text()
       │   └─ .docx → Document(file).paragraphs + tables
       │
       ├─► dividir_en_fragmentos(texto, max=300)
       │   └─ Chunks de 300 palabras
       │
       ├─► Para cada fragmento:
       │   ├─ get_predictor(modelo_tipo)
       │   ├─ predictor.predict(fragmento)
       │   └─ Acumular resultados
       │
       ├─► Calcular consenso:
       │   ├─ num_ia vs num_humano
       │   ├─ Promedio de probabilidades
       │   └─ Determinar confianza
       │
       ├─► Calcular hash SHA256 del archivo
       │
       ├─► Crear registros en DB:
       │   ├─ AnalisisTexto (texto, predicción, probs)
       │   └─ ArchivoAnalisis (hash, metadata)
       │
       └─► Response JSON:
           {
             resultado: 'IA' | 'Humano',
             probabilidad_ia: float,
             probabilidad_humano: float,
             confianza: 'ALTA' | 'MEDIA' | 'BAJA',
             fragmentos_analizados: int,
             archivo_info: {...},
             analisis_id: int
           }
```

### Flujo Completo: Análisis de Audio

```
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │ POST /api/audio/
       │ FormData: {file: AudioFile}
       │ Headers: {Authorization: Bearer <token>}
       ▼
┌──────────────────────────────────────────┐
│   audio/views.py: AudioUploadView        │
│   permission_classes = [IsAuthenticated] │
└──────┬───────────────────────────────────┘
       │
       ├─► Validar 'file' en request.FILES
       │
       ├─► AudioUploadSerializer.validate_file()
       │   ├─ content_type in TIPOS_AUDIO_PERMITIDOS
       │   ├─ size <= TAMANO_MAXIMO_AUDIO (50MB)
       │   └─ Renombrar: audio_{uuid}.{ext}
       │
       ├─► Guardar AudioUpload inicial
       │   └─ user=request.user
       │
       ├─► ia_model.verificar_autenticidad(audio_path)
       │   │
       │   └─► rf_model.RFAudioDetector
       │       ├─ Cargar audio: librosa.load(sr=16000)
       │       ├─ Segmentar: ventanas 3s, hop 1.5s
       │       ├─ Para cada segmento:
       │       │   ├─ _extract_features()
       │       │   │   ├─ STFT → spectral features
       │       │   │   ├─ Mel-spec → MFCCs
       │       │   │   ├─ Deltas y delta-deltas
       │       │   │   ├─ ZCR, centroid, flatness
       │       │   │   ├─ RMS, rolloff, flux
       │       │   │   └─ Agregación (mean, std, p10, p90)
       │       │   └─ model.predict_proba(features)
       │       ├─ Calcular métricas agregadas:
       │       │   ├─ avg_ia, avg_real
       │       │   └─ pct_ia (% segmentos ≥ thresh)
       │       └─ Decisión final:
       │           if avg_ia ≥ 0.60 OR pct_ia ≥ 0.20:
       │               resultado = 'IA'
       │           else:
       │               resultado = 'REAL'
       │
       ├─► utils.generar_espectrograma(audio_path)
       │   ├─ librosa.feature.melspectrogram()
       │   ├─ librosa.power_to_db()
       │   ├─ matplotlib backend: Agg
       │   ├─ Guardar PNG en media/plots/user_{id}/
       │   └─ Retornar ruta relativa
       │
       ├─► Actualizar AudioUpload:
       │   ├─ result = 'IA' | 'REAL'
       │   ├─ probability = float
       │   └─ spectrogram = path
       │
       └─► Response JSON:
           {
             status: 'success',
             data: {
               id, file_url, original_filename,
               result, probability, spectrogram,
               created_at
             }
           }
```

---

## 💾 MODELOS DE BASE DE DATOS

### Esquema Relacional

```sql
-- Usuario
CustomUser (usuario_customuser)
  id: INTEGER PRIMARY KEY
  email: VARCHAR(254) UNIQUE
  username: VARCHAR(150) UNIQUE
  first_name: VARCHAR(30)
  last_name: VARCHAR(30)
  is_verified: BOOLEAN DEFAULT FALSE
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
  -- Campos heredados de AbstractUser

UserProfile (usuario_userprofile)
  id: INTEGER PRIMARY KEY
  user_id: INTEGER FOREIGN KEY → CustomUser
  bio: TEXT
  avatar: VARCHAR(100)
  total_analyses: INTEGER DEFAULT 0
  premium_until: TIMESTAMP NULL

-- Texto
AnalisisTexto (texto_analisistexto)
  id: INTEGER PRIMARY KEY
  texto_original: TEXT
  prediccion: VARCHAR(10) CHECK IN ('IA', 'HUMANO')
  probabilidad_ia: FLOAT
  probabilidad_humano: FLOAT
  confianza: VARCHAR(10)
  modelo_utilizado: VARCHAR(50)
  tipo_entrada: VARCHAR(10) CHECK IN ('TEXTO', 'ARCHIVO')
  fecha_analisis: TIMESTAMP
  usuario_id: INTEGER FOREIGN KEY → CustomUser NULL

ArchivoAnalisis (archivo_analisis)
  id: INTEGER PRIMARY KEY
  analisis_id: INTEGER FOREIGN KEY → AnalisisTexto (OneToOne)
  ruta_archivo_original: VARCHAR(500)
  hash_archivo: VARCHAR(64)  -- SHA256
  fecha_subida: TIMESTAMP

-- Audio
AudioUpload (audio_audioupload)
  id: INTEGER PRIMARY KEY
  user_id: INTEGER FOREIGN KEY → CustomUser
  file: VARCHAR(100)  -- FileField path
  original_filename: VARCHAR(255)
  result: VARCHAR(100)
  probability: FLOAT
  spectrogram: VARCHAR(100)  -- ImageField path
  created_at: TIMESTAMP
  
  INDEX idx_user_created (user_id, created_at)
  INDEX idx_result (result)

-- Código (Pendiente)
CodigoUpload (codigo_codigoupload)
  -- Por implementar
```

### Relaciones Clave

```
CustomUser (1) ←→ (1) UserProfile
CustomUser (1) ←→ (N) AnalisisTexto
CustomUser (1) ←→ (N) AudioUpload
AnalisisTexto (1) ←→ (1) ArchivoAnalisis
```

---

## 🌐 APIs Y ENDPOINTS

### Autenticación (`/api/auth/`)

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/register/` | No | Registro de usuario |
| POST | `/login/` | No | Login JWT |
| POST | `/logout/` | No | Logout (blacklist token) |
| GET | `/profile/` | Sí | Perfil del usuario |
| GET | `/users/` | No | Listar usuarios |

**Request/Response Examples:**

```json
// POST /api/auth/register/
Request:
{
  "email": "usuario@example.com",
  "username": "usuario123",
  "password": "SecurePass123!",
  "first_name": "Juan",
  "last_name": "Pérez"
}

Response (201):
{
  "message": "Usuario creado exitosamente",
  "user": {
    "id": 1,
    "email": "usuario@example.com",
    "username": "usuario123",
    "first_name": "Juan",
    "last_name": "Pérez"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1Q...",
    "access": "eyJ0eXAiOiJKV1Q..."
  }
}
```

### Texto (`/api/texto/`)

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/analizar/` | No | Analizar texto directo |
| POST | `/analizar-archivo/` | No | Analizar archivo (TXT/PDF/DOCX) |
| POST | `/comparar/` | No | Comparar modelos N y B |
| POST | `/comparar-archivo/` | No | Comparar modelos con archivo |
| GET | `/estado/` | No | Estado del servicio |
| GET | `/info-modelos/` | No | Información de modelos |
| GET | `/` | No | Root endpoint |

**Request/Response Examples:**

```json
// POST /api/texto/analizar/
Request:
{
  "texto": "Este es un texto de ejemplo para analizar...",
  "modelo": "B"
}

Response (200):
{
  "prediccion": "IA",
  "probabilidad_ia": 87.34,
  "probabilidad_humano": 12.66,
  "confianza": "ALTA",
  "modelo_usado": "B",
  "analisis_id": 42,
  "fecha_analisis": "2025-11-18T10:30:00Z"
}

// POST /api/texto/analizar-archivo/
Request: FormData
  archivo: File
  modelo: 'B'

Response (200):
{
  "resultado": "Humano",
  "probabilidad_ia": 23.5,
  "probabilidad_humano": 76.5,
  "confianza": "ALTA",
  "fragmentos_analizados": 5,
  "fragmentos_ia": 1,
  "fragmentos_humano": 4,
  "archivo_info": {
    "nombre": "documento.pdf",
    "tamano": 245680,
    "tipo": ".pdf",
    "texto_extraido_preview": "Contenido del documento..."
  },
  "analisis_id": 43,
  "modelo_utilizado": "B"
}
```

### Audio (`/api/audio/`)

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/upload/` | Sí | Subir y analizar audio |
| GET | `/` | Sí | Historial del usuario autenticado |
| GET | `/upload/` | Sí | Historial global (admin/depuración) |
| GET | `/certificado/<id>/` | Sí | Descargar certificado PDF |
| POST | `/token/` | No | Obtener JWT (duplicado de `auth`) |
| POST | `/token/refresh/` | No | Refrescar JWT |

**Request/Response Examples:**

```json
// POST /api/audio/upload/
Request: FormData
  file: AudioFile
Headers:
  Authorization: Bearer <access_token>

Response (201):
{
  "status": "success",
  "data": {
    "id": 15,
    "file_url": "http://localhost:8000/media/audios/user_1/audio_abc123.wav",
    "original_filename": "grabacion_voz.wav",
    "result": "REAL",
    "probability": 0.92,
    "spectrogram": "http://localhost:8000/media/plots/user_1/15.png",
    "created_at": "2025-11-18T11:45:00Z"
  }
}

// GET /api/audio/certificado/15/
Response: PDF File (application/pdf)
```

### Código (`/api/codigo/`)

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/` | No | Panel HTML (vista principal) |
| POST | `/subir/` | No | Subir archivo y analizar |
| GET | `/analisis/<id>/` | No | Detalle profesional del análisis |
| GET | `/historial/` | No | Historial con filtros (nombre, lenguaje, IA, fechas) |
| GET | `/historial/comparar/` | No | Comparar 2 análisis (?id1=&id2=) |
| POST | `/historial/comparar/` | No | Comparar lista de IDs (JSON {ids:[]}) |
| GET | `/historial/estadisticas/` | No | KPIs y promedios |
| GET | `/historial/exportar/` | No | Exportación JSON del historial |
| GET | `/reporte/pdf/<id>/` | No | Reporte en PDF |
| GET | `/reporte/json/<id>/` | No | Reporte JSON |

---

## 🤖 INTEGRACIÓN CON ML/IA

### Modelos de Texto (BERT)

**Ubicación:**
- `Backend/texto/modelo_deteccion_ia_B/`
- `Backend/texto/modelo_deteccion_ia_N/`

**Arquitectura:**
```
Input Text → Tokenizer → BERT Encoder → [CLS] token
                                            ↓
                                    Classification Head
                                            ↓
                                    Softmax(logits)
                                            ↓
                                 [P(Humano), P(IA)]
```

**Características:**
- Vocabulario: ~30K tokens
- Max sequence length: 512
- Fine-tuned para clasificación binaria
- Soporte GPU con fallback a CPU

**Gestión de Modelos:**
```python
# Singleton pattern para evitar recargas
predictors = {}

def get_predictor(model_type='B'):
    if model_type not in predictors:
        predictors[model_type] = TextoPredictor(model_type)
    return predictors[model_type]
```

### Modelo de Audio (Random Forest)

**Ubicación:** `Backend/content/rf_v1/`

**Archivos:**
- `model_rf.joblib`: Modelo serializado con joblib
- `manifest.json`: Configuración y metadatos

**Pipeline de Features:**
```
Raw Audio (16kHz)
    ↓
Segmentation (3s windows, 1.5s hop)
    ↓
For each segment:
  ├─ STFT → Magnitude spectrum
  ├─ Mel filterbank → Log-mel spectrogram
  ├─ MFCCs (20 coefficients)
  ├─ Delta MFCCs
  ├─ Delta-delta MFCCs
  ├─ Spectral features:
  │   ├─ Centroid
  │   ├─ Rolloff (85%, 95%)
  │   ├─ Flatness
  │   └─ Flux
  └─ Temporal features:
      ├─ Zero Crossing Rate
      └─ RMS Energy
    ↓
Aggregate statistics per feature:
  [mean, std, p10, p90]
    ↓
Feature vector (144 dimensions)
    ↓
Random Forest (predict_proba)
    ↓
[P(REAL), P(IA)] per segment
    ↓
Aggregate decision:
  avg_ia, pct_ia → Final label
```

**Decisión Multi-Segmento:**
```python
# Estrategia AND para reducir falsos positivos
if avg_ia >= 0.60 OR pct_ia >= 0.20:
    resultado = 'IA'
else:
    resultado = 'REAL'
```

### Modelo de Código (Implementado)

**Ubicación:** `Backend/codigo/code_detection-model-complete/`

**Arquitectura:**
- Detector basado en Transformer (tipo CodeBERT) cargado perezosamente (`CodeDetectorHF`) con fallback seguro si faltan pesos.
- Pipeline complementario: heurísticas por línea/bloque y análisis sintáctico (AST, complejidad ciclomatica, patrones, predictibilidad).

---

## 🔒 SEGURIDAD Y AUTENTICACIÓN

### JWT (JSON Web Tokens)

**Configuración:**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Configuración permisiva
    ],
}
```

**Flujo de Tokens:**
```
1. Login → Generate (refresh_token, access_token)
2. Store tokens en cliente (localStorage/cookies)
3. Requests → Header: Authorization: Bearer <access_token>
4. Refresh → POST con refresh_token → Nuevo access_token
5. Logout → Blacklist refresh_token
```

### CORS (Cross-Origin Resource Sharing)

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
```

### Validación de Archivos

**Audio:**
```python
TIPOS_AUDIO_PERMITIDOS = [
    'audio/wav', 'audio/mpeg', 'audio/mp3', 
    'audio/wave', 'audio/x-wav', 'audio/x-m4a', 
    'audio/aac'
]
TAMANO_MAXIMO_AUDIO = 50 * 1024 * 1024  # 50MB
```

**Documentos:**
```python
ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.docx']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Validación de headers de archivo
if file_extension == '.pdf' and not first_bytes.startswith(b'%PDF'):
    return False, "Archivo no válido"
```

### Protección de Rutas

**Decoradores y Clases:**
```python
# Vista basada en función
@permission_classes([IsAuthenticated])
def mi_vista(request):
    ...

# Vista basada en clase
class MiVista(APIView):
    permission_classes = [IsAuthenticated]
    ...
```

**Acceso Restringido:**
```python
# Solo permitir acceso al propietario
audio_upload = get_object_or_404(
    AudioUpload, 
    id=audio_id, 
    user=request.user  # Filtra por usuario
)
```

### Mitigación de Riesgos

1. **SQL Injection:** Django ORM parametriza queries automáticamente
2. **XSS:** Django escapa HTML por defecto en templates
3. **CSRF:** Protección activa (excepto en API endpoints con @csrf_exempt)
4. **Path Traversal:** Validación de nombres de archivo
5. **DoS:** Límites de tamaño de archivo
6. **Rate Limiting:** Pendiente de implementación

### Hallazgos de Permisos y CORS (código real)

- `REST_FRAMEWORK.DEFAULT_PERMISSION_CLASSES = AllowAny` (global) → todos los endpoints son públicos salvo que la vista declare permisos.
- `audio/` aplica `IsAuthenticated` en `AudioUploadView`, `AudioAnalysisView` y en certificados.
- `texto/` usa funciones con `@csrf_exempt` y sin autenticación → público; operaciones de ML potencialmente costosas.
- `usuario/` marca `AllowAny` incluso en `profile`, `logout` y `users` → exposición indebida de datos/acciones.
- `audio/urls.py` expone `token` y `token/refresh`; duplican endpoints de auth y deberían centralizarse bajo `/api/auth/`.
- `CORS_ALLOW_ALL_ORIGINS=True` además de `CORS_ALLOWED_ORIGINS=[localhost:5173]` → solo aceptable en desarrollo.

Recomendaciones rápidas:
- Definir permisos explícitos por vista y endurecer el default a `IsAuthenticated` o per-app.
- Mover endpoints JWT a `/api/auth/` exclusivamente y eliminar duplicados en `audio`.
- Añadir throttling (anónimo/autenticado) para `/api/texto/*`.
- Desactivar `CORS_ALLOW_ALL_ORIGINS` fuera de desarrollo.

---

## ⚙️ CONFIGURACIÓN Y DEPLOYMENT

### Variables de Entorno (.env)

```bash
# Base de datos
POSTGRES_DB=proyecto_sw1
POSTGRES_USER=sw1_user
POSTGRES_PASSWORD=sw1_password
DB_HOST=localhost
DB_PORT=5435

# Django
SECRET_KEY=django-insecure-^p=%8&dp...
DEBUG=True
ALLOWED_HOSTS=*

# Frontend (para CORS)
VITE_API_URL=http://localhost:8000
```

### Docker Compose

**Servicios:**
```yaml
services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - "5435:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Logging

**Configuración:**
```python
RUTA_LOGS = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(RUTA_LOGS, 'audio_analysis.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'audio': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    },
}
```

### Estructura de Archivos Media

```
media/
├── audios/
│   ├── user_1/
│   │   ├── audio_abc123.wav
│   │   └── audio_def456.wav
│   └── user_2/
│       └── audio_xyz789.wav
├── plots/
│   ├── user_1/
│   │   ├── 1.png
│   │   └── 2.png
│   └── user_2/
│       └── 3.png
└── avatars/
    └── user_1_avatar.jpg
```

### Dependencias (requirements.txt)

**Core:**
- Django==5.2.8
- djangorestframework
- djangorestframework-simplejwt
- django-cors-headers
- psycopg2-binary

**ML/IA:**
- torch
- transformers
- scikit-learn
- joblib
- librosa
- numpy

**Procesamiento:**
- PyPDF2
- python-docx
- python-magic (validación de tipos MIME)
- Pillow (imágenes)

**Generación de PDFs:**
- reportlab

**Utilidades:**
- python-dotenv

---

## 📊 PATRONES Y BUENAS PRÁCTICAS

### Patrones Identificados

#### 1. Lazy Loading de Modelos ML
```python
# Cargar modelos una sola vez y cachearlos
predictors = {}

def get_predictor(model_type='B'):
    if model_type not in predictors:
        predictors[model_type] = TextoPredictor(model_type)
    return predictors[model_type]
```

**Beneficio:** Evita recargar modelos pesados (100MB+) en cada request.

#### 2. Try-Except con Fallbacks
```python
try:
    self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
except Exception:
    try:
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    except Exception:
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
```

**Beneficio:** Sistema robusto que no falla si archivos locales están corruptos.

#### 3. Serializers para Validación
```python
class AudioUploadSerializer(serializers.ModelSerializer):
    def validate_file(self, archivo):
        if archivo.content_type not in settings.TIPOS_AUDIO_PERMITIDOS:
            raise ValidationError({...})
        if archivo.size > settings.TAMANO_MAXIMO_AUDIO:
            raise ValidationError({...})
        return archivo
```

**Beneficio:** Validación centralizada, reutilizable y consistente.

#### 4. Context Managers para Modelos
```python
with torch.no_grad():
    outputs = self.model(**inputs)
```

**Beneficio:** Desactiva cálculo de gradientes → Ahorra memoria y acelera inferencia.

#### 5. Agregación de Métricas
```python
def _aggregate_stats(self, x: np.ndarray) -> List[float]:
    return [np.mean(x), np.std(x), 
            np.percentile(x, 10), np.percentile(x, 90)]
```

**Beneficio:** Reduce dimensionalidad de features temporales a estadísticas representativas.

### Buenas Prácticas Django

1. **Uso de `get_object_or_404`:**
   ```python
   audio = get_object_or_404(AudioUpload, id=audio_id, user=request.user)
   ```

2. **Modelos con Meta Options:**
   ```python
   class Meta:
       ordering = ['-created_at']
       indexes = [models.Index(fields=['user', 'created_at'])]
   ```

3. **Related Names:**
   ```python
   user = models.ForeignKey(CustomUser, related_name='audio_uploads')
   # Acceso: user.audio_uploads.all()
   ```

4. **Upload To Functions:**
   ```python
   def ruta_archivo_audio(instance, filename):
       user_folder = f"user_{instance.user.id}"
       return os.path.join(settings.RUTA_SUBIDA_AUDIOS, user_folder, filename)
   ```

5. **Signals para Actualización Automática:**
   ```python
   def save(self, *args, **kwargs):
       if self.user and hasattr(self.user, 'userprofile'):
           self.user.userprofile.total_analyses = self.user.audio_uploads.count()
           self.user.userprofile.save()
       super().save(*args, **kwargs)
   ```

---

## 🚀 ÁREAS DE MEJORA

### Críticas

1. **Falta de Rate Limiting**
  - Endpoints públicos sin límite de requests
  - Riesgo de abuso/DoS

2. **Permisos por Defecto Permisivos**
  - `DEFAULT_PERMISSION_CLASSES = AllowAny` globalmente
  - `usuario/` expone `profile`, `logout`, `users` con `AllowAny`
  - `texto/` es público y costoso (ML) → susceptible a abuso

3. **JWT Duplicado en `audio/`**
  - `token/` y `token/refresh/` también existen en `audio/urls.py`
  - Deben centralizarse bajo `/api/auth/` para coherencia

4. **Falta de Tests Unitarios**
   - Archivos `tests.py` vacíos
   - Solo tests básicos en `tests/`

5. **Logging Incompleto**
   - Solo configurado para `audio`
   - `texto/` y `codigo/` sin logging

### Medias

6. **Fragmentación de Código Duplicado**
   - Cálculo de confianza repetido
   - Validación de archivos duplicada

7. **Manejo de Errores Genérico**
   - Muchos `except Exception` sin especificar
   - Mensajes de error poco descriptivos

8. **Falta de Paginación**
  - Listas sin paginar (p.ej. `GET /api/audio/upload/` global y `codigo/historial/`)
  - Problema de performance con muchos registros

9. **Sin Compresión de Media**
   - Espectrogramas PNG sin optimizar
   - Audios sin compresión

10. **Configuración Hardcodeada**
    - `SECRET_KEY` visible en settings.py
    - `DEBUG=True` en producción

### Bajas (Mejoras)

11. **Versionado de API**
    - `/api/v1/texto/` para futuras versiones
    - Facilita breaking changes

12. **Caché de Resultados**
    - Cache de predicciones por hash de archivo
    - Redis para resultados recientes

13. **Async/Background Tasks**
    - Celery para análisis largos
    - Evitar timeouts en requests HTTP

14. **Métricas y Monitoreo**
    - Prometheus/Grafana para observabilidad
    - Track de accuracy, latencia, uso de modelos

15. **Documentación Automática**
    - Swagger/OpenAPI con drf-yasg
    - Docs interactivas de API

---

## 📈 MÉTRICAS DEL SISTEMA

### Líneas de Código (Estimado)
```
audio/: ~800 líneas
texto/: ~1200 líneas
usuario/: ~300 líneas
Backend/: ~400 líneas
Total: ~2700 líneas (sin contar modelos ML)
```

### Modelos ML
```
Texto:
  - Modelo B: ~440MB (model.safetensors)
  - Modelo N: ~440MB
  
Audio:
  - RF Model: ~50MB (model_rf.joblib)
  
Código:
  - CodeBERT: ~500MB (integrado vía carga perezosa)
```

### Endpoints Totales (aprox.)
```
Autenticación: 5
Texto: 7
Audio: 6
Código: 10
Total: 28 endpoints
```

---

## 🔗 INTERACCIÓN CON FRONTEND

### API Contract

**Base URL:** `http://localhost:8000/api/`

**Headers Comunes:**
```javascript
{
  'Content-Type': 'application/json',
  'Authorization': 'Bearer <access_token>'  // Para endpoints protegidos
}
```

**Error Responses:**
```json
{
  "error": "Mensaje descriptivo",
  "codigo": "ERROR_CODE",  // Opcional
  "detalles": {...}        // Opcional
}
```

### Flujos Frontend-Backend

**1. Registro y Login:**
```javascript
// Registro
POST /api/auth/register/
  → Guardar tokens en localStorage
  → Redirect a dashboard

// Login
POST /api/auth/login/
  → Guardar tokens
  → Actualizar contexto de usuario
```

**2. Análisis de Texto:**
```javascript
// Texto directo
POST /api/texto/analizar/
  → Mostrar resultado en UI
  → Guardar en historial local

// Archivo
POST /api/texto/analizar-archivo/
  → FormData con archivo
  → Progress bar durante subida
  → Mostrar resultado + preview del texto
```

**3. Análisis de Audio:**
```javascript
// Subir audio
POST /api/audio/upload/
  → Headers: Authorization
  → FormData con archivo
  → Mostrar espectrograma
  → Botón para descargar certificado

// Certificado
GET /api/audio/certificado/{id}/
  → Headers: Authorization
  → Download PDF
```

### CORS y Cookies

```javascript
// Configuración de fetch
fetch(url, {
  method: 'POST',
  credentials: 'include',  // Para cookies
  headers: {
    'Authorization': `Bearer ${accessToken}`
  },
  body: formData
})
```

---

## 📝 CONCLUSIÓN

### Fortalezas del Sistema

1. **Arquitectura Modular:** Separación clara de responsabilidades
2. **Múltiples Modalidades:** Texto, audio, código (implementado)
3. **ML Robusto:** Modelos preentrenados con fallbacks
4. **Autenticación Moderna:** JWT con refresh tokens
5. **Validación Exhaustiva:** Serializers y validators en múltiples capas
6. **Logging Estructurado:** RotatingFileHandler para auditoría

### Oportunidades de Mejora

1. Implementar rate limiting y throttling
2. Endurecer permisos (`usuario/`, `texto/`) y centralizar JWT
3. Añadir tests unitarios comprehensivos
4. Optimizar performance con caché
5. Migrar a tareas asíncronas (Celery)
6. Mejorar seguridad (SECRET_KEY, DEBUG)
7. Documentación automática de API

### Próximos Pasos Recomendados

1. **Corto Plazo (1-2 semanas):**
  - Añadir rate limiting básico (throttling DRF)
  - Endurecer permisos y mover JWT sólo a `/api/auth/`
  - Completar tests críticos (texto/audio/código)
  - Documentar API con Swagger

2. **Mediano Plazo (1 mes):**
   - Implementar Celery para tasks pesadas
   - Cache con Redis
   - Optimización de media (compresión)
   - Paginación en listados

3. **Largo Plazo (3 meses):**
   - Versionado de API (v1, v2)
   - Métricas y monitoreo avanzado
   - CI/CD pipeline
   - Deployment production-ready

---

**Documento generado:** 18/11/2025  
**Última actualización:** 19/11/2025  
**Autor:** Análisis automatizado del backend  
**Versión:** 1.0.0
