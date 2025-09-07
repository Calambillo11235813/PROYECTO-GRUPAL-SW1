import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

const MobileMenu = ({ isOpen, modules, currentPath }) => {
  if (!isOpen) return null;

  return (
    <div className="md:hidden">
      <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-slate-700/50">
        {modules.map((module) => {
          const isActive = module.isActive && currentPath.includes(module.path);
          
          // Clases base para todos los elementos
          const baseClasses = "block px-3 py-2 rounded-md text-base font-medium flex items-center";
          
          // Clases específicas según estado
          const stateClasses = isActive
            ? "bg-slate-800 text-cyan-400 border border-cyan-500/30 shadow-[0_0_8px_rgba(6,182,212,0.3)]"
            : "text-slate-300 hover:bg-slate-800/60 hover:text-cyan-300";
            
          // Si está marcado como próximamente
          if (module.comingSoon) {
            return (
              <div 
                key={module.name}
                className={`${baseClasses} opacity-60 cursor-not-allowed text-slate-400`}
              >
                <span className="mr-2">{module.icon}</span>
                {module.name}
                <span className="ml-2 text-xs bg-slate-800 px-1.5 py-0.5 rounded text-yellow-300 border border-yellow-500/30">
                  Pronto
                </span>
              </div>
            );
          }
          
          return (
            <Link
              key={module.name}
              to={module.path}
              className={`${baseClasses} ${stateClasses}`}
            >
              <span className="mr-2">{module.icon}</span>
              {module.name}
            </Link>
          );
        })}
      </div>
      
      {/* Elemento de perfil en móvil */}
      <div className="pt-4 pb-3 border-t border-slate-700">
        <div className="flex items-center px-5">
          <div className="flex-shrink-0">
            <span className="text-xl">👤</span>
          </div>
          <div className="ml-3">
            <div className="text-base font-medium text-slate-200">Usuario</div>
            <div className="text-sm font-medium text-slate-400">usuario@ejemplo.com</div>
          </div>
        </div>
        <div className="mt-3 px-2 space-y-1">
          <Link
            to="/profile"
            className="block px-3 py-2 rounded-md text-base font-medium text-slate-300 hover:text-cyan-300 hover:bg-slate-800"
          >
            Mi Perfil
          </Link>
          <Link
            to="/settings"
            className="block px-3 py-2 rounded-md text-base font-medium text-slate-300 hover:text-cyan-300 hover:bg-slate-800"
          >
            Configuración
          </Link>
          <button
            className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-slate-300 hover:text-orange-400 hover:bg-slate-800"
          >
            Cerrar Sesión
          </button>
        </div>
      </div>
    </div>
  );
};

MobileMenu.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  modules: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      path: PropTypes.string.isRequired,
      icon: PropTypes.string.isRequired,
      isActive: PropTypes.bool,
      comingSoon: PropTypes.bool
    })
  ).isRequired,
  currentPath: PropTypes.string.isRequired
};

export default MobileMenu;