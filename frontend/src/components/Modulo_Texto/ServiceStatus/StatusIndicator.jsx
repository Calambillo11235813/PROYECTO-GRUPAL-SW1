import React from 'react';
import PropTypes from 'prop-types';

/**
 * Componente que muestra un indicador visual del estado del servicio
 * @param {Object} props - Propiedades del componente
 * @param {string} props.status - Estado del servicio ('online', 'offline', 'degraded', 'loading')
 * @param {string} props.message - Mensaje descriptivo opcional
 * @param {number} props.latency - Tiempo de respuesta en ms (opcional)
 */
const StatusIndicator = ({ status, message, latency }) => {
  // Mapeo de estados a colores y clases
  const statusConfig = {
    online: {
      bgColor: 'bg-green-500',
      textColor: 'text-green-900',
      ringColor: 'ring-green-400',
      pulseEffect: true,
      icon: '✓',
      label: 'En línea'
    },
    offline: {
      bgColor: 'bg-red-500',
      textColor: 'text-red-900',
      ringColor: 'ring-red-400',
      pulseEffect: false,
      icon: '✕',
      label: 'Fuera de línea'
    },
    degraded: {
      bgColor: 'bg-yellow-400',
      textColor: 'text-yellow-900',
      ringColor: 'ring-yellow-300',
      pulseEffect: true,
      icon: '⚠',
      label: 'Rendimiento degradado'
    },
    loading: {
      bgColor: 'bg-blue-400',
      textColor: 'text-blue-900',
      ringColor: 'ring-blue-300',
      pulseEffect: true,
      icon: '⟳',
      label: 'Verificando...'
    }
  };

  const config = statusConfig[status] || statusConfig.loading;

  return (
    <div className="flex items-center space-x-2">
      {/* Indicador de estado */}
      <div className={`relative ${config.pulseEffect ? 'animate-pulse' : ''}`}>
        <div className={`h-3 w-3 rounded-full ${config.bgColor} ring-2 ${config.ringColor}`}></div>
      </div>
      
      {/* Texto de estado */}
      <div className="flex flex-col">
        <span className={`font-medium ${config.textColor}`}>
          {config.icon} {config.label}
        </span>
        
        {message && (
          <span className="text-xs text-slate-600">{message}</span>
        )}
        
        {latency !== undefined && (
          <span className="text-xs font-mono">
            Latencia: {latency < 100 ? (
              <span className="text-green-600">{latency}ms</span>
            ) : latency < 300 ? (
              <span className="text-yellow-600">{latency}ms</span>
            ) : (
              <span className="text-red-600">{latency}ms</span>
            )}
          </span>
        )}
      </div>
    </div>
  );
};

StatusIndicator.propTypes = {
  status: PropTypes.oneOf(['online', 'offline', 'degraded', 'loading']).isRequired,
  message: PropTypes.string,
  latency: PropTypes.number
};

StatusIndicator.defaultProps = {
  message: '',
  latency: undefined
};

export default StatusIndicator;