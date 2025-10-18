import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * Componente para mostrar mensajes de error con estilo cyberpunk
 * @param {Object} props - Propiedades del componente
 * @param {string} props.message - Mensaje de error
 * @param {string} props.type - Tipo de error ('error', 'warning', 'info')
 * @param {boolean} props.dismissible - Si el error puede ser descartado
 * @param {Function} props.onDismiss - Función a llamar cuando se descarta
 * @param {string} props.details - Detalles técnicos del error (opcional)
 */
const ErrorMessage = ({ message, type, dismissible, onDismiss, details }) => {
  const [isVisible, setIsVisible] = useState(true);
  const [showDetails, setShowDetails] = useState(false);
  
  // Si no es visible, no renderizar nada
  if (!isVisible) return null;
  
  // Configuración según el tipo de error
  const configs = {
    error: {
      bgColor: 'bg-gradient-to-r from-red-900/60 to-orange-900/60',
      borderColor: 'border-orange-500',
      iconColor: 'text-orange-500',
      glowEffect: 'shadow-[0_0_10px_rgba(249,115,22,0.5)]',
      icon: '✕'
    },
    warning: {
      bgColor: 'bg-gradient-to-r from-yellow-900/60 to-orange-900/60',
      borderColor: 'border-yellow-300',
      iconColor: 'text-yellow-300',
      glowEffect: 'shadow-[0_0_10px_rgba(253,224,71,0.5)]',
      icon: '⚠'
    },
    info: {
      bgColor: 'bg-gradient-to-r from-blue-900/60 to-cyan-900/60',
      borderColor: 'border-cyan-500',
      iconColor: 'text-cyan-500',
      glowEffect: 'shadow-[0_0_10px_rgba(6,182,212,0.5)]',
      icon: 'ℹ'
    }
  };
  
  const config = configs[type] || configs.error;
  
  // Manejar el cierre del mensaje
  const handleDismiss = () => {
    setIsVisible(false);
    if (onDismiss) {
      onDismiss();
    }
  };
  
  return (
    <div className={`relative rounded-md border ${config.borderColor} ${config.bgColor} ${config.glowEffect} p-4 my-3 backdrop-blur-sm`}>
      <div className="flex items-start">
        {/* Icono */}
        <div className={`mr-3 ${config.iconColor} text-xl flex-shrink-0`}>
          {config.icon}
        </div>
        
        {/* Contenido */}
        <div className="flex-1">
          <p className="text-slate-200 font-medium">{message}</p>
          
          {details && (
            <div className="mt-1">
              <button
                onClick={() => setShowDetails(!showDetails)}
                className="text-xs text-slate-400 hover:text-slate-300 transition-colors underline"
              >
                {showDetails ? 'Ocultar detalles' : 'Mostrar detalles'}
              </button>
              
              {showDetails && (
                <pre className="mt-2 p-2 bg-slate-900/80 rounded border border-slate-700 text-xs text-slate-300 overflow-x-auto">
                  {details}
                </pre>
              )}
            </div>
          )}
        </div>
        
        {/* Botón de cerrar */}
        {dismissible && (
          <button
            onClick={handleDismiss}
            className="ml-auto text-slate-400 hover:text-slate-200 transition-colors"
            aria-label="Cerrar mensaje"
          >
            <span className="text-lg">×</span>
          </button>
        )}
      </div>
      
      {/* Efecto de línea de escaneo cyberpunk */}
      <div className="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-transparent via-cyan-500 to-transparent animate-scan"></div>
    </div>
  );
};

ErrorMessage.propTypes = {
  message: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['error', 'warning', 'info']),
  dismissible: PropTypes.bool,
  onDismiss: PropTypes.func,
  details: PropTypes.string
};

ErrorMessage.defaultProps = {
  type: 'error',
  dismissible: true,
  onDismiss: null,
  details: ''
};

export default ErrorMessage;