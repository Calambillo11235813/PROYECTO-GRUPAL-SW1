import { API_ENDPOINTS, getAuthHeaders, getAccessToken, getRefreshToken } from './config';

class AuthService {
  constructor() {
    this.baseURL = API_ENDPOINTS.AUTH;
  }

  // Almacenar tokens en localStorage
  setTokens(accessToken, refreshToken) {
    if (accessToken) localStorage.setItem('access_token', accessToken);
    if (refreshToken) localStorage.setItem('refresh_token', refreshToken);
  }

  // Limpiar tokens de localStorage
  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  // Wrappers para obtener tokens (usa las funciones de config si están disponibles)
  getAccessToken() {
    try {
      return getAccessToken();
    } catch {
      return localStorage.getItem('access_token');
    }
  }

  getRefreshToken() {
    try {
      return getRefreshToken();
    } catch {
      return localStorage.getItem('refresh_token');
    }
  }

  // Registro de usuario
  async register(userData) {
    try {
      const response = await fetch(`${this.baseURL}/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Error en el registro');
      }

      // Almacenar tokens si el registro incluye login automático
      if (data.tokens) {
        this.setTokens(data.tokens.access, data.tokens.refresh);
        if (data.user) {
          localStorage.setItem('user', JSON.stringify(data.user));
        }
      }

      return {
        success: true,
        data: data,
        user: data.user,
        tokens: data.tokens
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Login de usuario
  async login(credentials) {
    try {
      const response = await fetch(`${this.baseURL}/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Credenciales inválidas');
      }

      // Almacenar tokens y datos del usuario
      if (data.tokens) {
        this.setTokens(data.tokens.access, data.tokens.refresh);
      }
      
      if (data.user) {
        localStorage.setItem('user', JSON.stringify(data.user));
      }

      return {
        success: true,
        data: data,
        user: data.user,
        tokens: data.tokens
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Logout de usuario
  async logout() {
    try {
      const refreshToken = getRefreshToken();
      
      if (refreshToken) {
        await fetch(`${this.baseURL}/logout/`, {
          method: 'POST',
          headers: getAuthHeaders(true),
          body: JSON.stringify({ refresh: refreshToken })
        });
      }
    } catch (error) {
      console.error('Error durante logout:', error);
    } finally {
      // Limpiar tokens independientemente del resultado
      this.clearTokens();
    }

    return { success: true };
  }

  // Obtener perfil del usuario autenticado
  async getProfile() {
    try {
      const response = await fetch(`${this.baseURL}/profile/`, {
        method: 'GET',
        headers: getAuthHeaders(true)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Error al obtener perfil');
      }

      return {
        success: true,
        data: data
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Refrescar token de acceso
  async refreshAccessToken() {
    try {
      const refreshToken = getRefreshToken();
      
      if (!refreshToken) {
        throw new Error('No hay refresh token disponible');
      }

      const response = await fetch(`${this.baseURL}/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      // Actualizar access token
      localStorage.setItem('access_token', data.access);

      return {
        success: true,
        accessToken: data.access
      };
    } catch (error) {
      // Si falla el refresh, limpiar tokens
      this.clearTokens();
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Obtener usuario desde localStorage
  getCurrentUser() {
    try {
      const userStr = localStorage.getItem('user');
      return userStr ? JSON.parse(userStr) : null;
    } catch {
      return null;
    }
  }
}

// Exportar instancia singleton
export const authService = new AuthService();
export default authService;