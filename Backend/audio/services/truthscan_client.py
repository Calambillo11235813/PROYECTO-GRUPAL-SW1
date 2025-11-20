"""Helper para interactuar con TruthScan AI Audio Detection API."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class TruthScanError(Exception):
    """Error genérico al interactuar con TruthScan."""


class TruthScanAuthError(TruthScanError):
    """Error de autenticación o créditos insuficientes."""


class TruthScanValidationError(TruthScanError):
    """Error de validación al invocar TruthScan."""


@dataclass
class TruthScanResult:
    status: str
    probability: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None


class TruthScanClient:
    """Cliente HTTP mínimo para TruthScan."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> None:
        self.base_url = base_url or settings.TRUTHSCAN_BASE_URL
        self.api_key = api_key or settings.TRUTHSCAN_API_KEY
        self.timeout = timeout or settings.TRUTHSCAN_TIMEOUT

        if not self.api_key:
            raise TruthScanError("TRUTHSCAN_API_KEY no está configurado")

        self._auth_headers = {"apikey": self.api_key}

    def get_presigned_url(self, file_name: str) -> Dict[str, Any]:
        url = f"{self.base_url}/get-presigned-url"
        params = {"file_name": file_name}
        response = requests.get(
            url,
            params=params,
            headers=self._auth_headers,
            timeout=self.timeout,
        )
        self._ensure_success(response)
        return response.json()

    def upload_file(self, presigned_url: str, file_data: bytes, content_type: str) -> None:
        """
        Sube el archivo a S3/Spaces.
        Recibe 'file_data' como BYTES para asegurar el cálculo de Content-Length.
        """
        # DigitalOcean Spaces/S3 requiere saber el tamaño exacto
        file_size = len(file_data)

        headers = {
            "Content-Type": content_type,
            "Content-Length": str(file_size),  # Obligatorio para evitar EOF error
            "x-amz-acl": "private"             # Recomendado por la documentación
        }

        try:
            response = requests.put(
                presigned_url,
                data=file_data, # Pasamos bytes, no el objeto archivo
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.SSLError:
            # Reintento simple si la conexión se corta
            logger.warning("Reintentando subida por error SSL...")
            response = requests.put(
                presigned_url,
                data=file_data,
                headers=headers,
                timeout=self.timeout,
            )

        if response.status_code >= 400:
            logger.error("Error en upload de TruthScan (%s): %s", response.status_code, response.text)
            raise TruthScanError("No se pudo subir el archivo a TruthScan")
    
    def detect_audio(self, file_url: str, analyze_seconds: Optional[int] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/detect"
        payload = {"key": self.api_key, "url": file_url}
        if analyze_seconds is not None:
            payload["analyzeUpToSeconds"] = analyze_seconds

        response = requests.post(
            url,
            json=payload,
            headers=self._auth_headers,
            timeout=self.timeout,
        )
        self._ensure_success(response)
        return response.json()

    def query_detection(self, detection_id: str) -> TruthScanResult:
        url = f"{self.base_url}/query"
        payload = {"key": self.api_key, "id": detection_id}
        response = requests.post(
            url,
            json=payload,
            headers=self._auth_headers,
            timeout=self.timeout,
        )
        self._ensure_success(response)
        data = response.json()
        return TruthScanResult(
            status=data.get("status", "unknown"),
            probability=data.get("probability"),
            raw=data,
        )

    def _ensure_success(self, response: requests.Response) -> None:
        if response.status_code < 400:
            return

        if response.status_code in (401, 403):
            raise TruthScanAuthError(response.text)
        if response.status_code == 422:
            raise TruthScanValidationError(response.text)

        logger.error(
            "TruthScan respondió %s: %s",
            response.status_code,
            response.text,
        )
        raise TruthScanError("Error al comunicarse con TruthScan")


def get_truthscan_client() -> TruthScanClient:
    return TruthScanClient()