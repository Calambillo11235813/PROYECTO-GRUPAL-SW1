import axios from 'axios';
import { API_ENDPOINTS, getAccessToken } from './config';

const API_BASE_URL = API_ENDPOINTS.AUDIO + '/';

// Subir archivo de audio
export const uploadAudio = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return axios.post(`${API_BASE_URL}upload/`, formData, {
    headers: {
      'Authorization': `Bearer ${getAccessToken()}`,
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Obtener historial de análisis de audio (todos los registros)
export const getAllAudioUploads = async () => {
  return axios.get(API_BASE_URL, {
    headers: {
      'Authorization': `Bearer ${getAccessToken()}`,
    },
  });
};

// Obtener audios del usuario autenticado
export const getUserAudioAnalysis = async () => {
  return axios.get(API_BASE_URL, {
    headers: {
      'Authorization': `Bearer ${getAccessToken()}`,
    },
  });
};

// Descargar certificado PDF de un audio
export const downloadAudioCertificate = async (audioId) => {
  return axios.get(`${API_BASE_URL}certificado/${audioId}/`, {
    headers: {
      'Authorization': `Bearer ${getAccessToken()}`,
    },
    responseType: 'blob', // Para descargar archivos
  });
};