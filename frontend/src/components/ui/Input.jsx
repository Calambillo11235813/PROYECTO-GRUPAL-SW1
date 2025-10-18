import React from 'react';

const Input = ({ 
  type = 'text',
  label,
  name,
  value,
  onChange,
  placeholder,
  error,
  required = false,
  className = '',
  ...props
}) => {
  return (
    <div className="mb-4">
      {label && (
        <label 
          htmlFor={name}
          className="block text-sm font-medium text-cyber-text-accent mb-2"
        >
          {label} {required && <span className="text-cyber-error">*</span>}
        </label>
      )}
      
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={`
          w-full px-4 py-3 
          bg-cyber-bg-secondary/50 
          border border-cyber-border-primary/30 
          rounded-lg 
          text-cyber-text-primary 
          placeholder-cyber-text-muted
          focus:outline-none 
          focus:border-cyber-text-accent 
          focus:ring-2 
          focus:ring-cyber-accent-secondary/20
          transition-all duration-300
          ${error ? 'border-cyber-error focus:border-cyber-error focus:ring-cyber-error/20' : ''}
          ${className}
        `}
        {...props}
      />
      
      {error && (
        <p className="mt-1 text-sm text-cyber-error flex items-center">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}
    </div>
  );
};

export default Input;