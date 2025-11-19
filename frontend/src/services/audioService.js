import apiClient from './apiClient';
import { API_ENDPOINTS } from './config';

const API_BASE_URL = API_ENDPOINTS.AUDIO + '/';

// Subir archivo de audio
export const uploadAudio = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return apiClient.post(`${API_BASE_URL}upload/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

// Obtener historial de análisis de audio (todos los registros)
export const getAllAudioUploads = async () => {
  return apiClient.get(API_BASE_URL);
};

// Obtener audios del usuario autenticado
export const getUserAudioAnalysis = async () => {
  return apiClient.get(API_BASE_URL);
};

// Descargar certificado PDF de un audio
export const downloadAudioCertificate = async (audioId) => {
  return apiClient.get(`${API_BASE_URL}certificado/${audioId}/`, {
    responseType: 'blob',
  });
};