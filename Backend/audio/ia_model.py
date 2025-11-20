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
    file_name = os.path.basename(path_audio).replace(" ", "_") or "audio.wav"
    presigned = client.get_presigned_url(file_name=file_name)

    upload_url = presigned.get("url") or presigned.get("upload_url")
    file_path = presigned.get("file_path") or presigned.get("fileUrl")
    if not upload_url or not file_path:
        raise TruthScanError("Respuesta inválida al solicitar presigned URL")

    content_type = mimetypes.guess_type(path_audio)[0] or "audio/wav"
    with open(path_audio, "rb") as audio_file:
        client.upload_file(upload_url, audio_file.read(), content_type)

    detect_response = client.detect_audio(file_url=file_path)
    detection_id = detect_response.get("id") or detect_response.get("detection_id")
    if not detection_id:
        raise TruthScanError("TruthScan no devolvió ID de detección")

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
    raw = raw or {}
    result = (raw.get("result") or raw.get("label") or "desconocido").lower()
    probability = raw.get("probability") or raw.get("confidence")
    try:
        probability = float(probability)
    except (TypeError, ValueError):
        probability = 0.5
    return result, probability


def _analizar_con_rf(path_audio: str) -> Tuple[str, float]:
    try:
        result = rf_detector.process_audio(path_audio)
        if result.get('result') == 'error':
            logger.error("Modelo RF devolvió error: %s", result.get('message'))
            return "error", 0.5
        return result['result'].lower(), result.get('probability', 0.5)
    except Exception as exc:
        logger.exception("Error al procesar audio con RF: %s", exc)
        return "error", 0.5
