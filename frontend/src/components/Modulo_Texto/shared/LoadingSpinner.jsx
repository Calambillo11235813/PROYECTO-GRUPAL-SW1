import React from 'react';
import PropTypes from 'prop-types';

/**
 * Componente de spinner de carga con estilo cyberpunk
 * @param {Object} props - Propiedades del componente
 * @param {string} props.size - Tamaño del spinner ('sm', 'md', 'lg')
 * @param {string} props.color - Color del spinner ('primary', 'secondary', 'success')
 * @param {string} props.text - Texto opcional para mostrar junto al spinner
 * @param {boolean} props.fullScreen - Si debe ocupar toda la pantalla como overlay
 */
const LoadingSpinner = ({ size, color, text, fullScreen }) => {
  // Mapeo de tamaños a clases
  const sizeClasses = {
    sm: 'w-5 h-5 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4'
  };
  
  // Mapeo de colores a clases (siguiendo la paleta del README)
  const colorClasses = {
    primary: 'border-t-cyan-500 border-r-cyan-500/40 border-b-cyan-500/10 border-l-cyan-500/30',
    secondary: 'border-t-purple-500 border-r-purple-500/40 border-b-purple-500/10 border-l-purple-500/30',
    success: 'border-t-green-500 border-r-green-500/40 border-b-green-500/10 border-l-green-500/30',
    warning: 'border-t-yellow-300 border-r-yellow-300/40 border-b-yellow-300/10 border-l-yellow-300/30',
    danger: 'border-t-orange-500 border-r-orange-500/40 border-b-orange-500/10 border-l-orange-500/30'
  };
  
  // Sombras de neón según el color
  const glowEffects = {
    primary: 'shadow-[0_0_15px_rgba(6,182,212,0.7)]',
    secondary: 'shadow-[0_0_15px_rgba(168,85,247,0.7)]',
    success: 'shadow-[0_0_15px_rgba(34,197,94,0.7)]',
    warning: 'shadow-[0_0_15px_rgba(253,224,71,0.7)]',
    danger: 'shadow-[0_0_15px_rgba(249,115,22,0.7)]'
  };
  
  // Seleccionar clases según props
  const spinnerSize = sizeClasses[size] || sizeClasses.md;
  const spinnerColor = colorClasses[color] || colorClasses.primary;
  const glowEffect = glowEffects[color] || glowEffects.primary;
  
  // Contenedor del spinner
  const spinnerElement = (
    <div className="flex flex-col items-center justify-center">
      <div 
        className={`rounded-full border-solid animate-spin ${spinnerSize} ${spinnerColor} ${glowEffect}`}
        role="status"
        aria-label="Cargando"
      />
      {text && (
        <p className="mt-3 text-sm font-medium text-slate-300 animate-pulse">
          {text}
        </p>
      )}
    </div>
  );
  
  // Si es fullScreen, mostrar como overlay
  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50 flex items-center justify-center">
        {spinnerElement}
      </div>
    );
  }
  
  return spinnerElement;
};

LoadingSpinner.propTypes = {
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  color: PropTypes.oneOf(['primary', 'secondary', 'success', 'warning', 'danger']),
  text: PropTypes.string,
  fullScreen: PropTypes.bool
};

LoadingSpinner.defaultProps = {
  size: 'md',
  color: 'primary',
  text: '',
  fullScreen: false
};

export default LoadingSpinner;