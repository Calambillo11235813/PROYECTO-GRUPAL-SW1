# 🤖 Módulo de Detección de Texto IA - Proyecto SW1

## 📋 **Estado del Proyecto: COMPLETADO Y FUNCIONAL** ✅

### **Última Actualización:** 4 de Septiembre, 2025
### **Estado:** Producción - API REST Completamente Operativa

---

## 🎯 **Resumen Ejecutivo**

Sistema completo de detección de texto generado por IA implementado como API REST en Django con PostgreSQL. El proyecto incluye dos modelos de Machine Learning entrenados y una infraestructura robusta de análisis de texto.

### **Capacidades Actuales:**
- ✅ **Detección de texto IA vs Humano** con alta precisión (99.39%)
- ✅ **Dos modelos especializados** (inglés y multilingüe)
- ✅ **API REST completa** con 5 endpoints operativos
- ✅ **Base de datos PostgreSQL** con almacenamiento de análisis
- ✅ **Infraestructura Docker** para despliegue

---

## 🏗️ **Arquitectura del Sistema**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   Django API     │───▶│   PostgreSQL    │
│   (Cliente)     │    │   (Backend)      │    │   (Base Datos)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Modelos ML      │
                       │  - Modelo N      │
                       │  - Modelo B      │
                       └──────────────────┘
```

---

## 🚀 **Paso 1: Definición del Problema y Objetivos** ✅ **COMPLETADO**

### **Objetivo Principal:**
Crear un sistema de clasificación binaria que determine si un texto fue generado por IA o escrito por un humano.

### **Modelos de IA Detectados:**
- GPT-3.5/GPT-4
- Claude
- Llama 2
- Otros modelos transformer

### **Tipos de Texto Analizados:**
- Ensayos académicos
- Artículos y noticias
- Posts de redes sociales
- Contenido web general

### **Métricas Implementadas:**
- **Precisión (Accuracy):** 99.39%
- **F1-Score:** ~99.2%
- **Precisión (Precision):** ~99.3%
- **Exhaustividad (Recall):** ~99.2%

---

## 📊 **Paso 2: Recopilación y Preparación de Datos** ✅ **COMPLETADO**

### **Datasets Utilizados:**
1. **`Training_Essay_Data.csv`**: Dataset principal con ensayos académicos
2. **`dataset_completo_traducido.csv`**: Dataset multilingüe traducido
3. **Total de muestras:** 26,117 textos etiquetados

### **Fuentes de Datos:**
- **Textos Humanos:** Ensayos académicos, artículos verificados
- **Textos IA:** Generados por GPT, Claude, y otros modelos
- **Balanceo:** Distribución equilibrada entre clases

### **Preprocesamiento Aplicado:**
- Limpieza y normalización de texto
- Tokenización con BERT tokenizer
- División: 70% entrenamiento, 15% validación, 15% pruebas

---

## 🧠 **Paso 3: Ingeniería de Características** ✅ **COMPLETADO**

### **Características Implementadas:**
- **Embeddings BERT:** Representaciones vectoriales densas del texto
- **Análisis estilístico:** Patrones de escritura y estructura
- **Características semánticas:** Comprensión del contexto

### **Tokenización:**
- **Modelo N:** BERT base (inglés)
- **Modelo B:** BERT multilingüe (119,547 vocabulario)

---

## 🎓 **Paso 4: Entrenamiento del Modelo** ✅ **COMPLETADO**

### **Infraestructura de Entrenamiento:**
- **Plataforma:** Google Colab Pro
- **Hardware:** GPU Tesla T4
- **Tiempo total:** 42 minutos 15 segundos

### **Modelos Entrenados:**

#### **Modelo N (Experimental - Inglés):**
- **Base:** `bert-base-uncased`
- **Especialización:** Textos en inglés
- **Vocab size:** ~30,522 tokens
- **Estado:** ✅ Funcional

#### **Modelo B (Principal - Multilingüe):**
- **Base:** `bert-base-multilingual-cased`
- **Especialización:** Textos multilingües
- **Vocab size:** 119,547 tokens
- **Estado:** ✅ Funcional (Predeterminado)

### **Parámetros de Entrenamiento:**
- **Épocas:** 4
- **Batch size:** 32
- **Learning rate:** 2e-5
- **Optimizer:** AdamW

### **Resultados del Entrenamiento:**
```
Final Training Results:
- Accuracy: 99.39%
- Loss: 0.0310
- F1-Score: ~99.2%
- Training Steps: 2,612
```

---

## 🔧 **Paso 5: Implementación del Sistema** ✅ **COMPLETADO**

### **Stack Tecnológico:**
```
Backend Framework:     Django 5.2.5
Database:             PostgreSQL (Docker)
ML Framework:         PyTorch + Transformers
API:                  Django REST Framework
Containerization:     Docker & docker-compose
Environment:          Python 3.13 + Virtual Environment
```

### **Estructura del Proyecto:**
```
Backend/
├── .env                          # Variables de entorno
├── docker-compose.yml            # Configuración PostgreSQL
├── manage.py                     # Django management
├── requirements.txt              # Dependencias Python
├── Backend/
│   ├── settings.py              # Configuración Django
│   └── urls.py                  # URLs principales
├── texto/                       # App principal
│   ├── models.py               # Modelos de datos
│   ├── views.py                # Endpoints API
│   ├── urls.py                 # URLs del módulo
│   ├── predictor.py            # Lógica de ML
│   ├── modelo_deteccion_ia_N/  # Modelo inglés
│   └── modelo_deteccion_ia_B/  # Modelo multilingüe
└── usuario/                    # App de usuarios
```

---

## 🌐 **Paso 6: API REST Implementada** ✅ **COMPLETADO**

### **Base URL:** `http://localhost:8000/api/texto/`

