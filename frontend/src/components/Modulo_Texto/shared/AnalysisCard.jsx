import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * Tarjeta para mostrar resultados de análisis con estilo cyberpunk
 * @param {Object} props - Propiedades del componente
 * @param {string} props.title - Título de la tarjeta
 * @param {number} props.score - Puntuación (0-100)
 * @param {string} props.conclusion - Conclusión del análisis
 * @param {string} props.model - Nombre del modelo (opcional)
 * @param {Object} props.details - Detalles adicionales (opcional)
 * @param {string} props.type - Tipo de resultado ('ai', 'human', 'uncertain')
 */
const AnalysisCard = ({ title, score, conclusion, model, details, type }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Configuración según el tipo de resultado
  const typeConfigs = {
    ai: {
      gradient: 'from-purple-900/50 to-cyan-900/50',
      borderColor: 'border-cyan-500',
      textColor: 'text-cyan-400',
      icon: '🤖',
      glowEffect: 'shadow-[0_0_15px_rgba(6,182,212,0.4)]'
    },
    human: {
      gradient: 'from-green-900/50 to-emerald-900/50',
      borderColor: 'border-green-500',
      textColor: 'text-green-400',
      icon: '👤',
      glowEffect: 'shadow-[0_0_15px_rgba(34,197,94,0.4)]'
    },
    uncertain: {
      gradient: 'from-yellow-900/50 to-orange-900/50',
      borderColor: 'border-yellow-300',
      textColor: 'text-yellow-300',
      icon: '❓',
      glowEffect: 'shadow-[0_0_15px_rgba(253,224,71,0.4)]'
    }
  };
  
  const config = typeConfigs[type] || typeConfigs.uncertain;
  
  // Determinar el color del score basado en el valor
  const getScoreColor = () => {
    const isAIScore = type === 'ai';
    
    // Para AI, un score alto es rojo, para humano, un score alto es verde
    if (isAIScore) {
      if (score >= 75) return 'text-cyan-400';
      if (score >= 50) return 'text-cyan-300';
      return 'text-slate-300';
    } else {
      if (score >= 75) return 'text-green-400';
      if (score >= 50) return 'text-green-300';
      return 'text-slate-300';
    }
  };
  
  return (
    <div 
      className={`bg-gradient-to-br ${config.gradient} border ${config.borderColor} rounded-lg p-4 ${config.glowEffect} backdrop-blur-sm transition-all duration-300 hover:scale-[1.01]`}
    >
      {/* Encabezado */}
      <div className="flex items-center justify-between mb-3">
        <h3 className={`font-bold text-lg ${config.textColor} flex items-center`}>
          <span className="mr-2">{config.icon}</span>
          {title}
        </h3>
        
        {model && (
          <div className="bg-slate-800/60 px-2 py-1 rounded text-xs text-slate-300 border border-slate-700">
            Modelo: {model}
          </div>
        )}
      </div>
      
      {/* Score */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-1">
          <span className="text-sm text-slate-400">Probabilidad</span>
          <span className={`font-mono font-bold ${getScoreColor()}`}>
            {score}%
          </span>
        </div>
        
        {/* Barra de progreso */}
        <div className="h-2 bg-slate-800/60 rounded-full overflow-hidden">
          <div 
            className={`h-full ${type === 'ai' ? 'bg-cyan-500' : type === 'human' ? 'bg-green-500' : 'bg-yellow-300'}`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>
      
      {/* Conclusión */}
      <div className="text-slate-200 font-medium mb-3">
        {conclusion}
      </div>
      
      {/* Detalles expandibles */}
      {details && Object.keys(details).length > 0 && (
        <div className="mt-3 border-t border-slate-700/50 pt-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className={`text-xs ${config.textColor} hover:underline flex items-center`}
          >
            <span>{isExpanded ? '▼' : '►'}</span>
            <span className="ml-1">
              {isExpanded ? 'Ocultar detalles' : 'Mostrar detalles'}
            </span>
          </button>
          
          {isExpanded && (
            <div className="mt-2 text-sm grid gap-2">
              {Object.entries(details).map(([key, value]) => (
                <div key={key} className="grid grid-cols-3 gap-2">
                  <span className="text-slate-400">{key}:</span>
                  <span className="text-slate-200 col-span-2">{value}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      
      {/* Efecto línea de escaneo */}
      <div className="absolute inset-x-0 top-0 h-0.5 bg-gradient-to-r from-transparent via-cyan-400 to-transparent opacity-70 animate-scan"></div>
    </div>
  );
};

AnalysisCard.propTypes = {
  title: PropTypes.string.isRequired,
  score: PropTypes.number.isRequired,
  conclusion: PropTypes.string.isRequired,
  model: PropTypes.string,
  details: PropTypes.object,
  type: PropTypes.oneOf(['ai', 'human', 'uncertain'])
};

AnalysisCard.defaultProps = {
  model: '',
  details: {},
  type: 'uncertain'
};

export default AnalysisCard;