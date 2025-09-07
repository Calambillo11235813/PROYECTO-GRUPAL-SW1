import React from 'react';

const ModelCard = ({ 
  modelName, 
  modelDescription, 
  result, 
  color = 'cyan',
  isHighlighted = false 
}) => {
  if (!result) {
    return (
      <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-6">
        <div className="text-center text-cyber-text-muted">
          <div className="w-16 h-16 mx-auto mb-3 bg-cyber-bg-secondary/30 rounded-full flex items-center justify-center">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <p className="text-sm">Sin resultado</p>
        </div>
      </div>
    );
  }

  const prediction = result.prediccion || result.prediction;
  const aiProbability = result.probabilidad_ia || result.ai_probability || 0;
  const humanProbability = result.probabilidad_humano || result.human_probability || 0;
  
  const isAI = prediction === 'IA' || prediction === 'AI';
  
  // Colores según el tema
  const colorClasses = {
    cyan: {
      bg: 'bg-cyan-400/10',
      border: 'border-cyan-400/30',
      text: 'text-cyan-400',
      gradient: 'from-cyan-400 to-blue-400',
      glow: 'shadow-cyan-400/20'
    },
    purple: {
      bg: 'bg-purple-400/10',
      border: 'border-purple-400/30',
      text: 'text-purple-400',
      gradient: 'from-purple-400 to-pink-400',
      glow: 'shadow-purple-400/20'
    },
    green: {
      bg: 'bg-green-400/10',
      border: 'border-green-400/30',
      text: 'text-green-400',
      gradient: 'from-green-400 to-emerald-400',
      glow: 'shadow-green-400/20'
    },
    orange: {
      bg: 'bg-orange-400/10',
      border: 'border-orange-400/30',
      text: 'text-orange-400',
      gradient: 'from-orange-400 to-red-400',
      glow: 'shadow-orange-400/20'
    }
  };

  const colorClass = colorClasses[color] || colorClasses.cyan;

  // Formatear porcentaje
  const formatPercentage = (value) => {
    return Math.round(value * 100) / 100;
  };

  // Obtener nivel de confianza
  const getConfidenceLevel = (probability) => {
    if (probability > 80) return { level: 'Alta', color: 'text-green-400' };
    if (probability > 60) return { level: 'Media', color: 'text-yellow-400' };
    if (probability > 40) return { level: 'Baja', color: 'text-orange-400' };
    return { level: 'Muy Baja', color: 'text-red-400' };
  };

  const confidence = getConfidenceLevel(Math.max(aiProbability, humanProbability));

  return (
    <div className={`
      bg-cyber-bg-card border rounded-lg p-6 transition-all duration-300
      ${isHighlighted 
        ? `${colorClass.border} shadow-lg ${colorClass.glow}` 
        : 'border-cyber-border-primary/30 hover:border-cyber-border-primary/50'
      }
    `}>
      
      {/* Header del modelo */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <div className={`
            w-3 h-3 rounded-full animate-pulse
            ${isAI ? 'bg-cyber-error' : 'bg-cyber-success'}
          `}></div>
          <div className={`text-xs font-medium px-2 py-1 rounded ${colorClass.bg} ${colorClass.text}`}>
            {modelName}
          </div>
        </div>
        
        <h3 className={`text-lg font-bold ${colorClass.text} mb-1`}>
          {modelName}
        </h3>
        
        <p className="text-sm text-cyber-text-muted">
          {modelDescription}
        </p>
      </div>

      {/* Predicción principal */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-cyber-text-secondary text-sm">Predicción:</span>
          <div className="flex items-center space-x-2">
            <span className="text-xl">
              {isAI ? '🤖' : '👤'}
            </span>
            <span className={`font-bold ${
              isAI ? 'text-cyber-error' : 'text-cyber-success'
            }`}>
              {isAI ? 'IA' : 'Humano'}
            </span>
          </div>
        </div>

        {/* Barra de confianza principal */}
        <div className={`${colorClass.bg} rounded-lg p-3 border ${colorClass.border}`}>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-cyber-text-secondary">Confianza:</span>
            <span className={`text-sm font-medium ${confidence.color}`}>
              {confidence.level}
            </span>
          </div>
          
          <div className="relative">
            <div className="w-full bg-cyber-bg-primary rounded-full h-2">
              <div 
                className={`h-2 rounded-full transition-all duration-1000 ease-out bg-gradient-to-r ${
                  isAI ? 'from-cyber-error to-red-400' : 'from-cyber-success to-green-400'
                }`}
                style={{ width: `${Math.max(aiProbability, humanProbability)}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Probabilidades detalladas */}
      <div className="space-y-3">
        <div className="text-center text-xs text-cyber-text-accent font-medium mb-2">
          Distribución de Probabilidades
        </div>
        
        {/* Probabilidad IA */}
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <span className="text-lg">🤖</span>
            <span className="text-sm text-cyber-text-secondary">IA:</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-16 bg-cyber-bg-primary rounded-full h-1.5">
              <div 
                className="bg-gradient-to-r from-cyber-error to-red-400 h-1.5 rounded-full transition-all duration-500"
                style={{ width: `${aiProbability}%` }}
              ></div>
            </div>
            <span className={`text-sm font-medium min-w-[3rem] text-right ${
              isAI ? 'text-cyber-error font-bold' : 'text-cyber-text-secondary'
            }`}>
              {formatPercentage(aiProbability)}%
            </span>
          </div>
        </div>

        {/* Probabilidad Humano */}
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <span className="text-lg">👤</span>
            <span className="text-sm text-cyber-text-secondary">Humano:</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-16 bg-cyber-bg-primary rounded-full h-1.5">
              <div 
                className="bg-gradient-to-r from-cyber-success to-green-400 h-1.5 rounded-full transition-all duration-500"
                style={{ width: `${humanProbability}%` }}
              ></div>
            </div>
            <span className={`text-sm font-medium min-w-[3rem] text-right ${
              !isAI ? 'text-cyber-success font-bold' : 'text-cyber-text-secondary'
            }`}>
              {formatPercentage(humanProbability)}%
            </span>
          </div>
        </div>
      </div>

      {/* Metadata del resultado */}
      {result.modelo && (
        <div className="mt-4 pt-3 border-t border-cyber-border-secondary/30">
          <div className="text-xs text-cyber-text-muted text-center">
            Modelo: {result.modelo} • Procesado: {new Date().toLocaleTimeString()}
          </div>
        </div>
      )}
    </div>
  );
};

export default ModelCard;