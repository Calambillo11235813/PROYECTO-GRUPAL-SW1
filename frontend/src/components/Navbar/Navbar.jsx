import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import NavItem from './NavItem';
import MobileMenu from './MobileMenu';

const Navbar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  // Definición de módulos para la navegación
  const modules = [
    { 
      name: 'Texto', 
      path: '/text', 
      icon: '📝', 
      isActive: true 
    },
    { 
      name: 'Audio', 
      path: '/audio', 
      icon: '🔊', 
      isActive: false,  // Cambiar a true cuando implementes este módulo
      comingSoon: true
    },
    { 
      name: 'Código', 
      path: '/code', 
      icon: '💻', 
      isActive: false,  // Cambiar a true cuando implementes este módulo
      comingSoon: true
    },
    { 
      name: 'Video', 
      path: '/video', 
      icon: '🎬', 
      isActive: false,  // Cambiar a true cuando implementes este módulo
      comingSoon: true
    }
  ];

  return (
    <nav className="bg-slate-900/70 backdrop-blur-md border-b border-cyan-500/30 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo y título */}
          <div className="flex-shrink-0 flex items-center">
            <Link to="/" className="flex items-center">
              <span className="text-2xl mr-2">🤖</span>
              <span className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">
                AI Detector
              </span>
            </Link>
          </div>

          {/* Links de navegación - Escritorio */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-4">
              {modules.map((module) => (
                <NavItem 
                  key={module.name}
                  name={module.name}
                  path={module.path}
                  icon={module.icon}
                  isActive={module.isActive && location.pathname.includes(module.path)}
                  comingSoon={module.comingSoon}
                />
              ))}
            </div>
          </div>

          {/* Botón de perfil/configuración */}
          <div className="hidden md:block">
            <Link 
              to="/profile" 
              className="text-slate-300 hover:text-cyan-400 transition-colors p-2 rounded-full hover:bg-slate-800"
            >
              <span className="sr-only">Perfil</span>
              <span className="text-xl">👤</span>
            </Link>
          </div>

          {/* Botón del menú móvil */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-slate-300 hover:text-cyan-400 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-cyan-500"
              aria-expanded="false"
            >
              <span className="sr-only">Abrir menú principal</span>
              {/* Icono de menú/cerrar */}
              {isMobileMenuOpen ? (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Menú móvil */}
      <MobileMenu 
        isOpen={isMobileMenuOpen} 
        modules={modules} 
        currentPath={location.pathname} 
      />

      {/* Efecto de línea neón */}
      <div className="h-0.5 w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent"></div>
    </nav>
  );
};

export default Navbar;