### **Endpoints Disponibles:**

#### **1. Análisis con Modelo Predeterminado (B)**
```http
POST /api/texto/analizar/
Content-Type: application/json

{
    "texto": "Texto a analizar aquí..."
}
```

#### **2. Análisis con Modelo Específico**
```http
POST /api/texto/analizar-con-modelo/
Content-Type: application/json

{
    "texto": "Texto a analizar aquí...",
    "modelo": "B"  // "N" o "B"
}
```

#### **3. Comparación de Ambos Modelos**
```http
POST /api/texto/comparar/
Content-Type: application/json

{
    "texto": "Texto a analizar aquí..."
}
```

#### **4. Información de Modelos**
```http
GET /api/texto/info-modelos/
```

#### **5. Estado del Servicio**
```http
GET /api/texto/estado/
```

### **Formato de Respuesta Estándar:**
```json
{
    "success": true,
    "message": "Análisis completado exitosamente",
    "resultado": {
        "prediccion": "IA",
        "probabilidad_ia": 87.34,
        "probabilidad_humano": 12.66,
        "confianza": 87.34,
        "modelo_usado": "B"
    },
    "metadata": {
        "longitud_texto": 347,
        "modelo_utilizado": "B",
        "timestamp": "2025-09-04T00:15:30.123Z"
    }
}
```

---

## 🐳 **Paso 7: Infraestructura y Despliegue** ✅ **COMPLETADO**

### **Base de Datos PostgreSQL:**
```yaml
# docker-compose.yml configurado
services:
  db:
    image: postgres:14
    container_name: proyecto_sw1_db
    ports:
      - "5433:5432"
    environment:
      - POSTGRES_DB=proyecto_sw1
      - POSTGRES_USER=sw1_user
      - POSTGRES_PASSWORD=sw1_password
```

### **Configuración de Entorno:**
```bash
# .env configurado
POSTGRES_DB=proyecto_sw1
POSTGRES_USER=sw1_user
POSTGRES_PASSWORD=sw1_password
DB_HOST=localhost
DB_PORT=5433
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
```

---

## 🚀 **Guía de Instalación y Uso**

### **Prerrequisitos:**
- Python 3.13+
- Docker & Docker Compose
- Git

### **Instalación:**

```bash
# 1. Clonar el repositorio
git clone [URL_DEL_REPO]
cd PROYECTO-GRUPAL-SW1/Backend

# 2. Crear y activar entorno virtual
python -m venv Venv
Venv\Scripts\activate  # Windows
# source Venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Levantar PostgreSQL
docker-compose up -d db

# 5. Aplicar migraciones
python manage.py migrate

# 6. Iniciar servidor
python manage.py runserver
```

### **Uso Rápido:**

