import React, { useState } from 'react';
import { useAuth } from '../context/authContext';
import { Button } from '../components/componentExport';
import Navbar from '../components/Navbar/Navbar'; // Eliminé las llaves { }

// Importando componentes del módulo de texto
import {
  TextAnalyzer,
  ModelComparison,
  ServiceStatus,
  LoadingSpinner
} from '../components/Modulo_Texto/TextExport';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  
  // Función para manejar el cambio de estado de carga
  const handleLoadingChange = (loading) => {
    setIsLoading(loading);
  };

  return (
    <>
      {/* Fondo oscuro que cubre toda la pantalla */}
      <div className="fixed inset-0 w-full h-full bg-cyber-bg-primary -z-10" />

      {/* Contenido principal con padding-top para el navbar */}
      <div className="min-h-screen w-full pt-0">
        {isLoading && <LoadingSpinner fullScreen text="Procesando..." />}
        <main className="w-full flex justify-center px-2 sm:px-4 lg:px-8 py-8 mt-2">
          <div className="w-full max-w-7xl">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              
              {/* Panel izquierdo principal */}
              <div className="lg:col-span-8">
                {/* Contenido principal */}
                <div className="bg-slate-800/70 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
                  <TextAnalyzer 
                    onLoadingChange={handleLoadingChange}
                  />
                </div>
              </div>

              {/* Panel lateral derecho */}
              <div className="lg:col-span-4 flex flex-col gap-6">
                {/* Estado del servicio */}
                <div className="flex-1 bg-slate-800/70 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 shadow-[0_0_15px_rgba(6,182,212,0.2)] flex flex-col">
                  <h3 className="text-lg font-bold text-white mb-4">
                    Estado del Sistema
                  </h3>
                  <div className="flex-1">
                    <ServiceStatus 
                      refreshInterval={900000} 
                      showDetails={true}
                    />
                  </div>
                </div>

                {/* Información de usuario */}
                <div className="flex-1 bg-slate-800/70 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 shadow-[0_0_15px_rgba(6,182,212,0.2)] flex flex-col">
                  <h3 className="text-lg font-bold text-white mb-4 flex items-center">
                    <span className="mr-2">👤</span>
                    Perfil de Usuario
                  </h3>
                  
                  <div className="flex-1 flex flex-col justify-between">
                    {user ? (
                      <div className="space-y-4 flex flex-col h-full">
                        <div className="space-y-2 flex-1">
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
                          className="w-full mt-auto"
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
                </div>

                
              </div>
            </div>
          </div>
        </main>
      </div>
    </>
  );
};

export default Dashboard;