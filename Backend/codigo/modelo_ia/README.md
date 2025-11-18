# Sistema de Detección de Código Generado por IA

## Descripción General
Sistema híbrido inteligente que combina modelos de machine learning (CodeBERT) con reglas heurísticas para detectar código generado por inteligencia artificial con **92% de precisión**.

## Estructura de Archivos

### Archivos Principales del Modelo

| Archivo | Tamaño | Propósito |
|---------|--------|-----------|
| `production_detector.pkl` | 477 MB | **DETECTOR PRINCIPAL** - Clase serializada lista para usar |
| `model.safetensors` | 475 MB | Pesos del modelo CodeBERT fine-tuned |
| `tokenizer.json` | 3.4 MB | Configuración del tokenizador |
| `vocab.json` | 0.76 MB | Vocabulario del tokenizador |
| `merges.txt` | 0.44 MB | Reglas de merge para tokenización BPE |

### Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `config.json` | Configuración de la arquitectura del modelo |
| `tokenizer_config.json` | Configuración específica del tokenizador |
| `special_tokens_map.json` | Mapeo de tokens especiales |
| `system_metadata.json` | Metadatos del sistema y métricas de rendimiento |

### Archivos de Entrenamiento (Backup)

| Archivo | Propósito |
|---------|-----------|
| `training_args.bin` | Argumentos de entrenamiento guardados |
| `checkpoint-518/` | Checkpoint de época intermedia |
| `checkpoint-777/` | Checkpoint final del entrenamiento |

## Uso Rápido

```python
import joblib

# Cargar el detector
detector = joblib.load('./code-detection-model/production_detector.pkl')

# Analizar código
resultado = detector.detect('''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
''')

print(f"¿Es IA?: {resultado['is_ai_generated']}")
print(f"Confianza: {resultado['confidence']:.1%}")
print(f"Método usado: {resultado['method_used']}")
```

## Métricas del Modelo

- **Precisión General**: 91.92%
- **F1-Score**: 90.94%
- **Precisión (IA)**: 98.49%
- **Recall (IA)**: 84.47%
- **Falsos Negativos**: 0.62%
- **Tiempo Entrenamiento**: 13 minutos 29 segundos

## Arquitectura del Sistema

### Componentes Híbridos

1. **Análisis Heurístico**
   - Longitud del código
   - Densidad de comentarios
   - Complejidad estructural
   - Patrones de desarrollo humano

2. **Modelo CodeBERT Fine-Tuned**
   - Base: microsoft/codebert-base
   - Entrenado en: 11,798 muestras balanceadas
   - Clasificación binaria: IA vs Humano

3. **Compensación de Sesgos**
   - Corrección automática de falsos positivos
   - Ajuste de confianzas basado en análisis
   - Reglas para código simple

## Casos de Uso

### Detecta Correctamente

- **Código simple humano** → Reglas heurísticas
- **Código con patrones debug** → Detección de estilos humanos
- **Código IA bien documentado** → Modelo ML + análisis comentarios
- **Código de competencias** → Modelo ML ajustado

### Limitaciones

- **Longitud máxima**: 512 tokens
- **Lenguajes**: Múltiples (Python, JavaScript, Java, etc.)
- **Contexto**: No analiza el propósito del código, solo patrones estilísticos

## Requisitos Técnicos

```bash
# Dependencias principales
transformers >= 4.30.0
torch >= 2.0.0
scikit-learn >= 1.2.0
numpy >= 1.21.0
joblib >= 1.2.0
```

## Rendimiento

- **Inferencia**: ~100ms por análisis (GPU Tesla T4)
- **Memoria**: ~1.5GB GPU + 500MB RAM
- **Batch Processing**: Soporte para múltiples códigos simultáneos

## Desarrollo

### Entrenamiento
- **Dataset**: 11,798 muestras (52% IA, 48% Humano)
- **Épocas**: 3
- **Batch Size**: 32
- **Learning Rate**: 2e-5
- **GPU**: Tesla T4 (16GB)

### Validación
- **Conjunto prueba**: 1,770 muestras
- **Métricas**: Accuracy, F1, Precision, Recall
- **Generalización**: Diferencia validación/prueba < 1.1%

## Soporte

**Proyecto**: Sistema multimodal para análisis de intervención de IA
**Materia**: INF422-SC
**Fecha**: 2024

---

*¡Sistema listo para producción!*