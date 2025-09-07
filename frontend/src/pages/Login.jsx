import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';
import LoginForm from '../components/forms/LoginForm';

const Login = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  // Redirigir si ya está autenticado
  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleLoginSuccess = (result) => {
    console.log('Login exitoso:', result);
    // Redirigir al dashboard o página principal
    navigate('/dashboard', { replace: true });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center px-4">
      {/* Efectos de fondo cyberpunk */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-purple-500/10 to-cyan-500/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-cyan-500/10 to-purple-500/10 rounded-full blur-3xl" />
        {/* Efectos adicionales cyberpunk */}
        <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-yellow-300/5 rounded-full blur-2xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-40 h-40 bg-green-500/5 rounded-full blur-2xl animate-pulse delay-1000" />
      </div>

      {/* Container principal */}
      <div className="relative z-10 w-full max-w-md">
        {/* Card de login */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-8 shadow-2xl shadow-purple-500/20">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="mb-4">
              {/* Logo/Icon */}
              <div className="mx-auto w-16 h-16 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/25">
                <svg className="w-8 h-8 text-slate-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
            </div>
            
            <h1 className="text-3xl font-bold text-slate-100 mb-2">
              Bienvenido
            </h1>
            <p className="text-cyan-400">
              Inicia sesión en tu cuenta
            </p>
          </div>

          {/* Formulario */}
          <LoginForm onSuccess={handleLoginSuccess} />

          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-slate-700">
            <p className="text-center text-slate-400 text-xs">
              Detector de IA v1.0 - Sistema Cyberpunk
            </p>
          </div>
        </div>

        {/* Información adicional */}
        <div className="mt-6 text-center">
          <p className="text-cyan-300 text-sm">
            Sistema de detección de contenido generado por IA
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;