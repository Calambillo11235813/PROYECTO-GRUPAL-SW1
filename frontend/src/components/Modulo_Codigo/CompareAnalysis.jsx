import React, { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import {
  GitCompare,
  ArrowLeft,
  Code2,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  X,
} from "lucide-react";
import codeAnalysisService from "../../services/codeAnalysisService";

const CompareAnalysis = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadComparison = async (ids) => {
      setLoading(true);
      try {
        const data = await codeAnalysisService.compareAnalysis(ids);
        setComparisonData(data);
      } catch (error) {
        console.error("Error al comparar:", error);
      } finally {
        setLoading(false);
      }
    };

    const ids = searchParams.get("ids");
    if (ids) {
      const idArray = ids.split(",").map((id) => parseInt(id));
      loadComparison(idArray);
    }
  }, [searchParams]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  if (!comparisonData || !comparisonData.comparaciones) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-400">No se pudo realizar la comparación</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center space-x-2 text-slate-400 hover:text-cyan-400 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Volver</span>
          </button>

          <div className="flex items-center space-x-3">
            <GitCompare className="w-8 h-8 text-purple-400" />
            <div>
              <h2 className="text-2xl font-bold text-slate-100">
                Comparación de Análisis
              </h2>
              <p className="text-sm text-slate-400">
                {comparisonData.comparaciones.length} análisis comparados
              </p>
            </div>
          </div>
        </div>

        {/* Comparison Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {comparisonData.comparaciones.map((item) => (
            <div
              key={item.id}
              className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 hover:border-cyan-500/50 transition-all"
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div
                    className={`
                    p-2 rounded-lg
                    ${item.ia_es_generado ? "bg-red-500/20" : "bg-green-500/20"}
                  `}
                  >
                    <Code2
                      className={`w-5 h-5 ${
                        item.ia_es_generado ? "text-red-400" : "text-green-400"
                      }`}
                    />
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-100">
                      {item.nombre_archivo}
                    </h3>
                    <p className="text-xs text-slate-400">{item.lenguaje}</p>
                  </div>
                </div>
                <span
                  className={`
                  px-3 py-1 rounded-full text-xs font-bold
                  ${
                    item.ia_es_generado
                      ? "bg-red-500/20 text-red-300"
                      : "bg-green-500/20 text-green-300"
                  }
                `}
                >
                  {item.ia_es_generado ? "IA" : "Humano"}
                </span>
              </div>

              {/* Métricas */}
              <div className="space-y-3">
                {/* Confianza */}
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-slate-400">Confianza</span>
                    <span className="text-sm font-bold text-cyan-400">
                      {(item.ia_confianza * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div
                      className={`h-full rounded-full ${
                        item.ia_es_generado
                          ? "bg-gradient-to-r from-red-500 to-orange-500"
                          : "bg-gradient-to-r from-green-500 to-cyan-500"
                      }`}
                      style={{ width: `${item.ia_confianza * 100}%` }}
                    />
                  </div>
                </div>

                {/* Complejidad */}
                <div className="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg">
                  <span className="text-sm text-slate-400">
                    Complejidad Ciclomática
                  </span>
                  <span className="text-sm font-bold text-purple-400">
                    {item.complejidad_ciclomatica?.toFixed(2) || "N/A"}
                  </span>
                </div>

                {/* Predictibilidad */}
                <div className="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg">
                  <span className="text-sm text-slate-400">
                    Predictibilidad
                  </span>
                  <span className="text-sm font-bold text-orange-400">
                    {(item.indice_predictibilidad * 100)?.toFixed(1) || "N/A"}%
                  </span>
                </div>

                {/* Líneas Sospechosas */}
                <div className="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg">
                  <span className="text-sm text-slate-400">
                    Líneas Sospechosas
                  </span>
                  <span className="text-sm font-bold text-red-400">
                    {item.lineas_sospechosas?.length || 0}
                  </span>
                </div>

                {/* Fecha */}
                <div className="pt-3 border-t border-slate-700/50">
                  <p className="text-xs text-slate-500">
                    Analizado: {new Date(item.fecha_analisis).toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Resumen de Diferencias */}
        {comparisonData.diferencias && (
          <div className="bg-slate-800/50 border border-purple-500/50 rounded-xl p-6">
            <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center space-x-2">
              <TrendingUp className="w-6 h-6 text-purple-400" />
              <span>Resumen de Diferencias</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-900/50 rounded-lg p-4">
                <p className="text-sm text-slate-400 mb-1">
                  Diferencia de Confianza
                </p>
                <p className="text-2xl font-bold text-cyan-400">
                  {comparisonData.diferencias.confianza?.toFixed(1)}%
                </p>
              </div>

              <div className="bg-slate-900/50 rounded-lg p-4">
                <p className="text-sm text-slate-400 mb-1">
                  Diferencia de Complejidad
                </p>
                <p className="text-2xl font-bold text-purple-400">
                  {comparisonData.diferencias.complejidad?.toFixed(2)}
                </p>
              </div>

              <div className="bg-slate-900/50 rounded-lg p-4">
                <p className="text-sm text-slate-400 mb-1">
                  Diferencia de Predictibilidad
                </p>
                <p className="text-2xl font-bold text-orange-400">
                  {comparisonData.diferencias.predictibilidad?.toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Recomendaciones */}
        <div className="bg-cyan-500/10 border border-cyan-500/50 rounded-xl p-6">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-6 h-6 text-cyan-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-bold text-cyan-400 mb-2">
                Recomendaciones
              </h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li>
                  • Revise manualmente los fragmentos con alta confianza de IA
                </li>
                <li>• Compare patrones sintácticos entre archivos similares</li>
                <li>
                  • Considere el contexto del proyecto al interpretar resultados
                </li>
                <li>
                  • Las diferencias significativas pueden indicar estilos
                  distintos
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompareAnalysis;
