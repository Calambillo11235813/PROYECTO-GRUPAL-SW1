import axios from 'axios';
import { BASE_URL } from './config';
import authService from './authService';

// Cliente Axios con interceptores (401 -> refresh -> reintentar una vez)
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 20000,
});

// Adjuntar Authorization en cada request si existe
apiClient.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
    }
  } catch {}
  return config;
});

// Manejar 401: intentar refresh y reintentar una vez
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config || {};
    const status = error?.response?.status;

    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const result = await authService.refreshAccessToken();
      if (result?.success && result.accessToken) {
        // Actualizar header y reintentar
        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers['Authorization'] = `Bearer ${result.accessToken}`;
        return apiClient(originalRequest);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
