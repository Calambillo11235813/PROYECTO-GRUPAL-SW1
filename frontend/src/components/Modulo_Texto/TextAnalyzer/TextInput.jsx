import React from 'react';

const TextInput = ({ 
  value, 
  onChange, 
  placeholder = "Ingresa tu texto aquí...", 
  disabled = false,
  maxLength = 10000 
}) => {
  const characterCount = value.length;
  const isNearLimit = characterCount > maxLength * 0.8;
  const isOverLimit = characterCount > maxLength;

  return (
    <div>
      <label className="block text-sm font-medium text-cyber-text-accent mb-2">
        Texto a Analizar
        <span className={`text-xs ml-2 ${
          isOverLimit ? 'text-cyber-error' : 
          isNearLimit ? 'text-yellow-400' : 
          'text-cyber-text-muted'
        }`}>
          ({characterCount.toLocaleString()}/{maxLength.toLocaleString()} caracteres)
        </span>
      </label>
      
      <div className="relative">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          disabled={disabled}
          rows={8}
          maxLength={maxLength}
          className={`
            w-full px-4 py-3 
            bg-cyber-bg-secondary 
            border rounded-lg 
            text-white 
            placeholder-cyber-text-muted
            focus:outline-none 
            focus:ring-2 
            transition-all duration-300
            resize-none
            ${isOverLimit 
              ? 'border-cyber-error focus:border-cyber-error focus:ring-cyber-error/20' 
              : 'border-cyber-border-primary/40 focus:border-cyber-text-accent focus:ring-cyber-accent-secondary/30'
            }
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        />
        
        {/* Character limit warning */}
        {isNearLimit && (
          <div className="absolute bottom-2 right-2">
            <div className={`text-xs px-2 py-1 rounded ${
              isOverLimit 
                ? 'bg-cyber-error/20 text-cyber-error' 
                : 'bg-yellow-400/20 text-yellow-400'
            }`}>
              {isOverLimit ? 'Límite excedido' : 'Cerca del límite'}
            </div>
          </div>
        )}
      </div>
      
      {/* Help text */}
      <div className="mt-2 text-xs text-cyber-text-muted">
        💡 Tip: Textos más largos proporcionan análisis más precisos
      </div>
    </div>
  );
};

export default TextInput;