import React from 'react';
import { User, Mail, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';

const Profile = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  return (
    <>
      {/* Fondo oscuro que cubre toda la pantalla */}
      <div className="fixed inset-0 w-full h-full bg-cyber-bg-primary -z-10" />

      {/* Contenido principal */}
      <div className="min-h-screen w-full pt-8">
        <div className="flex items-center justify-center w-full p-4">
        <div className="w-full max-w-md bg-slate-800/80 backdrop-blur-sm rounded-xl p-8 shadow-xl border border-slate-700/50">
        <div className="flex flex-col items-center text-center">
          {/* User Icon */}
          <div className="w-24 h-24 rounded-full bg-cyan-900/30 flex items-center justify-center mb-6">
            <User className="w-12 h-12 text-cyan-400" />
          </div>
          
          {/* User Info */}
          <h1 className="text-2xl font-bold text-cyan-400 mb-1">
            {user.username || 'Usuario'}
          </h1>
          
          <div className="flex items-center space-x-2 text-slate-300 mb-8">
            <Mail className="w-4 h-4" />
            <span>{user.email || 'usuario@ejemplo.com'}</span>
          </div>
          
          {/* Logout Button */}
          <button
            onClick={handleLogout}
            className="flex items-center space-x-2 px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
          >
            <LogOut className="w-5 h-5" />
            <span>Cerrar sesión</span>
          </button>
        </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Profile;
