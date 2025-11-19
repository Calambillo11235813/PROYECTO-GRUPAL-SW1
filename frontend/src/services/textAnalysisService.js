import { API_ENDPOINTS, getAuthHeaders } from './config';

const API_BASE_URL = API_ENDPOINTS.TEXTO; // ← MANTENER IGUAL

class TextAnalysisService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Headers con autenticación opcional - MEJORADO
  getHeaders(includeAuth = false, isFormData = false) {
    return getAuthHeaders(includeAuth, isFormData);
  }

  // Validar texto de entrada - NUEVA FUNCIÓN
  validateText(texto) {
    if (!texto || typeof texto !== 'string') {
      throw new Error('El texto es requerido y debe ser una cadena válida');
    }
    
    if (texto.trim().length === 0) {
      throw new Error('El texto no puede estar vacío');
    }
    
    if (texto.length > 10000) {
      throw new Error('El texto es demasiado largo (máximo 10,000 caracteres)');
    }
    
    return texto.trim();
  }

  // Validar archivo - NUEVA FUNCIÓN
  validateFile(file) {
    if (!file || !(file instanceof File)) {
      throw new Error('Debe seleccionar un archivo válido');
    }

    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = [
      'text/plain',
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword'
    ];

    if (file.size > maxSize) {
      throw new Error('El archivo es demasiado grande (máximo 5MB)');
    }

    if (!allowedTypes.includes(file.type)) {
      throw new Error('Tipo de archivo no compatible. Solo se permiten: TXT, PDF, DOCX');
    }

    return file;
  }

  // Estructura de respuesta consistente - NUEVA FUNCIÓN
  createResponse(success, data = null, error = null) {
    return {
      success,
      data,
      error
    };
  }

  // Estado del servicio - MANTENER RUTA ORIGINAL
  async getServiceStatus() {
    try {
      console.log('🔍 Verificando estado del servicio...');
      
      const response = await fetch(`${this.baseURL}/`, { // ← RUTA ORIGINAL
        method: 'GET',
        headers: this.getHeaders()
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Estado del servicio obtenido:', data);
      return this.createResponse(true, data);

    } catch (error) {
      console.error('❌ Error verificando estado:', error);
      return this.createResponse(false, null, error.message);
    }
  }

  // Analizar texto - MANTENER RUTA ORIGINAL
  async analyzeText(texto, modelo = 'B') {
    try {
      console.log(`🔍 Analizando texto con modelo ${modelo}...`);
      
      // Validar entrada - MEJORADO
      const textoLimpio = this.validateText(texto);
      
      if (!['B', 'N'].includes(modelo.toUpperCase())) {
        throw new Error('Modelo debe ser "B" o "N"');
      }

      const response = await fetch(`${this.baseURL}/analizar/`, { // ← RUTA ORIGINAL
        method: 'POST',
        headers: this.getHeaders(true), // CORREGIDO: auth headers
        body: JSON.stringify({ 
          texto: textoLimpio, 
          modelo: modelo.toUpperCase() 
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.detail || `HTTP ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Análisis completado:', data);
      return this.createResponse(true, data);

    } catch (error) {
      console.error('❌ Error en análisis de texto:', error);
      return this.createResponse(false, null, error.message);
    }
  }

  // Comparar modelos - MANTENER RUTA ORIGINAL
  async compareModels(texto) {
    try {
      console.log('⚖️ Comparando modelos...');
      
      const textoLimpio = this.validateText(texto);

      const response = await fetch(`${this.baseURL}/comparar/`, { // ← RUTA ORIGINAL
        method: 'POST',
        headers: this.getHeaders(true), // CORREGIDO: auth headers
        body: JSON.stringify({ texto: textoLimpio })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.detail || `HTTP ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Comparación completada:', data);
      return this.createResponse(true, data);

    } catch (error) {
      console.error('❌ Error en comparación de modelos:', error);
      return this.createResponse(false, null, error.message);
    }
  }

  // Analizar archivo - MANTENER RUTA ORIGINAL
  async analyzeFile(file, modelo = 'B') {
    try {
      console.log(`📄 Analizando archivo con modelo ${modelo}:`, file.name);
      
      const validFile = this.validateFile(file);
      
      if (!['B', 'N'].includes(modelo.toUpperCase())) {
        throw new Error('Modelo debe ser "B" o "N"');
      }

      const formData = new FormData();
      formData.append('archivo', validFile);
      formData.append('modelo', modelo.toUpperCase());

      const response = await fetch(`${this.baseURL}/analizar-archivo/`, { // ← RUTA ORIGINAL
        method: 'POST',
        headers: this.getHeaders(true, true), // CORREGIDO: FormData headers
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.detail || `HTTP ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Análisis de archivo completado:', data);
      return this.createResponse(true, data);

    } catch (error) {
      console.error('❌ Error en análisis de archivo:', error);
      return this.createResponse(false, null, error.message);
    }
  }
}

// Exportar instancia singleton - MANTENER IGUAL
export const textAnalysisService = new TextAnalysisService();
export default textAnalysisService;