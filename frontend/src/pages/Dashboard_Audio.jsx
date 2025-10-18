import React, { useState } from 'react';
import AudioUpload from '../components/Modulo_Audio/AudioUpload';
import AudioResultCard from '../components/Modulo_Audio/AudioResultCard';
import AudioHistory from '../components/Modulo_Audio/AudioHistory';
import { Upload, Zap, Clock } from 'lucide-react';

const DashboardAudio = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [results, setResults] = useState([]);

  const handleUploadSuccess = (apiResponse) => {
    // The backend returns the data in a nested 'data' property
    const response = apiResponse.data || apiResponse;
    
    // Construir la URL del espectrograma
    let spectrogramUrl = "";
    if (response.spectrogram) {
      // Si la respuesta ya incluye la URL completa del espectrograma
      spectrogramUrl = response.spectrogram.startsWith('http') 
        ? response.spectrogram 
        : `${import.meta.env.VITE_API_BASE_URL}${response.spectrogram.replace(/^\//, '')}`;
    }
    
    const result = {
      id: response.id || Date.now(),
      probabilidad: response.probability || Math.floor(Math.random() * 100),
      es_ia: response.result === 'ai', // Use the result from the backend if available
      spectrogram_url: spectrogramUrl,
      audio_url: response.file || (response.id ? `${import.meta.env.VITE_API_BASE_URL}api/audio/${response.id}/` : '#')
    };
    
    console.log('Resultado del análisis:', result);
    
    // If we have a probability but no explicit result, determine it from the probability
    if (response.probability !== undefined && response.result === undefined) {
      result.es_ia = response.probability > 50;
    }
    
    setResults([result, ...results]);
    setActiveTab('results');
  };

  const tabs = [
    { id: 'upload', label: 'Subir Audio', icon: Upload },
    { id: 'results', label: 'Resultados', icon: Zap },
    { id: 'history', label: 'Historial', icon: Clock }
  ];

  return (
    <>
      {/* Fondo oscuro que cubre toda la pantalla */}
      <div className="fixed inset-0 w-full h-full bg-cyber-bg-primary -z-10" />

      {/* Contenido principal con padding-top para el navbar */}
      <div className="min-h-screen w-full pt-8">
        <div className="max-w-4xl mx-auto">
          {/* Navigation */}
          <div className="flex justify-center mb-8">
            <div className="flex bg-slate-800/50 rounded-2xl p-1 backdrop-blur-sm border border-slate-700/50">
              {tabs.map(tab => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-xl font-medium transition-all duration-200 ${
                      activeTab === tab.id
                        ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white shadow-lg'
                        : 'text-slate-400 hover:text-slate-300'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Content */}
          <div className="space-y-8">
            {activeTab === 'upload' && (
              <AudioUpload onUploadSuccess={handleUploadSuccess} />
            )}
            
            {activeTab === 'results' && (
              <div className="space-y-6">
                {results.length === 0 ? (
                  <div className="text-center py-12">
                    <Zap className="w-12 h-12 text-slate-500 mx-auto mb-4" />
                    <h3 className="text-xl font-medium text-slate-300 mb-2">No hay resultados</h3>
                    <p className="text-slate-500">Sube un archivo de audio para ver los resultados aquí</p>
                  </div>
                ) : (
                  results.map(result => (
                    <AudioResultCard key={result.id} result={result} />
                  ))
                )}
              </div>
            )}
            
            {activeTab === 'history' && <AudioHistory />}
          </div>
        </div>
      </div>
    </>
  );
};

export default DashboardAudio;