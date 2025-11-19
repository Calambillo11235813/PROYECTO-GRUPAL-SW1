 Flujo completo del análisis (explicación simple)

1.Usuario sube archivo → /api/codigo/subir/
2.Se guarda en el modelo AnalisisCodigo
3.Se lee el código
4.Se detecta lenguaje (detectar_lenguaje.py)
5.Se ejecuta IA CodeBERT (modelos/detector_hf.py)
6.Se obtienen:
 Probabilidad IA / humano
 Confianza
 Método usado
7.Se analizan aspectos del código:
 Complejidad ciclomatica
 Variabilidad de funciones
 Patrones de control
 Idiosincrasias de estilo
 Índice de predictibilidad
8.Se marcan líneas sospechosas IA (marcador_ia.py)
9.Se guardan en BD:
 líneas sospechosas
 bloques sospechosos
 ast_json
 métricas sintácticas
10.El usuario puede obtener:
 PDF detallado
 JSON completo
 Historial
 Comparación de 2 análisis
 Estadísticas globales








 # 📌 SECCIÓN: FUNCIONALIDADES IMPLEMENTADAS

========================================================
🔹 1. HISTORIAS DE USUARIO (HU) COMPLETADAS
========================================================

--------------------------------------------------------
✔ HU-013 — SUBIDA DE ARCHIVOS
--------------------------------------------------------
Permite subir un archivo y generar un análisis completo.

ENDPOINT:
    POST /api/codigo/subir/

--------------------------------------------------------
✔ HU-014 — ANÁLISIS DE PATRONES SINTÁCTICOS
--------------------------------------------------------
INCLUYE:
    ▪ Variabilidad de funciones
    ▪ Complejidad ciclomatica
    ▪ Patrones de control (ifs, loops, trys)
    ▪ Patrones comunes
    ▪ Idiosincrasias (camelCase / snake_case)
    ▪ Índice de predictibilidad

ARCHIVO RESPONSABLE:
    utils/analizador_codigo.py

--------------------------------------------------------
✔ HU-015 — MARCAR LÍNEAS GENERADAS POR IA
--------------------------------------------------------
NIVELES DE DETECCIÓN:
    ▪ lineas_sospechosas  → línea por línea
    ▪ bloques_sospechosos → fragmentos agrupados con score

ARCHIVO RESPONSABLE:
    utils/marcador_ia.py

EL PANEL HTML MUESTRA:
    <<< IA     (en cada línea sospechosa)

--------------------------------------------------------
✔ HU-018 — REPORTE DETALLADO (PDF / JSON)
--------------------------------------------------------
ENDPOINTS:
    GET /api/codigo/reporte/pdf/<id>/
    GET /api/codigo/reporte/json/<id>/

CONTENIDO DEL REPORTE:
    ▪ Probabilidades IA/Humano
    ▪ Métricas técnicas
    ▪ Patrones sintácticos
    ▪ Idiosincrasias
    ▪ Fragmentos sospechosos
    ▪ Timestamp del modelo
    ▪ Versión del modelo
    ▪ (Opcional) Código coloreado tipo VSCode

--------------------------------------------------------
✔ HU-019 — HISTORIAL DE ANÁLISIS
--------------------------------------------------------
FUNCIONES DISPONIBLES:
    ✔ Filtros (nombre, lenguaje, IA/Humano, fechas)
    ✔ Comparación de 2 análisis side-by-side
    ✔ Estadísticas globales
    ✔ Exportación de historial completo en JSON

ENDPOINTS:
    GET /api/codigo/historial/
    GET /api/codigo/historial/comparar/?id1=XX&id2=YY
    GET /api/codigo/historial/estadisticas/
    GET /api/codigo/historial/exportar/

========================================================
🔹 2. PANEL HTML (PARA PRUEBAS DEL EQUIPO)
========================================================

ARCHIVO:
    templates/panel.html

FUNCIONALIDADES:
    ▪ Subir archivo
    ▪ Ver historial completo
    ▪ Filtrar historial
    ▪ Ver código con líneas IA resaltadas
    ▪ Exportar PDF
    ▪ Exportar JSON
    ▪ Comparador de análisis
    ▪ Gráfico IA vs Humano (Chart.js)
    ▪ Modo oscuro

URL DEL PANEL:
    /api/codigo/panel/

========================================================
🔹 3. IA UTILIZADA — MODELO LOCAL CODEBERT
========================================================

UBICACIÓN DEL MODELO:
    codigo/modelo_ia/

CARGADOR DEL MODELO:
    modelos/detector_hf.py

NOTA:
    • No usa internet.
    • Todo se ejecuta localmente.

ALTERNATIVA: DETECTOR PKL (joblib)
--------------------------------------------------------
Desde ahora el backend también soporta un detector `.pkl` (por ejemplo `production_detector.pkl`).

Selección del detector (por env):
- `CODE_DETECTOR_IMPL=pkl` → usa PKL
- `CODE_DETECTOR_IMPL=hf` → usa HuggingFace
- `CODE_DETECTOR_IMPL=auto` (default) → intenta PKL y si no, HF, si no, fallback

Rutas por defecto:
- PKL: `codigo/code_detection-model-complete/production_detector.pkl` (o `codigo/modelo_ia/production_detector.pkl`)
- HF:  `codigo/modelo_ia/`

