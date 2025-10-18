import React from 'react';

const ComparisonChart = ({ 
  modelBResult, 
  modelNResult, 
  showDetails = true 
}) => {
  if (!modelBResult || !modelNResult) {
    return (
      <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-6">
        <div className="text-center text-cyber-text-muted">
          <svg className="mx-auto h-12 w-12 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p>No hay datos para mostrar el gráfico</p>
        </div>
      </div>
    );
  }

  // Extraer datos
  const modelB = {
    name: 'Modelo B',
    prediction: modelBResult.prediccion,
    aiProb: modelBResult.probabilidad_ia || 0,
    humanProb: modelBResult.probabilidad_humano || 0,
    color: 'cyan'
  };

  const modelN = {
    name: 'Modelo N',
    prediction: modelNResult.prediccion,
    aiProb: modelNResult.probabilidad_ia || 0,
    humanProb: modelNResult.probabilidad_humano || 0,
    color: 'purple'
  };

  // Determinar consenso
  const hasConsensus = modelB.prediction === modelN.prediction;
  const averageAI = (modelB.aiProb + modelN.aiProb) / 2;
  const averageHuman = (modelB.humanProb + modelN.humanProb) / 2;

  // Formatear porcentaje
  const formatPercentage = (value) => Math.round(value * 100) / 100;

  return (
    <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-6">
      
      {/* Header */}
      <div className="text-center mb-6">
        <h3 className="text-lg font-bold text-white mb-2">
          📊 Gráfico Comparativo de Modelos
        </h3>
        <p className="text-sm text-cyber-text-secondary">
          Análisis visual de las predicciones de ambos modelos
        </p>
      </div>

      {/* Consenso */}
      <div className={`
        mb-6 p-4 rounded-lg border text-center
        ${hasConsensus 
          ? 'bg-cyber-success/10 border-cyber-success/30' 
          : 'bg-yellow-400/10 border-yellow-400/30'
        }
      `}>
        <div className="flex items-center justify-center space-x-2 mb-2">
          <span className="text-xl">
            {hasConsensus ? '✅' : '⚠️'}
          </span>
          <span className={`font-bold ${
            hasConsensus ? 'text-cyber-success' : 'text-yellow-400'
          }`}>
            {hasConsensus ? 'CONSENSO' : 'DISCREPANCIA'}
          </span>
        </div>
        <p className={`text-sm ${
          hasConsensus ? 'text-cyber-success' : 'text-yellow-400'
        }`}>
          {hasConsensus 
            ? `Ambos modelos coinciden: ${modelB.prediction}` 
            : `Modelo B: ${modelB.prediction} vs Modelo N: ${modelN.prediction}`
          }
        </p>
      </div>

      {/* Gráfico de barras comparativo */}
      <div className="space-y-6">
        
        {/* Probabilidad IA */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <span className="text-lg">🤖</span>
              <span className="text-white font-medium">Probabilidad IA</span>
            </div>
            <span className="text-sm text-cyber-text-muted">
              Promedio: {formatPercentage(averageAI)}%
            </span>
          </div>
          
          <div className="space-y-3">
            {/* Modelo B */}
            <div className="flex items-center space-x-3">
              <div className="w-20 text-sm text-cyan-400 font-medium">
                Modelo B
              </div>
              <div className="flex-1 relative">
                <div className="w-full bg-cyber-bg-secondary rounded-full h-6 border border-cyber-border-secondary/30">
                  <div 
                    className="bg-gradient-to-r from-cyan-400 to-blue-400 h-6 rounded-full flex items-center justify-end pr-2 transition-all duration-1000 ease-out"
                    style={{ width: `${modelB.aiProb}%` }}
                  >
                    <span className="text-xs font-bold text-white">
                      {formatPercentage(modelB.aiProb)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Modelo N */}
            <div className="flex items-center space-x-3">
              <div className="w-20 text-sm text-purple-400 font-medium">
                Modelo N
              </div>
              <div className="flex-1 relative">
                <div className="w-full bg-cyber-bg-secondary rounded-full h-6 border border-cyber-border-secondary/30">
                  <div 
                    className="bg-gradient-to-r from-purple-400 to-pink-400 h-6 rounded-full flex items-center justify-end pr-2 transition-all duration-1000 ease-out"
                    style={{ width: `${modelN.aiProb}%` }}
                  >
                    <span className="text-xs font-bold text-white">
                      {formatPercentage(modelN.aiProb)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Probabilidad Humano */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <span className="text-lg">👤</span>
              <span className="text-white font-medium">Probabilidad Humano</span>
            </div>
            <span className="text-sm text-cyber-text-muted">
              Promedio: {formatPercentage(averageHuman)}%
            </span>
          </div>
          
          <div className="space-y-3">
            {/* Modelo B */}
            <div className="flex items-center space-x-3">
              <div className="w-20 text-sm text-cyan-400 font-medium">
                Modelo B
              </div>
              <div className="flex-1 relative">
                <div className="w-full bg-cyber-bg-secondary rounded-full h-6 border border-cyber-border-secondary/30">
                  <div 
                    className="bg-gradient-to-r from-green-400 to-emerald-400 h-6 rounded-full flex items-center justify-end pr-2 transition-all duration-1000 ease-out"
                    style={{ width: `${modelB.humanProb}%` }}
                  >
                    <span className="text-xs font-bold text-white">
                      {formatPercentage(modelB.humanProb)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Modelo N */}
            <div className="flex items-center space-x-3">
              <div className="w-20 text-sm text-purple-400 font-medium">
                Modelo N
              </div>
              <div className="flex-1 relative">
                <div className="w-full bg-cyber-bg-secondary rounded-full h-6 border border-cyber-border-secondary/30">
                  <div 
                    className="bg-gradient-to-r from-green-400 to-emerald-400 h-6 rounded-full flex items-center justify-end pr-2 transition-all duration-1000 ease-out"
                    style={{ width: `${modelN.humanProb}%` }}
                  >
                    <span className="text-xs font-bold text-white">
                      {formatPercentage(modelN.humanProb)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Estadísticas adicionales */}
      {showDetails && (
        <div className="mt-6 pt-4 border-t border-cyber-border-secondary/30">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            
            <div className="bg-cyber-bg-secondary/30 rounded-lg p-3">
              <div className="text-xs text-cyber-text-muted mb-1">Diferencia IA</div>
              <div className={`text-sm font-bold ${
                Math.abs(modelB.aiProb - modelN.aiProb) > 20 ? 'text-yellow-400' : 'text-cyber-success'
              }`}>
                {formatPercentage(Math.abs(modelB.aiProb - modelN.aiProb))}%
              </div>
            </div>

            <div className="bg-cyber-bg-secondary/30 rounded-lg p-3">
              <div className="text-xs text-cyber-text-muted mb-1">Diferencia Humano</div>
              <div className={`text-sm font-bold ${
                Math.abs(modelB.humanProb - modelN.humanProb) > 20 ? 'text-yellow-400' : 'text-cyber-success'
              }`}>
                {formatPercentage(Math.abs(modelB.humanProb - modelN.humanProb))}%
              </div>
            </div>

            <div className="bg-cyber-bg-secondary/30 rounded-lg p-3">
              <div className="text-xs text-cyber-text-muted mb-1">Confianza B</div>
              <div className="text-sm font-bold text-cyan-400">
                {formatPercentage(Math.max(modelB.aiProb, modelB.humanProb))}%
              </div>
            </div>

            <div className="bg-cyber-bg-secondary/30 rounded-lg p-3">
              <div className="text-xs text-cyber-text-muted mb-1">Confianza N</div>
              <div className="text-sm font-bold text-purple-400">
                {formatPercentage(Math.max(modelN.aiProb, modelN.humanProb))}%
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Interpretación */}
      <div className="mt-4 p-3 bg-cyber-bg-secondary/20 rounded-lg border border-cyber-border-secondary/30">
        <div className="text-xs text-cyber-text-accent font-medium mb-1">💡 Interpretación:</div>
        <div className="text-xs text-cyber-text-muted">
          {hasConsensus ? (
            `Ambos modelos están de acuerdo en que el texto fue ${modelB.prediction.toLowerCase() === 'ia' ? 'generado por IA' : 'escrito por un humano'}.`
          ) : (
            `Los modelos no están de acuerdo. El Modelo B sugiere ${modelB.prediction}, mientras que el Modelo N sugiere ${modelN.prediction}. Se recomienda revisión manual.`
          )}
        </div>
      </div>
    </div>
  );
};

export default ComparisonChart;