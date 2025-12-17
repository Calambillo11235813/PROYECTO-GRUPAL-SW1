import React, { useState } from 'react';
import VideoUpload from '../components/Modulo_Video/VideoUpload';
import VideoHistoryFull from '../components/Modulo_Video/VideoHistoryFull';
import VideoPlayer from '../components/Modulo_Video/VideoPlayer';
import VideoResultCard from '../components/Modulo_Video/VideoResultCard';
import { Upload, Zap, Clock } from 'lucide-react';

export default function DashboardVideo() {
  const [activeTab, setActiveTab] = useState('upload');
  const [previewSrc, setPreviewSrc] = useState(null);
  const [latestResult, setLatestResult] = useState(null);

  const handleUploadSuccess = (result) => {
    setLatestResult(result);
  };

  const tabs = [
    { id: 'upload', label: 'Subir Video', icon: Upload },
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
              <div className="space-y-6">
                <VideoUpload onPreview={setPreviewSrc} onResult={handleUploadSuccess} />
                {previewSrc && (
                  <div className="bg-slate-900/50 p-4 rounded-lg backdrop-blur-sm border border-slate-700/50">
                    <h3 className="text-cyan-300 font-semibold mb-3">Previsualización</h3>
                    <VideoPlayer src={previewSrc} />
                  </div>
                )}
                {latestResult && (
                  <VideoResultCard result={latestResult} />
                )}
              </div>
            )}
            
            {activeTab === 'history' && <VideoHistoryFull />}
          </div>
        </div>
      </div>
    </>
  );
}
