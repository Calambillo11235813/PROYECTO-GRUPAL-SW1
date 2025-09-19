import React, { useState, useRef, useEffect } from 'react';
import { RefreshCw, FileAudio, Clock, Download, Trash2 } from 'lucide-react';
import AudioResultCard from './AudioResultCard';

// Componente AudioHistory mejorado
const AudioHistory = () => {
  const [audios, setAudios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, ai, human
  const [sortBy, setSortBy] = useState('recent'); // recent, probability, name
  const [expandedId, setExpandedId] = useState(null); // Nuevo estado para expandir detalles

  useEffect(() => {
    // Datos de ejemplo para la demo
    setTimeout(() => {
      setAudios([
        {
          id: 1,
          original_filename: "podcast_episode_01.mp3",
          probabilidad: 85,
          es_ia: true,
          created_at: "2024-09-19T10:30:00Z",
          audio_url: "/api/audio/1/download",
          spectrogram_url: "/api/spectrogram/1.png"
        },
        {
          id: 2,
          original_filename: "interview_recording.wav",
          probabilidad: 25,
          es_ia: false,
          created_at: "2024-09-19T09:15:00Z",
          audio_url: "/api/audio/2/download",
          spectrogram_url: "/api/spectrogram/2.png"
        },
        {
          id: 3,
          original_filename: "ai_voice_sample.mp3",
          probabilidad: 92,
          es_ia: true,
          created_at: "2024-09-18T16:45:00Z",
          audio_url: "/api/audio/3/download",
          spectrogram_url: "/api/spectrogram/3.png"
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredAudios = audios.filter(audio => {
    if (filter === 'ai') return audio.es_ia;
    if (filter === 'human') return !audio.es_ia;
    return true;
  });

  const sortedAudios = [...filteredAudios].sort((a, b) => {
    if (sortBy === 'recent') {
      return new Date(b.created_at) - new Date(a.created_at);
    }
    if (sortBy === 'probability') {
      return b.probabilidad - a.probabilidad;
    }
    if (sortBy === 'name') {
      return a.original_filename.localeCompare(b.original_filename);
    }
    return 0;
  });

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleDownload = (audio) => {
    // Lógica de descarga
    console.log('Downloading:', audio.original_filename);
  };

  const handleDelete = (audioId) => {
    setAudios(audios.filter(audio => audio.id !== audioId));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="flex items-center space-x-3">
          <RefreshCw className="w-6 h-6 text-cyan-400 animate-spin" />
          <span className="text-slate-300 text-lg">Cargando historial...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header con filtros */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
        <div>
          <h3 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
            Historial de Análisis
          </h3>
          <p className="text-slate-400 mt-1">{audios.length} archivos analizados</p>
        </div>

        <div className="flex flex-wrap gap-3">
          {/* Filtro por tipo */}
          <div className="flex bg-slate-800 rounded-xl p-1">
            {[
              { key: 'all', label: 'Todos' },
              { key: 'ai', label: 'IA' },
              { key: 'human', label: 'Humano' }
            ].map(option => (
              <button
                key={option.key}
                onClick={() => setFilter(option.key)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                  filter === option.key
                    ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white shadow-lg'
                    : 'text-slate-400 hover:text-slate-300'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>

          {/* Ordenar */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-sm focus:border-cyan-500 focus:outline-none"
          >
            <option value="recent">Más reciente</option>
            <option value="probability">Probabilidad</option>
            <option value="name">Nombre</option>
          </select>
        </div>
      </div>

      {/* Lista de audios */}
      {sortedAudios.length === 0 ? (
        <div className="text-center py-12">
          <div className="p-4 rounded-full bg-slate-800 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
            <FileAudio className="w-8 h-8 text-slate-500" />
          </div>
          <h4 className="text-lg font-medium text-slate-300 mb-2">No hay análisis previos</h4>
          <p className="text-slate-500">
            {filter === 'all' 
              ? 'Sube tu primer archivo de audio para comenzar'
              : `No hay archivos ${filter === 'ai' ? 'generados por IA' : 'humanos'} en tu historial`
            }
          </p>
        </div>
      ) : (
        <div className="grid gap-6">
          {sortedAudios.map((audio) => (
            <div key={audio.id} className="relative">
              {/* Mini card para el historial */}
              <div className="p-4 rounded-xl bg-gradient-to-r from-slate-800/50 to-slate-700/50 border border-slate-700/50 hover:border-cyan-500/30 transition-all duration-300">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className={`p-2 rounded-lg ${audio.es_ia ? 'bg-red-500/20' : 'bg-green-500/20'}`}>
                      <FileAudio className={`w-5 h-5 ${audio.es_ia ? 'text-red-400' : 'text-green-400'}`} />
                    </div>
                    <div>
                      <div className="font-medium text-slate-300">{audio.original_filename}</div>
                      <div className="flex items-center space-x-4 text-sm text-slate-500">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-3 h-3" />
                          <span>{formatDate(audio.created_at)}</span>
                        </div>
                        <div className={`font-medium ${audio.es_ia ? 'text-red-400' : 'text-green-400'}`}>
                          {audio.probabilidad}% {audio.es_ia ? 'IA' : 'Humano'}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleDownload(audio)}
                      className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-400 hover:text-cyan-400 transition-all duration-200"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(audio.id)}
                      className="p-2 rounded-lg bg-slate-700 hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition-all duration-200"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setExpandedId(expandedId === audio.id ? null : audio.id)}
                      className="p-2 rounded-lg bg-slate-700 hover:bg-cyan-500/20 text-slate-400 hover:text-cyan-400 transition-all duration-200"
                    >
                      Ver detalles
                    </button>
                  </div>
                </div>
              </div>

              {/* Resultado expandido solo si se ha hecho click en "Ver detalles" */}
              {expandedId === audio.id && (
                <div className="absolute top-full left-0 right-0 z-10 mt-2">
                  <AudioResultCard 
                    result={audio} 
                    onDownload={handleDownload}
                    onDelete={handleDelete}
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
export default AudioHistory;