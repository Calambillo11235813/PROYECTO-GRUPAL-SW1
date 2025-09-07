import React, { useState } from 'react';
import { useAuth } from '../../context/authContext';
import Input from '../ui/Input';
import Button from '../ui/Button';

const LoginForm = ({ onSuccess }) => {
  const { login, isLoading, error, clearError } = useAuth();
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  
  const [formErrors, setFormErrors] = useState({});

  // Validaciones
  const validateForm = () => {
    const errors = {};
    
    if (!formData.email) {
      errors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email inválido';
    }
    
    if (!formData.password) {
      errors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      errors.password = 'La contraseña debe tener al menos 6 caracteres';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Manejar cambios en inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error del campo específico
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    // Limpiar error general
    if (error) {
      clearError();
    }
  };

  // Manejar envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const result = await login(formData);
    
    if (result.success && onSuccess) {
      onSuccess(result);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Error general */}
      {error && (
        <div className="bg-orange-900/20 border border-orange-500/50 rounded-lg p-4">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-orange-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-orange-300 text-sm">{error}</span>
          </div>
        </div>
      )}

      {/* Campo Email */}
      <Input
        type="email"
        name="email"
        label="Email"
        value={formData.email}
        onChange={handleChange}
        placeholder="usuario@ejemplo.com"
        error={formErrors.email}
        required
        autoComplete="email"
      />

      {/* Campo Password */}
      <Input
        type="password"
        name="password"
        label="Contraseña"
        value={formData.password}
        onChange={handleChange}
        placeholder="Tu contraseña"
        error={formErrors.password}
        required
        autoComplete="current-password"
      />

      {/* Botón Submit */}
      <Button
        type="submit"
        variant="primary"
        size="lg"
        loading={isLoading}
        className="w-full"
      >
        {isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
      </Button>

      {/* Enlaces adicionales */}
      <div className="text-center">
        <p className="text-slate-400 text-sm">
          ¿No tienes cuenta?{' '}
          <a 
            href="/register" 
            className="text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            Regístrate aquí
          </a>
        </p>
      </div>
    </form>
  );
};

export default LoginForm;