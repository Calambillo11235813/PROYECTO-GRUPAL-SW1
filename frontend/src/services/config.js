// config.js - Configuración centralizada para servicios
const BASE_URL = 'http://127.0.0.1:8000/api';

// Función para obtener headers de autenticación
export const getAuthHeaders = (includeAuth = false, isFormData = false) => {
  const headers = {};

  // Solo agregar Content-Type si NO es FormData
  if (!isFormData) {
    headers['Content-Type'] = 'application/json';
  }

  if (includeAuth) {
    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  return headers;
};

// Función para obtener token de acceso
export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

// Función para obtener token de refresh
export const getRefreshToken = () => {
  return localStorage.getItem('refresh_token');
};

// URLs específicas por servicio
export const API_ENDPOINTS = {
  AUTH: `${BASE_URL}/auth`,
  TEXTO: `${BASE_URL}/texto`,
  AUDIO: `${BASE_URL}/audio`
};

// Endpoint para el servicio de video
API_ENDPOINTS.VIDEO = `${BASE_URL}/video`;

export { BASE_URL };