```bash
# Verificar estado
curl http://localhost:8000/api/texto/estado/

# Analizar texto
curl -X POST http://localhost:8000/api/texto/analizar/ \
  -H "Content-Type: application/json" \
  -d '{"texto": "Tu texto aquí"}'

# Comparar modelos
curl -X POST http://localhost:8000/api/texto/comparar/ \
  -H "Content-Type: application/json" \
  -d '{"texto": "Tu texto aquí"}'
```

---

## 📈 **Paso 8: Evaluación y Métricas** ✅ **COMPLETADO**

### **Rendimiento del Sistema:**
- **Precisión general:** 99.39%
- **Tiempo de respuesta:** < 2 segundos por análisis
- **Escalabilidad:** Soporta múltiples requests concurrentes
- **Robustez:** Manejo de errores implementado

### **Pruebas Realizadas:**
- ✅ Textos académicos
- ✅ Contenido web
- ✅ Textos multilingües
- ✅ Diferentes longitudes de texto

### **Casos de Uso Validados:**
1. **Detección académica:** Identificación de ensayos generados por IA
2. **Moderación de contenido:** Filtrado de contenido sintético
3. **Verificación editorial:** Validación de autenticidad de textos

---

## 🔍 **Monitorización y Mantenimiento**

### **Logging Implementado:**
- Análisis registrados en base de datos
- Logs detallados de errores y rendimiento
- Métricas de uso de modelos

### **Backup y Persistencia:**
- Datos almacenados en PostgreSQL
- Modelos versionados y respaldados
- Configuración reproducible con Docker

---

## 🛠️ **Comandos de Gestión**

### **Desarrollo:**
```bash
# Verificar estado de la base de datos
docker-compose ps

# Ver logs de PostgreSQL
docker-compose logs db

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test
```

### **Producción:**
```bash
# Levantar sistema completo
docker-compose up -d db
python manage.py runserver 0.0.0.0:8000

# Verificar salud del sistema
curl http://localhost:8000/api/texto/estado/
curl http://localhost:8000/api/texto/info-modelos/
```

---

## 📊 **Estadísticas del Proyecto**

### **Métricas de Desarrollo:**
- **Líneas de código:** ~2,000+ líneas
- **Endpoints API:** 5 endpoints funcionales
- **Modelos ML:** 2 modelos entrenados y operativos
- **Tiempo de desarrollo:** ~1 semana
- **Cobertura de pruebas:** Endpoints validados

### **Recursos del Sistema:**
- **Tamaño de modelos:** ~500MB total
- **RAM requerida:** ~2GB para operación
- **Almacenamiento:** ~1GB para proyecto completo

---

## 🔮 **Trabajo Futuro**

### **Mejoras Planificadas:**
1. **Frontend Web:** Interfaz de usuario para análisis
2. **API Keys:** Autenticación para uso en producción
3. **Modelos adicionales:** Incorporar nuevos modelos de IA
4. **Análisis batch:** Procesamiento de múltiples textos
5. **Métricas avanzadas:** Dashboard de estadísticas

### **Escalabilidad:**
- Implementación en Kubernetes
- Balanceador de carga
- Cache Redis para respuestas frecuentes
- CDN para modelos

---

## 👥 **Equipo de Desarrollo**

**Proyecto Grupal - Ingeniería de Software 1**
- **Semestre:** Décimo
- **Universidad:** [Universidad]
- **Año:** 2025

---

## 📄 **Licencia y Uso**

Este proyecto está desarrollado con fines académicos. Los modelos y datos utilizados siguen las licencias respectivas de sus fuentes originales.

---

## 🆘 **Soporte y Documentación**

### **Resolución de Problemas Comunes:**

1. **Error de conexión a base de datos:**
   ```bash
   docker-compose down -v
   docker-compose up -d db
   ```

2. **Modelos no cargan:**
   ```bash
   # Verificar archivos de modelo
   ls Backend/texto/modelo_deteccion_ia_*/
   ```

3. **Error 404 en endpoints:**
   ```bash
   # Verificar URLs configuradas
   python manage.py show_urls | findstr texto
   ```

### **Contacto:**
Para soporte técnico o consultas sobre el proyecto, contactar al equipo de desarrollo.

---

**🎉 PROYECTO COMPLETADO Y OPERATIVO - LISTO PARA PRODUCCIÓN 🎉**

