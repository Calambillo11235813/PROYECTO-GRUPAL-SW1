import authService from './authService';
import { getAccessToken } from './config';

// Helper fetch con auth + reintento en 401 (una vez)
export async function fetchWithAuth(input, init = {}) {
  const makeRequest = async () => {
    const headers = new Headers(init.headers || {});

    // Adjuntar Authorization si existe token y el caller no lo deshabilita
    // (si el caller ya pasó Authorization, respetamos)
    if (!headers.has('Authorization')) {
      const token = getAccessToken();
      if (token) headers.set('Authorization', `Bearer ${token}`);
    }

    // Evitar forzar Content-Type si body es FormData
    const isFormData = (init.body && typeof FormData !== 'undefined' && init.body instanceof FormData);
    if (!isFormData && !headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json');
    }

    return fetch(input, { ...init, headers });
  };

  // Primer intento
  let response = await makeRequest();

  // Si 401: intentar refresh y reintentar una vez
  if (response.status === 401 && !init._retry) {
    const refreshed = await authService.refreshAccessToken();
    if (refreshed?.success && refreshed.accessToken) {
      const retryInit = { ...init, _retry: true };
      response = await fetchWithAuth(input, retryInit);
    }
  }

  return response;
}
