// filepath: frontend/src/components/ui/Button.jsx
import React from 'react';

export const Button = ({ 
  children,
  type = 'button',
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  className = '',
  ...props
}) => {
  const baseClasses = `
    inline-flex items-center justify-center
    font-medium rounded-lg
    transition-all duration-300
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    relative overflow-hidden
    group
  `;

  const variants = {
    primary: `
      bg-cyber-button
      hover:shadow-cyber-glow-lg
      hover:-translate-y-1
      text-cyber-text-primary
      focus:ring-cyber-accent-secondary
      shadow-cyber-glow
      border-0
    `,
    secondary: `
      bg-cyber-bg-secondary 
      hover:bg-cyber-bg-primary 
      text-cyber-text-accent 
      border border-cyber-border-primary/30
      focus:ring-cyber-accent-secondary
    `,
    danger: `
      bg-gradient-to-r from-cyber-error to-red-500
      hover:from-cyber-error/80 hover:to-red-400
      text-cyber-text-primary
      focus:ring-cyber-error
      shadow-cyber-glow
    `,
    success: `
      bg-gradient-to-r from-cyber-success to-emerald-500
      hover:from-cyber-success/80 hover:to-emerald-400
      text-cyber-text-primary
      focus:ring-cyber-success
      shadow-cyber-glow-green
    `,
    ghost: `
      bg-transparent
      hover:bg-cyber-accent-secondary/10
      text-cyber-text-accent
      border border-cyber-border-primary/30
      focus:ring-cyber-accent-secondary
    `
  };

  const sizes = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };

  return (
    <button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={`
        ${baseClasses}
        ${variants[variant]}
        ${sizes[size]}
        ${className}
      `}
      {...props}
    >
      {loading && (
        <svg 
          className="animate-spin -ml-1 mr-3 h-5 w-5 text-cyber-text-primary" 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24"
        >
          <circle 
            className="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4"
          />
          <path 
            className="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      
      {children}
      
      {/* Efecto cyberpunk hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-cyber-accent-highlight/10 to-transparent transform -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
    </button>
  );
};

export default Button;