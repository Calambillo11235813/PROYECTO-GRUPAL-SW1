import React, { useState } from 'react';
import AudioUpload from '../components/Modulo_Audio/AudioUpload';
import AudioResultCard from '../components/Modulo_Audio/AudioResultCard';
import AudioHistory from '../components/Modulo_Audio/AudioHistory';
import { Upload, Zap, Clock } from 'lucide-react';

const DashboardAudio = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [results, setResults] = useState([]);

  const handleUploadSuccess = (apiResponse) => {
    const response = apiResponse.data || apiResponse;
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
    console.log('Respuesta de la API:', response);
    let probValue = 0;
    
    if (response.probability !== undefined && response.probability !== null) {
      probValue = Number(response.probability);
    } else if (typeof response.result === 'number') {
      // Caso directo de TruthScan donde result es el float (ej: 0.873)
      probValue = response.result;
    } else if (response.score !== undefined) {
      probValue = Number(response.score);
    }

    const probPercentage = probValue <= 1 ? probValue * 100 : probValue;

    const label = (response.result || response.label || '').toString().toLowerCase();
    const explicitAI = label === 'ai' || label === 'fake' || label === 'generated';
    
    // La verdad definitiva:
    const isAI = explicitAI || probPercentage > 50;

    // Construir URL del espectrograma (igual que antes)
    let spectrogramUrl = "";
    if (response.spectrogram) {
      spectrogramUrl = response.spectrogram.startsWith('http') 
        ? response.spectrogram 
        : `${import.meta.env.VITE_API_BASE_URL}${response.spectrogram.replace(/^\//, '')}`;
    }

    let audioUrl = '#';
    if (response.file) {
        const filePath = response.file;
        
        // Caso 1: Si ya es una URL completa (http/https - ej. S3 de TruthScan)
        if (filePath.startsWith('http')) {
            audioUrl = filePath;
        } 
        // Caso 2: Si es una ruta relativa local (ej. /media/audios/...)
        else {
            // Aseguramos que la URL base termine en barra y el path no empiece por ella
            const cleanBase = apiBaseUrl.endsWith('/') ? apiBaseUrl : `${apiBaseUrl}/`;
            const cleanPath = filePath.startsWith('/') ? filePath.slice(1) : filePath;
            
            audioUrl = `${cleanBase}${cleanPath}`; // Resultado: http://localhost:8000/media/...
        }
    } 
    // Fallback: Si el backend solo devuelve el ID de la entidad
    else if (response.id) {
        audioUrl = `${apiBaseUrl}api/audio/${response.id}/`;
    }
    
    const result = {
      id: response.id || Date.now(),
      probabilidad: probPercentage, 
      es_ia: isAI,
      spectrogram_url: spectrogramUrl,
      audio_url: audioUrl,
    };
    console.log('URL de audio final para el navegador:', audioUrl);
    console.log('Resultado normalizado:', result);
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