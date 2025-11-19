import React, { useState, useEffect } from "react";
import {
  BarChart3,
  TrendingUp,
  Code2,
  Clock,
  PieChart,
  CheckCircle2,
} from "lucide-react";
import codeAnalysisService from "../../../services/codeAnalysisService";

const CodeStatistics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    setLoading(true);
    try {
      const data = await codeAnalysisService.getStatistics();
      setStats(data);
    } catch (error) {
      console.error("Error al cargar estadísticas:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="text-center py-12 text-slate-400">
        No hay estadísticas disponibles
      </div>
    );
  }

  const calculatePercentage = (value, total) => {
    return total > 0 ? ((value / total) * 100).toFixed(1) : 0;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3">
        <BarChart3 className="w-8 h-8 text-cyan-400" />
        <div>
          <h2 className="text-2xl font-bold text-slate-100">
            Estadísticas de Análisis
          </h2>
          <p className="text-sm text-slate-400">
            Resumen de tendencias y patrones
          </p>
        </div>
      </div>

      {/* Main Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Análisis */}
        <div className="bg-gradient-to-br from-cyan-500/20 to-cyan-600/20 border border-cyan-500/50 rounded-xl p-6">
          <div className="flex items-center justify-between mb-2">
            <Code2 className="w-8 h-8 text-cyan-400" />
            <span className="text-3xl font-bold text-cyan-400">
              {stats.total_analisis || 0}
            </span>
          </div>
          <p className="text-sm text-slate-300">Total Análisis</p>
        </div>

        {/* Código IA */}
        <div className="bg-gradient-to-br from-red-500/20 to-red-600/20 border border-red-500/50 rounded-xl p-6">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="w-8 h-8 text-red-400" />
            <span className="text-3xl font-bold text-red-400">
              {stats.codigo_ia || 0}
            </span>
          </div>
          <p className="text-sm text-slate-300">Generado por IA</p>
          <p className="text-xs text-slate-400 mt-1">
            {calculatePercentage(stats.codigo_ia, stats.total_analisis)}% del
            total
          </p>
        </div>

        {/* Código Humano */}
        <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 border border-green-500/50 rounded-xl p-6">
          <div className="flex items-center justify-between mb-2">
            <CheckCircle2 className="w-8 h-8 text-green-400" />
            <span className="text-3xl font-bold text-green-400">
              {stats.codigo_humano || 0}
            </span>
          </div>
          <p className="text-sm text-slate-300">Código Humano</p>
          <p className="text-xs text-slate-400 mt-1">
            {calculatePercentage(stats.codigo_humano, stats.total_analisis)}%
            del total
          </p>
        </div>

        {/* Promedio Confianza */}
        <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 border border-purple-500/50 rounded-xl p-6">
          <div className="flex items-center justify-between mb-2">
            <PieChart className="w-8 h-8 text-purple-400" />
            <span className="text-3xl font-bold text-purple-400">
              {stats.promedio_confianza?.toFixed(1) || 0}%
            </span>
          </div>
          <p className="text-sm text-slate-300">Confianza Promedio</p>
        </div>
      </div>

      {/* Lenguajes Más Analizados */}
      {stats.por_lenguaje && Object.keys(stats.por_lenguaje).length > 0 && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
          <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center space-x-2">
            <Code2 className="w-6 h-6 text-cyan-400" />
            <span>Análisis por Lenguaje</span>
          </h3>

          <div className="space-y-3">
            {Object.entries(stats.por_lenguaje)
              .sort((a, b) => b[1] - a[1])
              .slice(0, 5)
              .map(([lenguaje, cantidad]) => (
                <div key={lenguaje}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-slate-300 capitalize">
                      {lenguaje}
                    </span>
                    <span className="text-sm font-bold text-cyan-400">
                      {cantidad}
                    </span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full transition-all duration-1000"
                      style={{
                        width: `${calculatePercentage(
                          cantidad,
                          stats.total_analisis
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Tendencia Temporal */}
      {stats.ultimos_30_dias && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
          <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center space-x-2">
            <Clock className="w-6 h-6 text-purple-400" />
            <span>Actividad Reciente (Últimos 30 días)</span>
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-900/50 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-cyan-400">
                {stats.ultimos_30_dias.total || 0}
              </p>
              <p className="text-xs text-slate-400 mt-1">Total</p>
            </div>

            <div className="bg-slate-900/50 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-red-400">
                {stats.ultimos_30_dias.ia || 0}
              </p>
              <p className="text-xs text-slate-400 mt-1">IA</p>
            </div>

            <div className="bg-slate-900/50 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-green-400">
                {stats.ultimos_30_dias.humano || 0}
              </p>
              <p className="text-xs text-slate-400 mt-1">Humano</p>
            </div>

            <div className="bg-slate-900/50 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-purple-400">
                {stats.ultimos_30_dias.promedio_confianza?.toFixed(1) || 0}%
              </p>
              <p className="text-xs text-slate-400 mt-1">Confianza Avg</p>
            </div>
          </div>
        </div>
      )}

      {/* Métricas Promedio */}
      {stats.metricas_promedio && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
          <h3 className="text-lg font-bold text-slate-100 mb-4">
            Métricas Promedio
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-sm text-slate-400 mb-2">
                Complejidad Ciclomática
              </p>
              <p className="text-2xl font-bold text-cyan-400">
                {stats.metricas_promedio.complejidad_ciclomatica?.toFixed(2) ||
                  "N/A"}
              </p>
            </div>

            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-sm text-slate-400 mb-2">
                Índice de Predictibilidad
              </p>
              <p className="text-2xl font-bold text-purple-400">
                {(
                  stats.metricas_promedio.indice_predictibilidad * 100
                )?.toFixed(1) || "N/A"}
                %
              </p>
            </div>

            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-sm text-slate-400 mb-2">
                Líneas Sospechosas Avg
              </p>
              <p className="text-2xl font-bold text-orange-400">
                {stats.metricas_promedio.lineas_sospechosas?.toFixed(0) ||
                  "N/A"}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeStatistics;
