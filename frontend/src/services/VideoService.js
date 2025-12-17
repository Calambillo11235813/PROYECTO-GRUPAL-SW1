/**
 * VideoService.js
 * Servicio para manejar subidas de video y análisis (HU-11 a HU-14).
 */
import apiClient from './apiClient';

const VideoService = {
  // Subir video usando FormData. onUploadProgress es opcional.
  uploadVideo: (formData, onUploadProgress) => {
    return apiClient.post('/video/videoupload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress,
      // Algunos videos grandes pueden tardar más en subir
      timeout: 120000, // 2 minutos
    });
  },

  // Disparar análisis para un video existente (endpoint action)
  triggerAnalyze: (videoId) =>
    apiClient.post(`/video/videoupload/${videoId}/analyze/`, null, {
      // El análisis con MTCNN + Tensorflow puede tardar bastante
      timeout: 600000, // 10 minutos
    }),

  // Listar resultados de análisis
  listAnalyses: () => apiClient.get('/video/analysisresult/'),

  // Obtener un resultado de análisis específico
  getAnalysis: (id) => apiClient.get(`/video/analysisresult/${id}/`),

  // Eliminar un resultado de análisis
  deleteAnalysis: (id) => apiClient.delete(`/video/analysisresult/${id}/`),

  // Eliminar todos los resultados de análisis
  deleteAllAnalyses: () => apiClient.delete('/video/analysisresult/delete-all/'),
};

export default VideoService;
