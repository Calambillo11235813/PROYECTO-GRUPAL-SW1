import React, { useState } from "react";
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
  Eye,
  EyeOff,
} from "lucide-react";

const AnalysisResults = ({ analysisData }) => {
  const [showCode, setShowCode] = useState(false);

  if (!analysisData) return null;

  const {
    info_archivo,
    analisis_ia,
    resaltado_ia,
    metricas_codigo,
    patrones_sintacticos,
    codigo_original,
  } = analysisData;

  // Determinar color según confianza
  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return "text-red-400";
    if (confidence >= 0.6) return "text-orange-400";
    return "text-yellow-400";
  };

  // Función para renderizar código con líneas marcadas
  const renderCodeWithMarkedLines = () => {
    if (!codigo_original) return null;

    const lines = codigo_original.split("\n");
    const suspiciousLines = resaltado_ia?.lineas_sospechosas || [];
    // El backend devuelve 'bloques' en la respuesta JSON
    const suspiciousBlocks = resaltado_ia?.bloques || [];

    // Crear un Set de líneas sospechosas para búsqueda rápida
    const suspiciousSet = new Set(suspiciousLines);

    // Crear un Set de rangos de bloques sospechosos
    const blockRanges = suspiciousBlocks.map((block) => ({
      start: block.inicio,
      end: block.fin,
    }));

    return (
      <div className="bg-slate-900/50 border-t border-slate-700/50">
        <div className="relative">
          <pre className="text-sm text-slate-300 font-mono overflow-x-auto bg-slate-950 p-4 rounded-lg max-h-[600px] overflow-y-auto">
            <code>
              {lines.map((line, index) => {
                const lineNumber = index + 1;
                const isSuspicious = suspiciousSet.has(lineNumber);
                
                // Verificar si está en un bloque sospechoso
                const isInBlock = blockRanges.some(
                  (block) => lineNumber >= block.start && lineNumber <= block.end
                );

                // Determinar el estilo según el tipo de sospecha
                let lineStyle = "";
                if (isSuspicious && isInBlock) {
                  // Línea sospechosa que también está en un bloque
                  lineStyle = "bg-red-500/30 border-l-4 border-red-500";
                } else if (isSuspicious) {
                  // Solo línea sospechosa
                  lineStyle = "bg-orange-500/20 border-l-4 border-orange-500";
                } else if (isInBlock) {
                  // Solo en bloque sospechoso
                  lineStyle = "bg-purple-500/15 border-l-4 border-purple-500";
                }

                return (
                  <div
                    key={index}
                    className={`flex items-start ${lineStyle} px-2 py-1 hover:bg-slate-800/50 transition-colors`}
                  >
                    <span className="text-slate-500 text-xs mr-4 w-12 text-right select-none">
                      {lineNumber}
                    </span>
                    <span className="flex-1">{line || " "}</span>
                    {isSuspicious && (
                      <span className="ml-2 text-orange-400 text-xs" title="Línea sospechosa">
                        ⚠️
                      </span>
                    )}
                  </div>
                );
              })}
            </code>
          </pre>
        </div>
        
        {/* Leyenda */}
        <div className="p-4 bg-slate-800/50 border-t border-slate-700/50">
          <div className="flex items-center space-x-6 text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-orange-500/20 border-l-4 border-orange-500"></div>
              <span className="text-slate-300">Línea sospechosa</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-red-500/30 border-l-4 border-red-500"></div>
              <span className="text-slate-300">Línea en bloque sospechoso</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-purple-500/15 border-l-4 border-purple-500"></div>
              <span className="text-slate-300">En bloque sospechoso</span>
            </div>
          </div>
        </div>
      </div>
    );
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
          </div>
          
          {/* Botón para ver código */}
          {codigo_original && (
            <button
              onClick={() => setShowCode(!showCode)}
              className="flex items-center space-x-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-colors"
            >
              {showCode ? (
                <>
                  <EyeOff className="w-4 h-4" />
                  <span>Ocultar Código</span>
                </>
              ) : (
                <>
                  <Eye className="w-4 h-4" />
                  <span>Ver Código</span>
                </>
              )}
            </button>
          )}
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
            {(metricas_codigo?.indice_predictibilidad * 100)?.toFixed(1) ||
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
            {resaltado_ia?.lineas_sospechosas?.length || 0}
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
                {metricas_codigo?.variabilidad_funciones?.toFixed(2) ||
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
      {resaltado_ia?.lineas_sospechosas &&
        resaltado_ia.lineas_sospechosas.length > 0 && (
          <div className="bg-slate-800/50 border border-orange-500/50 rounded-xl p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Code2 className="w-6 h-6 text-orange-400" />
              <h3 className="text-lg font-bold text-slate-100">
                Líneas Sospechosas Detectadas
              </h3>
            </div>

            <div className="space-y-2">
              <div className="bg-slate-900/50 border border-orange-500/30 rounded-lg p-4">
                <p className="text-sm text-slate-400 mb-2">Números de línea detectadas:</p>
                <div className="flex flex-wrap gap-2">
                  {resaltado_ia.lineas_sospechosas.slice(0, 20).map((numeroLinea, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-orange-500/20 text-orange-300 rounded-lg text-sm font-mono"
                    >
                      {numeroLinea}
                    </span>
                  ))}
                  {resaltado_ia.lineas_sospechosas.length > 20 && (
                    <span className="px-3 py-1 text-slate-400 text-sm">
                      +{resaltado_ia.lineas_sospechosas.length - 20} más
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

      {/* Bloques Sospechosos */}
      {resaltado_ia?.bloques &&
        resaltado_ia.bloques.length > 0 && (
          <div className="bg-slate-800/50 border border-purple-500/50 rounded-xl p-6">
            <div className="flex items-center space-x-3 mb-4">
              <FileCode className="w-6 h-6 text-purple-400" />
              <h3 className="text-lg font-bold text-slate-100">
                Bloques Sospechosos
              </h3>
            </div>

            <div className="space-y-3 max-h-96 overflow-y-auto">
              {resaltado_ia.bloques.map((bloque, idx) => (
                <div
                  key={idx}
                  className="bg-slate-900/50 border border-purple-500/30 rounded-lg p-3"
                >
                  <p className="text-sm text-slate-400 mb-1">
                    Bloque {idx + 1}: Líneas {bloque.inicio} - {bloque.fin}
                  </p>
                  <p className="text-xs text-purple-400">
                    Tamaño: {bloque.fin - bloque.inicio + 1} líneas
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

      {/* Código con Líneas Marcadas */}
      {showCode && codigo_original && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl overflow-hidden">
          <div className="flex items-center justify-between p-4 bg-slate-800/70 border-b border-slate-700/50">
            <div className="flex items-center space-x-3">
              <Code2 className="w-6 h-6 text-cyan-400" />
              <h3 className="text-lg font-bold text-slate-100">
                Código con Líneas Sospechosas Marcadas
              </h3>
            </div>
            <button
              onClick={() => setShowCode(false)}
              className="text-slate-400 hover:text-slate-200 transition-colors"
            >
              <EyeOff className="w-5 h-5" />
            </button>
          </div>
          {renderCodeWithMarkedLines()}
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;