Variables útiles:
- `CODE_PKL_PATH` → ruta absoluta/relativa al `.pkl`
- `CODE_HF_PATH` → (opcional) ruta al checkpoint HF
- `CODE_DETECTOR_FORCE_FALLBACK=1` → fuerza dummy detector (dev)

--------------------------------------------------------
📦 Cómo instalar/colocar el modelo (HuggingFace)
--------------------------------------------------------

El detector espera un checkpoint de Transformers en `Backend/codigo/modelo_ia/` con:
- Pesos: `pytorch_model.bin` o `model.safetensors`
- Configuración: `config.json`
- Tokenizador: `tokenizer.json` (o archivos `vocab.json` + `merges.txt`, según el modelo)

Ejemplo (placeholder) para descargar y guardar un modelo en local:

PowerShell (desde `Backend/`):

```
./venv/Scripts/python.exe -c "from transformers import AutoModelForSequenceClassification, AutoTokenizer; import os; m='bert-base-uncased'; d=os.path.join(os.getcwd(),'codigo','modelo_ia'); os.makedirs(d, exist_ok=True); AutoTokenizer.from_pretrained(m).save_pretrained(d); AutoModelForSequenceClassification.from_pretrained(m, num_labels=2).save_pretrained(d)"
```

Importante: el modelo anterior es solo para satisfacer la estructura de archivos. Para detección IA real de código, usa un modelo entrenado para esa tarea y guarda su checkpoint en `codigo/modelo_ia/`.

--------------------------------------------------------
🛟 Fallback seguro (sin pesos locales)
--------------------------------------------------------

Si no existen pesos HF, el sistema usa un detector "dummy" que:
- Nunca lanza excepción
- Responde `ia_metodo: "fallback"` y `ia_confianza: 0.0`

Puedes forzar este modo en desarrollo sin intentar cargar HF usando la variable de entorno:

```
CODE_DETECTOR_FORCE_FALLBACK=1
```

Sugerido: copia `Backend/.env.example` a `Backend/.env` y deja `CODE_DETECTOR_FORCE_FALLBACK=1` en dev.

========================================================
🔹 4. MODELO AnalisisCodigo — CAMPOS EXPLICADOS
========================================================

PRINCIPALES CAMPOS DEL MODELO:

    ▪ archivo
    ▪ nombre_archivo
    ▪ lenguaje
    ▪ ia_es_generado
    ▪ ia_confianza
    ▪ ia_detalles
    ▪ lineas_sospechosas
    ▪ bloques_sospechosos
    ▪ complejidad_ciclomatica
    ▪ variabilidad_funciones
    ▪ patrones_comunes
    ▪ patrones_control
    ▪ idiosincrasias
    ▪ ast_json
    ▪ indice_predictibilidad
    ▪ version_modelo
    ▪ timestamp_modelo

========================================================
🔹 5. CÓMO PROBAR EL SISTEMA DESDE EL PANEL
========================================================

PASOS:

    1. Abrir navegador.
    2. Entrar a:
           http://127.0.0.1:8000/api/codigo/panel/
    3. Subir un archivo.
    4. Revisar historial.
    5. Exportar PDF o JSON.
    6. Ver código marcado con IA.
    7. Comparar dos análisis.
    8. Usar filtros.
    9. Ver gráfica estadística.

========================================================
🔹 6. Pruebas rápidas (API / consola)
========================================================

1) Subir archivo por API (Django test client desde consola):

PowerShell (desde `Backend/`):

```
./venv/Scripts/python.exe -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE','Backend.settings'); django.setup(); from django.test import Client; from django.core.files.uploadedfile import SimpleUploadedFile as SUF; c=Client(); r=c.post('/api/codigo/subir/', {'archivo': SUF('foo.py', b'print(123)')}); print(r.status_code); print(r.json())"
```

2) Ver detalle de un análisis creado (reemplaza <ID>):

```
curl -X GET http://127.0.0.1:8000/api/codigo/analisis/<ID>/
```

3) Exportar PDF/JSON (reemplaza <ID>):

```
curl -X GET -o reporte.pdf http://127.0.0.1:8000/api/codigo/reporte/pdf/<ID>/
curl -X GET -o reporte.json http://127.0.0.1:8000/api/codigo/reporte/json/<ID>/
```

4) Forzar fallback solo para esta sesión PowerShell:

```
$env:CODE_DETECTOR_FORCE_FALLBACK="1"
```

5) Recomendado en desarrollo: usar `.env` con `CODE_DETECTOR_FORCE_FALLBACK=1` y añadir modelo real más adelante en `codigo/modelo_ia/`.

6) Probar modo PKL (si tienes `production_detector.pkl`):

PowerShell (desde `Backend/`):

```
$env:CODE_DETECTOR_IMPL="pkl"
$env:CODE_PKL_PATH="C:\Users\DELL\Desktop\PROYECTO-GRUPAL-SW1\Backend\codigo\code_detection-model-complete\production_detector.pkl"
.\n+venv\Scripts\python.exe -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE','Backend.settings'); django.setup(); from django.test import Client; from django.core.files.uploadedfile import SimpleUploadedFile as SUF; c=Client(); r=c.post('/api/codigo/subir/', {'archivo': SUF('foo.py', b'print(123)')}); print(r.status_code); print(r.json())"
```


