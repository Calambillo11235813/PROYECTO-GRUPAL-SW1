import React, { useState, useEffect } from "react";
import {
  History,
  Search,
  Filter,
  Download,
  GitCompare,
  Calendar,
  Code2,
  ChevronDown,
  X,
  FileText,
  Eye,
} from "lucide-react";
import codeAnalysisService from "../../services/codeAnalysisService";
import { useNavigate } from "react-router-dom";

const CodeHistory = () => {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);
  const [selectedItems, setSelectedItems] = useState([]);
  const navigate = useNavigate();

  const [filters, setFilters] = useState({
    nombre: "",
    lenguaje: "",
    ia: "",
    inicio: "",
    fin: "",
  });

  useEffect(() => {
    const loadHistory = async () => {
      setLoading(true);
      try {
        const data = await codeAnalysisService.getHistory(filters);
        setHistory(data);
        setFilteredHistory(data);
      } catch (error) {
        console.error("Error al cargar historial:", error);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, [filters]);

  const applyFilters = async () => {
    setLoading(true);
    try {
      const data = await codeAnalysisService.getHistory(filters);
      setFilteredHistory(data);
    } catch (error) {
      console.error("Error al aplicar filtros:", error);
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setFilters({
      nombre: "",
      lenguaje: "",
      ia: "",
      inicio: "",
      fin: "",
    });
    setFilteredHistory(history);
  };

  const handleExportHistory = async () => {
    try {
      await codeAnalysisService.exportHistoryJSON();
    } catch (error) {
      console.error("Error al exportar:", error);
    }
  };

  const toggleItemSelection = (id) => {
    setSelectedItems((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleCompare = () => {
    if (selectedItems.length >= 2) {
      navigate(`/codigo/comparar?ids=${selectedItems.join(",")}`);
    }
  };

  const viewAnalysis = (id) => {
    navigate(`/codigo/analisis/${id}`);
  };

  if (loading && filteredHistory.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <History className="w-8 h-8 text-cyan-400" />
          <div>
            <h2 className="text-2xl font-bold text-slate-100">
              Historial de Análisis
            </h2>
            <p className="text-sm text-slate-400">
              {filteredHistory.length} análisis registrados
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          {selectedItems.length >= 2 && (
            <button
              onClick={handleCompare}
              className="flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
            >
              <GitCompare className="w-4 h-4" />
              <span>Comparar ({selectedItems.length})</span>
            </button>
          )}

          <button
            onClick={handleExportHistory}
            className="flex items-center space-x-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Exportar</span>
          </button>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              showFilters
                ? "bg-cyan-600 text-white"
                : "bg-slate-700 text-slate-200 hover:bg-slate-600"
            }`}
          >
            <Filter className="w-4 h-4" />
            <span>Filtros</span>
            <ChevronDown
              className={`w-4 h-4 transition-transform ${
                showFilters ? "rotate-180" : ""
              }`}
            />
          </button>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Nombre */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Nombre de Archivo
              </label>
              <input
                type="text"
                value={filters.nombre}
                onChange={(e) =>
                  setFilters({ ...filters, nombre: e.target.value })
                }
                placeholder="Buscar por nombre..."
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>

            {/* Lenguaje */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Lenguaje
              </label>
              <select
                value={filters.lenguaje}
                onChange={(e) =>
                  setFilters({ ...filters, lenguaje: e.target.value })
                }
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              >
                <option value="">Todos</option>
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
                <option value="csharp">C#</option>
              </select>
            </div>

            {/* Tipo de Código */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Tipo de Código
              </label>
              <select
                value={filters.ia}
                onChange={(e) => setFilters({ ...filters, ia: e.target.value })}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              >
                <option value="">Todos</option>
                <option value="true">Generado por IA</option>
                <option value="false">Código Humano</option>
              </select>
            </div>

            {/* Fecha Inicio */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Fecha Inicio
              </label>
              <input
                type="date"
                value={filters.inicio}
                onChange={(e) =>
                  setFilters({ ...filters, inicio: e.target.value })
                }
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>

            {/* Fecha Fin */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Fecha Fin
              </label>
              <input
                type="date"
                value={filters.fin}
                onChange={(e) =>
                  setFilters({ ...filters, fin: e.target.value })
                }
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={applyFilters}
              className="flex items-center space-x-2 px-6 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-colors"
            >
              <Search className="w-4 h-4" />
              <span>Aplicar Filtros</span>
            </button>

            <button
              onClick={clearFilters}
              className="flex items-center space-x-2 px-6 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg transition-colors"
            >
              <X className="w-4 h-4" />
              <span>Limpiar</span>
            </button>
          </div>
        </div>
      )}

      {/* History List */}
      <div className="space-y-3">
        {filteredHistory.length === 0 ? (
          <div className="text-center py-12 bg-slate-800/50 border border-slate-700/50 rounded-xl">
            <FileText className="w-16 h-16 text-slate-600 mx-auto mb-4" />
            <p className="text-slate-400">No hay análisis registrados</p>
          </div>
        ) : (
          filteredHistory.map((item) => (
            <div
              key={item.id}
              className={`
                bg-slate-800/50 border rounded-xl p-4 transition-all hover:border-cyan-500/50
                ${
                  selectedItems.includes(item.id)
                    ? "border-cyan-500 bg-cyan-500/10"
                    : "border-slate-700/50"
                }
              `}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 flex-1">
                  {/* Checkbox */}
                  <input
                    type="checkbox"
                    checked={selectedItems.includes(item.id)}
                    onChange={() => toggleItemSelection(item.id)}
                    className="w-5 h-5 rounded border-slate-600 text-cyan-500 focus:ring-cyan-500"
                  />

                  {/* Icon */}
                  <div
                    className={`
                    p-3 rounded-lg
                    ${item.ia_es_generado ? "bg-red-500/20" : "bg-green-500/20"}
                  `}
                  >
                    <Code2
                      className={`w-6 h-6 ${
                        item.ia_es_generado ? "text-red-400" : "text-green-400"
                      }`}
                    />
                  </div>

                  {/* Info */}
                  <div className="flex-1">
                    <h3 className="font-semibold text-slate-200">
                      {item.nombre_archivo}
                    </h3>
                    <div className="flex items-center space-x-4 text-sm text-slate-400 mt-1">
                      <span className="flex items-center space-x-1">
                        <Code2 className="w-4 h-4" />
                        <span>{item.lenguaje || "N/A"}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>
                          {new Date(item.fecha_analisis).toLocaleDateString()}
                        </span>
                      </span>
                      <span
                        className={`px-2 py-0.5 rounded text-xs font-semibold ${
                          item.ia_es_generado
                            ? "bg-red-500/20 text-red-300"
                            : "bg-green-500/20 text-green-300"
                        }`}
                      >
                        {item.ia_es_generado ? "IA" : "Humano"}
                      </span>
                      <span className="text-cyan-400 font-semibold">
                        {(item.ia_confianza * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <button
                  onClick={() => viewAnalysis(item.id)}
                  className="flex items-center space-x-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-colors"
                >
                  <Eye className="w-4 h-4" />
                  <span>Ver Detalle</span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default CodeHistory;
