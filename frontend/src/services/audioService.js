import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/audio/';

// Subir archivo de audio
export const uploadAudio = async (file, token) => {
  const formData = new FormData();
  formData.append('file', file);

  return axios.post(`${API_BASE_URL}upload/`, formData, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Obtener historial de análisis de audio (todos los registros)
export const getAllAudioUploads = async (token) => {
  return axios.get(API_BASE_URL, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
};

// Obtener audios del usuario autenticado
export const getUserAudioAnalysis = async (token) => {
  return axios.get(API_BASE_URL, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
};

// Descargar certificado PDF de un audio
export const downloadAudioCertificate = async (audioId, token) => {
  return axios.get(`${API_BASE_URL}certificado/${audioId}/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    responseType: 'blob', // Para descargar archivos
  });
};