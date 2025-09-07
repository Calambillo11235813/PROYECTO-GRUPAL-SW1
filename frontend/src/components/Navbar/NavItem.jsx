import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

const NavItem = ({ name, path, icon, isActive, comingSoon }) => {
  // Determinar las clases según el estado
  const baseClasses = "px-3 py-2 rounded-md text-sm font-medium flex items-center transition-all duration-200";
  
  // Clases específicas según estado
  const stateClasses = isActive
    ? "bg-slate-800 text-cyan-400 border border-cyan-500/30 shadow-[0_0_8px_rgba(6,182,212,0.3)]"
    : "text-slate-300 hover:bg-slate-800/60 hover:text-cyan-300";
    
  // Si está marcado como próximamente, deshabilitar
  if (comingSoon) {
    return (
      <div className={`${baseClasses} opacity-60 cursor-not-allowed text-slate-400`}>
        <span className="mr-1">{icon}</span>
        {name}
        <span className="ml-1 text-xs bg-slate-800 px-1.5 py-0.5 rounded text-yellow-300 border border-yellow-500/30">
          Pronto
        </span>
      </div>
    );
  }

  // Renderizar como link si está activo
  return (
    <Link to={path} className={`${baseClasses} ${stateClasses}`}>
      <span className="mr-1">{icon}</span>
      {name}
    </Link>
  );
};

NavItem.propTypes = {
  name: PropTypes.string.isRequired,
  path: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  isActive: PropTypes.bool,
  comingSoon: PropTypes.bool
};

NavItem.defaultProps = {
  isActive: false,
  comingSoon: false
};

export default NavItem;