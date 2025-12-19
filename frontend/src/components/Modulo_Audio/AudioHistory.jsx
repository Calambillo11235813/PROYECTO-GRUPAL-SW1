import React, { useState, useEffect } from 'react';
import { RefreshCw, FileAudio, Clock, Download, Trash2, AlertTriangle, AlertCircle } from 'lucide-react';
import AudioResultCard from './AudioResultCard';
import { deleteAudio, deleteAllAudios } from '../../services/audioService';
import { API_ENDPOINTS } from '../../services/config';

const AudioHistory = () => {
  const [audios, setAudios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all'); // all, ai, human
  const [sortBy, setSortBy] = useState('recent'); // recent, probability, name
  const [expandedId, setExpandedId] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchHistory = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('No se encontró el token de autenticación');
      }

      const response = await fetch(`${API_ENDPOINTS.AUDIO}/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Error al cargar el historial');
      }

      const data = await response.json();

    // Transformar la respuesta para que coincida con la estructura esperada
    const formattedAudios = data.map(audio => {
            // 1. Probabilidad (0-100)
            const rawProb = audio.probability || 0;
            // Aseguramos que la probabilidad se escala a 0-100
            const probPercentage = rawProb <= 1 ? Math.round(rawProb * 100) : Math.round(rawProb);
            
            // 2. Determinación de IA (Consistente con Dashboard)
            const label = (audio.result || '').toString().toLowerCase();
            const explicitAI = label === 'ai' || label === 'fake';
            const isAI = explicitAI || probPercentage > 50;

            // 3. Corrección de URL de audio (para manejar rutas locales)
            let audioUrl = audio.file;
            if (!audioUrl) {
                audioUrl = `${API_ENDPOINTS.AUDIO}/${audio.id}/`;
            } else if (!audioUrl.startsWith('http')) {
                audioUrl = audioUrl.startsWith('/') ? audioUrl : `/${audioUrl}`;
            }

            // 4. Corrección de URL de espectrograma
            let spectrogramUrl = audio.spectrogram;
            if (spectrogramUrl && !spectrogramUrl.startsWith('http')) {
                spectrogramUrl = spectrogramUrl.startsWith('/') ? spectrogramUrl : `/${spectrogramUrl}`;
            }

            return {
            id: audio.id,
            original_filename: audio.original_filename || `audio_${audio.id}`,
            probabilidad: probPercentage, 
            es_ia: isAI,
            created_at: audio.created_at,
            audio_url: audioUrl, 
            spectrogram_url: spectrogramUrl,
            // Dejamos los campos originales por si son necesarios
            file: audio.file,
            result: audio.result,
            probability: audio.probability
            };
        });

      setAudios(formattedAudios);
      setError('');
    } catch (err) {
      console.error('Error al cargar el historial:', err);
      setError('No se pudo cargar el historial. Intenta recargar la página.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Cargar historial al montar el componente
  useEffect(() => {
    fetchHistory();
  }, []);

  // Función para manejar la recarga manual
  const handleRefresh = () => {
    setRefreshing(true);
    fetchHistory();
  };

  // Función para eliminar un audio individual
  const handleDelete = async (audioId) => {
    if (!confirm('¿Estás seguro de eliminar este audio? Esta acción no se puede deshacer.')) return;
    
    try {
      await deleteAudio(audioId);
      setAudios(audios.filter(a => a.id !== audioId));
    } catch (err) {
      console.error('Error al eliminar audio:', err);
      alert('Error al eliminar el audio');
    }
  };

  // Función para eliminar todos los audios
  const handleDeleteAll = async () => {
    if (!confirm('¿Estás seguro de eliminar TODO el historial? Esta acción no se puede deshacer.')) return;
    
    try {
      await deleteAllAudios();
      setAudios([]);
    } catch (err) {
      console.error('Error al eliminar historial:', err);
      alert('Error al eliminar el historial');
    }
  };

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
    if (!dateString) return 'Fecha desconocida';
    
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Fecha inválida';
      
      return new Intl.DateTimeFormat('es-ES', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      }).format(date);
    } catch (e) {
      console.error('Error al formatear fecha:', e);
      return 'Fecha inválida';
    }
  };

  const handleDownload = async (audio) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('No se encontró el token de autenticación');
      }

      // Si ya tenemos una URL directa al archivo, usamos esa
      if (audio.audio_url && audio.audio_url.startsWith('http')) {
        window.open(audio.audio_url, '_blank');
        return;
      }

      // Si no, hacemos una petición al endpoint de descarga
      const response = await fetch(`${API_ENDPOINTS.AUDIO}/${audio.id}/download/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Error al descargar el archivo');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = audio.original_filename || `audio_${audio.id}.wav`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (err) {
      console.error('Error al descargar el audio:', err);
      alert('No se pudo descargar el archivo: ' + err.message);
    }
  };

  if (loading && !refreshing) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-slate-100 mb-1">Historial de Análisis de Audio</h2>
            <p className="text-slate-400">Revisa tus análisis de audio anteriores</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="p-4 rounded-full bg-red-500/10 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
          <AlertCircle className="w-8 h-8 text-red-400" />
        </div>
        <h4 className="text-lg font-medium text-slate-300 mb-2">Error al cargar el historial</h4>
        <p className="text-slate-500 mb-4">{error}</p>
        <button
          onClick={handleRefresh}
          className="px-4 py-2 rounded-xl bg-cyan-500 text-white hover:bg-cyan-600 transition-colors flex items-center mx-auto"
          disabled={refreshing}
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
          {refreshing ? 'Cargando...' : 'Reintentar'}
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header con filtros */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
        <div>
          <div className="flex items-center space-x-4">
            <h3 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Historial de Análisis
            </h3>
            <button
              onClick={handleRefresh}
              className="p-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-400 hover:text-cyan-400 transition-colors"
              disabled={refreshing}
              title="Actualizar"
            >
              <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
            </button>
            {audios.length > 0 && (
              <button
                onClick={handleDeleteAll}
                className="p-1.5 rounded-lg bg-red-600/20 hover:bg-red-600 text-red-400 hover:text-white transition-colors"
                title="Eliminar todo"
              >
                <AlertTriangle className="w-4 h-4" />
              </button>
            )}
          </div>
          <p className="text-slate-400 mt-1">
            {audios.length} {audios.length === 1 ? 'archivo analizado' : 'archivos analizados'}
          </p>
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
                    <div className="min-w-0">
                      <div className="font-medium text-slate-300 truncate max-w-xs">
                        {audio.original_filename}
                      </div>
                      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-slate-500">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-3 h-3 flex-shrink-0" />
                          <span>{formatDate(audio.created_at)}</span>
                        </div>
                        <div className={`font-medium ${audio.es_ia ? 'text-red-400' : 'text-green-400'}`}>
                          {audio.probabilidad}% {audio.es_ia ? 'IA' : 'Humano'}
                        </div>
                        {audio.spectrogram_url && (
                          <div className="flex items-center space-x-1 text-cyan-400">
                            <span className="text-xs bg-cyan-500/10 px-2 py-0.5 rounded-full">
                              Espectrograma disponible
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleDownload(audio)}
                      className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-400 hover:text-cyan-400 transition-all duration-200"
                      title="Descargar"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(audio.id)}
                      className="p-2 rounded-lg bg-red-600/20 hover:bg-red-600 text-red-400 hover:text-white transition-all duration-200"
                      title="Eliminar"
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