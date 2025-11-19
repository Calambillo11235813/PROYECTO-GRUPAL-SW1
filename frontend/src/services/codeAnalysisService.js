const API_BASE_URL = "http://127.0.0.1:8000/api/codigo";

class CodeAnalysisService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  getAuthHeaders() {
    const token = localStorage.getItem("access_token");
    return {
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  // HU-013: Subir archivo de código
  async uploadCodeFile(file) {
    const formData = new FormData();
    formData.append("archivo", file);
    const { fetchWithAuth } = await import('./fetchClient');
    const response = await fetchWithAuth(`${this.baseURL}/subir/`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Error al subir el archivo");
    }

    return await response.json();
  }

  // HU-014, HU-015: Obtener detalle de análisis
  async getAnalysisDetail(id) {
    const { fetchWithAuth } = await import('./fetchClient');
    const response = await fetchWithAuth(`${this.baseURL}/analisis/${id}/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error("Error al obtener el análisis");
    }

    return await response.json();
  }

  // HU-019: Historial de análisis con filtros
  async getHistory(filters = {}) {
    const params = new URLSearchParams();

    if (filters.nombre) params.append("nombre", filters.nombre);
    if (filters.lenguaje) params.append("lenguaje", filters.lenguaje);
    if (filters.ia !== undefined) params.append("ia", filters.ia);
    if (filters.inicio) params.append("inicio", filters.inicio);
    if (filters.fin) params.append("fin", filters.fin);

    const { fetchWithAuth } = await import('./fetchClient');
    const response = await fetchWithAuth(
      `${this.baseURL}/historial/?${params.toString()}`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }
    );

    if (!response.ok) {
      throw new Error("Error al obtener el historial");
    }

    return await response.json();
  }

  // HU-019: Comparar análisis side-by-side
  async compareAnalysis(ids) {
    const { fetchWithAuth } = await import('./fetchClient');
    const response = await fetchWithAuth(`${this.baseURL}/historial/comparar/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids }),
    });

    if (!response.ok) {
      throw new Error("Error al comparar análisis");
    }

    return await response.json();
  }

  // HU-019: Estadísticas del historial
  async getStatistics() {
    const { fetchWithAuth } = await import('./fetchClient');
    const response = await fetchWithAuth(`${this.baseURL}/historial/estadisticas/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error("Error al obtener estadísticas");
    }

    return await response.json();
  }

  // HU-018: Descargar reporte PDF
  async downloadPDFReport(id) {
    const { fetchWithAuth } = await import('./fetchClient');
    const response = await fetchWithAuth(`${this.baseURL}/reporte/pdf/${id}/`, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error("Error al descargar el reporte PDF");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `reporte_${id}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }

  // HU-018: Obtener reporte JSON
  async getJSONReport(id) {
    const { fetchWithAuth } = await import('./fetchClient');
    const response = await fetchWithAuth(`${this.baseURL}/reporte/json/${id}/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error("Error al obtener el reporte JSON");
    }

    return await response.json();
  }

  // HU-019: Exportar historial completo
  async exportHistoryJSON() {
    const { fetchWithAuth } = await import('./fetchClient');
    const response = await fetchWithAuth(`${this.baseURL}/historial/exportar/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error("Error al exportar el historial");
    }

    const data = await response.json();

    // Descargar como archivo JSON
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `historial_codigo_${
      new Date().toISOString().split("T")[0]
    }.json`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
}

export default new CodeAnalysisService();
