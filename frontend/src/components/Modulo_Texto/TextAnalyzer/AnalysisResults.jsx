import React from 'react';

const AnalysisResults = ({ result, modelName = "Modelo" }) => {
  if (!result || !result.success) {
    return (
      <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-4">
        <div className="text-cyber-error">
          ❌ Error: {result?.error || 'Error desconocido'}
        </div>
      </div>
    );
  }

  const { data } = result;
  const isAI = data.prediccion === 'IA';
  const confidence = data.probabilidad_ia || 0;

  return (
    <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-6">
      <h3 className="text-lg font-bold text-white mb-4 flex items-center">
        📊 Resultado del Análisis - {modelName}
      </h3>
      
      {/* Predicción Principal */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-cyber-text-secondary">Predicción:</span>
          <div className="flex items-center">
            <span className={`font-bold text-lg ${
              isAI ? 'text-cyber-error' : 'text-cyber-success'
            }`}>
              {isAI ? '🤖 Generado por IA' : '👤 Escrito por Humano'}
            </span>
          </div>
        </div>
        
        {/* Barra de Confianza */}
        <div className="bg-cyber-bg-secondary/50 rounded-lg p-4">
          <div className="flex justify-between mb-2">
            <span className="text-sm text-cyber-text-secondary">Confianza IA:</span>
            <span className={`text-sm font-bold ${
              confidence > 70 ? 'text-cyber-error' : 
              confidence > 30 ? 'text-yellow-400' : 
              'text-cyber-success'
            }`}>
              {Math.round(confidence)}%
            </span>
          </div>
          
          <div className="relative">
            <div className="w-full bg-cyber-bg-primary rounded-full h-3">
              <div 
                className={`h-3 rounded-full transition-all duration-1000 ease-out ${
                  confidence > 70 ? 'bg-gradient-to-r from-cyber-error to-red-400' :
                  confidence > 30 ? 'bg-gradient-to-r from-yellow-400 to-cyber-accent-primary' :
                  'bg-gradient-to-r from-cyber-success to-green-400'
                }`}
                style={{ width: `${Math.min(confidence, 100)}%` }}
              ></div>
            </div>
            
            {/* Marcadores de referencia */}
            <div className="flex justify-between text-xs text-cyber-text-muted mt-1">
              <span>0%</span>
              <span>50%</span>
              <span>100%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Detalles Adicionales */}
      {data.probabilidad_humano && (
        <div className="border-t border-cyber-border-secondary/30 pt-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-cyber-error">
                {Math.round(data.probabilidad_ia)}%
              </div>
              <div className="text-xs text-cyber-text-muted">Probabilidad IA</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-cyber-success">
                {Math.round(data.probabilidad_humano)}%
              </div>
              <div className="text-xs text-cyber-text-muted">Probabilidad Humano</div>
            </div>
          </div>
        </div>
      )}

      {/* Timestamp */}
      <div className="text-xs text-cyber-text-muted text-center pt-3 border-t border-cyber-border-secondary/30 mt-4">
        Análisis completado el {new Date().toLocaleString()}
      </div>
    </div>
  );
};

export default AnalysisResults;