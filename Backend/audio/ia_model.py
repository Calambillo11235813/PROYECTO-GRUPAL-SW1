import logging
import mimetypes
import os
import time
from typing import Tuple

from .rf_model import load_rf_detector
from .services.truthscan_client import (
    TruthScanError,
    TruthScanResult,
    get_truthscan_client,
)

logger = logging.getLogger(__name__)

# Cargar el modelo personalizado de Random Forest (fallback)
# Cargar el modelo personalizado de Random Forest
rf_detector = load_rf_detector()

# Parámetros de espera para TruthScan
TRUTHSCAN_MAX_POLLS = 10
TRUTHSCAN_POLL_INTERVAL = 3  # segundos


def verificar_autenticidad(path_audio: str) -> Tuple[str, float]:
    """Analiza un audio usando TruthScan y cae al modelo RF si falla."""

    try:
        client = get_truthscan_client()
        logger.info("Analizando audio con TruthScan: %s", path_audio)
        return _analizar_con_truthscan(client, path_audio)
    except TruthScanError as exc:
        logger.warning("TruthScan no disponible (%s). Usando modelo RF.", exc)
    except Exception:
        logger.exception("Error inesperado usando TruthScan. Usando modelo RF.")

    # Fallback al modelo local
    return _analizar_con_rf(path_audio)


def _analizar_con_truthscan(client, path_audio: str) -> Tuple[str, float]:
    # 1. Limpieza de nombre (Requerido por docs: "remove spaces")
    file_name = os.path.basename(path_audio).replace(" ", "_") or "audio.wav"
    
    # 2. Obtener URL firmada
    presigned = client.get_presigned_url(file_name=file_name)
    
    # CORRECCIÓN: Usar las claves exactas de la documentación
    upload_url = presigned.get("presigned_url")
    file_path = presigned.get("file_path")

    if not upload_url or not file_path:
        logger.error(f"Respuesta TruthScan inesperada: {presigned}")
        raise TruthScanError("Respuesta inválida al solicitar presigned URL")

    # 3. Subir archivo
    content_type = mimetypes.guess_type(path_audio)[0] or "audio/wav"
    
    # CORRECCIÓN: Leemos todo el archivo a bytes aquí.
    # Esto evita el error 'EOF occurred in violation of protocol'
    with open(path_audio, "rb") as audio_file:
        file_bytes = audio_file.read()
        client.upload_file(upload_url, file_bytes, content_type)

    # 4. Iniciar detección
    detect_response = client.detect_audio(file_url=file_path)
    detection_id = detect_response.get("id")
    
    if not detection_id:
        raise TruthScanError("TruthScan no devolvió ID de detección")

    # 5. Polling de resultados
    for _ in range(TRUTHSCAN_MAX_POLLS):
        result: TruthScanResult = client.query_detection(detection_id)
        status = (result.status or "").lower()
        
        if status == "done":
            return _formatear_resultado_truthscan(result.raw)
        if status == "failed":
            raise TruthScanError("TruthScan reportó estado 'failed'")
            
        time.sleep(TRUTHSCAN_POLL_INTERVAL)

    raise TruthScanError("TruthScan tardó demasiado en responder")


def _formatear_resultado_truthscan(raw: dict | None) -> Tuple[str, float]:
    """
    Parsea la respuesta final basada en la documentación.
    Ejemplo respuesta: {"result": 0.873, "result_details": {...}}
    """
    raw = raw or {}
    
    # La documentación dice que "result" es un float (probabilidad de IA)
    # Si result > 0.5 es IA (fake), si no es humano (real).
    probability = raw.get("result")
    
    # Fallback si la estructura cambia
    if probability is None:
         # Intentar buscar en result_details por si acaso
         details = raw.get("result_details", {})
         probability = details.get("mean_ai_prob", 0.5)

    try:
        prob_float = float(probability)
    except (TypeError, ValueError):
        prob_float = 0.5

    # Definir etiqueta basada en umbral (asumiendo > 0.5 es IA)
    label = "fake" if prob_float > 0.5 else "real"
    
    return label, prob_float

def _analizar_con_rf(path_audio: str) -> Tuple[str, float]:
    try:
        # Procesar el audio con el detector RF
        result = rf_detector.process_audio(path_audio)
        if result.get('result') == 'error':
            logger.error("Modelo RF devolvió error: %s", result.get('message'))

            return "error", 0.5
        return result['result'].lower(), result.get('probability', 0.5)
    except Exception as exc:
        logger.exception("Error al procesar audio con RF: %s", exc)
        return "error", 0.5