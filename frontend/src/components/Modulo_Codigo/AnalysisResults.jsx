import React from "react";
import {
  Code2,
  FileCode,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  BarChart3,
  Zap,
  GitBranch,
  Brain,
} from "lucide-react";

const AnalysisResults = ({ analysisData }) => {
  if (!analysisData) return null;

  const {
    info_archivo,
    analisis_ia,
    resaltado_ia,
    metricas_codigo,
    patrones_sintacticos,
  } = analysisData;

  // Determinar color según confianza
  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return "text-red-400";
    if (confidence >= 0.6) return "text-orange-400";
    return "text-yellow-400";
  };

  const getConfidenceBg = (confidence) => {
    if (confidence >= 0.8) return "bg-red-500/20 border-red-500/50";
    if (confidence >= 0.6) return "bg-orange-500/20 border-orange-500/50";
    return "bg-yellow-500/20 border-yellow-500/50";
  };

  return (
    <div className="space-y-6">
      {/* Header Card - Resultado Principal */}
      <div
        className={`
        rounded-xl p-6 border-2 transition-all duration-300
        ${
          analisis_ia?.es_generado
            ? "bg-red-500/10 border-red-500/50 shadow-lg shadow-red-500/20"
            : "bg-green-500/10 border-green-500/50 shadow-lg shadow-green-500/20"
        }
      `}
      >
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              {analisis_ia?.es_generado ? (
                <Brain className="w-8 h-8 text-red-400" />
              ) : (
                <CheckCircle2 className="w-8 h-8 text-green-400" />
              )}
              <div>
                <h2 className="text-2xl font-bold text-slate-100">
                  {analisis_ia?.es_generado
                    ? "Código Generado por IA"
                    : "Código Humano"}
                </h2>
                <p className="text-sm text-slate-400">
                  Archivo: {info_archivo?.nombre} | Lenguaje:{" "}
                  {info_archivo?.lenguaje}
                </p>
              </div>
            </div>

            {/* Confianza */}
            <div className="mt-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-300">
                  Nivel de Confianza
                </span>
                <span
                  className={`text-lg font-bold ${getConfidenceColor(
                    analisis_ia?.confianza
                  )}`}
                >
                  {(analisis_ia?.confianza * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-1000 ${
                    analisis_ia?.es_generado
                      ? "bg-gradient-to-r from-red-500 to-orange-500"
                      : "bg-gradient-to-r from-green-500 to-cyan-500"
                  }`}
                  style={{ width: `${analisis_ia?.confianza * 100}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Grid de Métricas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Complejidad Ciclomática */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 hover:border-cyan-500/50 transition-all">
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-cyan-500/20 rounded-lg">
              <GitBranch className="w-5 h-5 text-cyan-400" />
            </div>
            <h3 className="font-semibold text-slate-200">
              Complejidad Ciclomática
            </h3>
          </div>
          <p className="text-2xl font-bold text-cyan-400">
            {metricas_codigo?.complejidad_ciclomatica?.toFixed(2) || "N/A"}
          </p>
          <p className="text-xs text-slate-400 mt-1">Promedio por función</p>
        </div>

        {/* Índice de Predictibilidad */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 hover:border-purple-500/50 transition-all">
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-purple-500/20 rounded-lg">
              <TrendingUp className="w-5 h-5 text-purple-400" />
            </div>
            <h3 className="font-semibold text-slate-200">Predictibilidad</h3>
          </div>
          <p className="text-2xl font-bold text-purple-400">
            {(patrones_sintacticos?.indice_predictibilidad * 100)?.toFixed(1) ||
              "N/A"}
            %
          </p>
          <p className="text-xs text-slate-400 mt-1">Índice calculado</p>
        </div>

        {/* Líneas Sospechosas */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 hover:border-orange-500/50 transition-all">
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-orange-500/20 rounded-lg">
              <AlertTriangle className="w-5 h-5 text-orange-400" />
            </div>
            <h3 className="font-semibold text-slate-200">Líneas Sospechosas</h3>
          </div>
          <p className="text-2xl font-bold text-orange-400">
            {resaltado_ia?.total_lineas_sospechosas || 0}
          </p>
          <p className="text-xs text-slate-400 mt-1">Fragmentos detectados</p>
        </div>
      </div>

      {/* Patrones Sintácticos */}
      {patrones_sintacticos && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-4">
            <BarChart3 className="w-6 h-6 text-cyan-400" />
            <h3 className="text-lg font-bold text-slate-100">
              Análisis de Patrones Sintácticos
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Variabilidad de Funciones */}
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-sm text-slate-400 mb-2">
                Variabilidad en Funciones
              </p>
              <p className="text-xl font-bold text-slate-200">
                {patrones_sintacticos.variabilidad_funciones?.toFixed(2) ||
                  "N/A"}
              </p>
              <p className="text-xs text-slate-500 mt-1">Desviación estándar</p>
            </div>

            {/* Estructuras de Control */}
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-sm text-slate-400 mb-2">Patrones de Control</p>
              <div className="flex flex-wrap gap-2 mt-2">
                {patrones_sintacticos.patrones_control &&
                  Object.entries(patrones_sintacticos.patrones_control).map(
                    ([key, value]) => (
                      <span
                        key={key}
                        className="px-2 py-1 bg-cyan-500/20 text-cyan-300 text-xs rounded"
                      >
                        {key}: {value}
                      </span>
                    )
                  )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Líneas Sospechosas Detalladas */}
      {resaltado_ia?.lineas_marcadas &&
        resaltado_ia.lineas_marcadas.length > 0 && (
          <div className="bg-slate-800/50 border border-orange-500/50 rounded-xl p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Code2 className="w-6 h-6 text-orange-400" />
              <h3 className="text-lg font-bold text-slate-100">
                Fragmentos Sospechosos Detectados
              </h3>
            </div>

            <div className="space-y-3 max-h-96 overflow-y-auto">
              {resaltado_ia.lineas_marcadas.slice(0, 10).map((linea, idx) => (
                <div
                  key={idx}
                  className="bg-slate-900/50 border border-orange-500/30 rounded-lg p-3"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-400">
                      Línea {linea.numero}
                    </span>
                    <span
                      className={`text-xs font-bold ${getConfidenceColor(
                        linea.confianza
                      )}`}
                    >
                      {(linea.confianza * 100).toFixed(0)}% confianza
                    </span>
                  </div>
                  <code className="text-sm text-orange-300 font-mono block whitespace-pre-wrap">
                    {linea.codigo}
                  </code>
                  {linea.razon && (
                    <p className="text-xs text-slate-500 mt-2">
                      Razón: {linea.razon}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

      {/* Naming Conventions */}
      {metricas_codigo?.naming_conventions && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-4">
            <FileCode className="w-6 h-6 text-purple-400" />
            <h3 className="text-lg font-bold text-slate-100">
              Convenciones de Nomenclatura
            </h3>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {Object.entries(metricas_codigo.naming_conventions).map(
              ([key, value]) => (
                <div
                  key={key}
                  className="bg-slate-900/50 rounded-lg p-3 text-center"
                >
                  <p className="text-2xl font-bold text-purple-400">{value}</p>
                  <p className="text-xs text-slate-400 mt-1 capitalize">
                    {key.replace("_", " ")}
                  </p>
                </div>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;
