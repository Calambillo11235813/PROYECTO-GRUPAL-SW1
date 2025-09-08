import React, { useState } from 'react';
import { useAuth } from '../context/authContext';
import { Button } from '../components/componentExport';
import Navbar from '../components/Navbar/Navbar'; // Eliminé las llaves { }

// Importando componentes del módulo de texto
import {
  TextAnalyzer,
  FileAnalysis,
  ModelComparison,
  ServiceStatus,
  LoadingSpinner
} from '../components/Modulo_Texto/TextExport';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('analyze');
  const [isLoading, setIsLoading] = useState(false);
  
  // Función para manejar el cambio de estado de carga
  const handleLoadingChange = (loading) => {
    setIsLoading(loading);
  };

  // Función para manejar el cambio de pestañas
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 fixed inset-0 overflow-auto">
      {/* Navbar global */}
      <Navbar />
      
      {/* Spinner de carga global */}
      {isLoading && <LoadingSpinner fullScreen text="Procesando..." />}
      
      {/* Contenido principal */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Panel izquierdo principal */}
          <div className="lg:col-span-8">
            {/* Tabs de navegación */}
            <div className="mb-6">
              <div className="flex space-x-1 bg-slate-800/80 p-1 rounded-lg border border-cyan-500/20">
                {/*
                  Aquí se definen las pestañas para la navegación entre diferentes secciones:
                  - Análisis de Texto
                  - Comparar Modelos
                  - Análisis de Archivo
                */}
                {[
                  { id: 'analyze', label: 'Análisis de Texto', icon: '📝' },
                  { id: 'compare', label: 'Comparar Modelos', icon: '⚖️' },
                  { id: 'file', label: 'Análisis de Archivo', icon: '📄' }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => handleTabChange(tab.id)}
                    className={`
                      flex-1 flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium transition-all duration-200
                      ${activeTab === tab.id 
                        ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white shadow-[0_0_10px_rgba(6,182,212,0.5)]' 
                        : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
                      }
                    `}
                  >
                    <span className="mr-2">{tab.icon}</span>
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Contenido principal basado en la pestaña activa */}
            <div className="bg-slate-800/70 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
              {/* Tab: Análisis de Texto */}
              {activeTab === 'analyze' && (
                <TextAnalyzer 
                  onLoadingChange={handleLoadingChange}
                />
              )}

              {/* Tab: Comparar Modelos */}
              {activeTab === 'compare' && (
                <ModelComparison 
                  onLoadingChange={handleLoadingChange}
                />
              )}

              {/* Tab: Análisis de Archivo */}
              {activeTab === 'file' && (
                <FileAnalysis 
                  onLoadingChange={handleLoadingChange}
                />
              )}
            </div>
          </div>

          {/* Panel lateral derecho */}
          <div className="lg:col-span-4 space-y-6">
            {/* Estado del servicio */}
            <div className="bg-slate-800/70 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
              <h3 className="text-lg font-bold text-white mb-4">
                Estado del Sistema
              </h3>
              <ServiceStatus 
                refreshInterval={30000} 
                showDetails={true}
              />
            </div>

            {/* Información de usuario */}
            <div className="bg-slate-800/70 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center">
                <span className="mr-2">👤</span>
                Perfil de Usuario
              </h3>
              
              {user ? (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Nombre:</span>
                      <span className="text-slate-200">
                        {user.first_name} {user.last_name}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Email:</span>
                      <span className="text-slate-200">
                        {user.email}
                      </span>
                    </div>
                  </div>
                  
                  <Button 
                    variant="secondary" 
                    size="sm" 
                    onClick={logout}
                    className="w-full"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Cerrar Sesión
                  </Button>
                </div>
              ) : (
                <div className="text-slate-400">
                  No ha iniciado sesión
                </div>
              )}
            </div>

            {/* Información de Modelos */}
            <div className="bg-slate-800/70 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
              <h3 className="text-lg font-bold text-white mb-4">
                🧠 Información de Modelos
              </h3>
              
              <div className="space-y-3 text-sm">
                <div>
                  <div className="text-cyan-400 font-medium">Modelo B - Sensible</div>
                  <div className="text-slate-300">Detecta patrones sutiles de IA con alta sensibilidad</div>
                </div>
                <div>
                  <div className="text-purple-400 font-medium">Modelo N - Conservador</div>
                  <div className="text-slate-300">Análisis más conservador con menos falsos positivos</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;