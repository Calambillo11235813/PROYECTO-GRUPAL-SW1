import React, { useState, useEffect, useRef } from 'react';
import { Upload, Volume2, Play, Pause, Download, Trash2, RefreshCw, AlertCircle, CheckCircle, Clock, FileAudio, Zap } from 'lucide-react';

// Componente AudioResultCard mejorado
const AudioResultCard = ({ result, onDownload, onDelete }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const getProbabilityColor = (probability) => {
    if (probability >= 70) return 'text-red-400';
    if (probability >= 40) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getConfidenceLevel = (probability) => {
    if (probability >= 80) return 'Alta';
    if (probability >= 60) return 'Media';
    return 'Baja';
  };

  return (
    <div className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900/90 to-slate-800/90 border border-cyan-500/30 shadow-2xl backdrop-blur-sm hover:border-cyan-400/50 transition-all duration-300">
      {/* Efecto de glow animado */}
      <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 via-purple-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative p-6 space-y-4">
        {/* Header con icono animado */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500">
              <Zap className="w-5 h-5 text-white animate-pulse" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Análisis Completado
            </h3>
          </div>
          
          {/* Indicador de confianza */}
          <div className="px-3 py-1 rounded-full bg-slate-700/50 border border-cyan-500/30">
            <span className="text-xs text-cyan-400 font-medium">
              Confianza: {getConfidenceLevel(result.probabilidad)}
            </span>
          </div>
        </div>

        {/* Métricas principales */}
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm">Probabilidad IA</span>
              {result.es_ia ? 
                <AlertCircle className="w-4 h-4 text-red-400" /> : 
                <CheckCircle className="w-4 h-4 text-green-400" />
              }
            </div>
            <div className={`text-2xl font-bold ${getProbabilityColor(result.probabilidad)}`}>
              {result.probabilidad}%
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
            <div className="text-slate-400 text-sm mb-2">Clasificación</div>
            <div className={`text-lg font-bold ${result.es_ia ? 'text-red-400' : 'text-green-400'}`}>
              {result.es_ia ? '🤖 IA Generado' : '👤 Humano'}
            </div>
          </div>
        </div>

        {/* Barra de progreso visual */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-slate-400">
            <span>Humano</span>
            <span>IA</span>
          </div>
          <div className="w-full bg-slate-700/50 rounded-full h-3 overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-green-500 to-red-500 rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${result.probabilidad}%` }}
            />
          </div>
        </div>

        {/* Reproductor de audio */}
        {result.audio_url && (
          <div className="flex items-center space-x-4 p-4 rounded-xl bg-slate-800/30 border border-slate-700/50">
            <button
              onClick={handlePlayPause}
              className="p-3 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-400 hover:to-purple-400 transition-all duration-200 transform hover:scale-105"
            >
              {isPlaying ? 
                <Pause className="w-5 h-5 text-white" /> : 
                <Play className="w-5 h-5 text-white ml-1" />
              }
            </button>
            <div className="flex-1">
              <div className="text-sm text-slate-400 mb-1">Audio Original</div>
              <audio ref={audioRef} src={result.audio_url} className="w-full" />
            </div>
          </div>
        )}

        {/* Espectrograma */}
        {result.spectrogram_url && (
          <div className="space-y-2">
            <h4 className="text-cyan-400 font-medium flex items-center space-x-2">
              <Volume2 className="w-4 h-4" />
              <span>Análisis Espectral</span>
            </h4>
            <div className="relative group/img">
              <img 
                src={result.spectrogram_url} 
                alt="Espectrograma" 
                className="w-full rounded-xl border border-cyan-500/30 shadow-lg hover:shadow-cyan-500/20 transition-shadow duration-300" 
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/50 to-transparent rounded-xl opacity-0 group-hover/img:opacity-100 transition-opacity duration-200" />
            </div>
          </div>
        )}

        {/* Acciones */}
        <div className="flex space-x-2 pt-4 border-t border-slate-700/50">
          {onDownload && (
            <button
              onClick={() => onDownload(result)}
              className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 rounded-xl bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 hover:text-cyan-400 transition-all duration-200"
            >
              <Download className="w-4 h-4" />
              <span className="text-sm">Descargar</span>
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(result.id)}
              className="flex items-center justify-center px-4 py-2 rounded-xl bg-red-500/20 hover:bg-red-500/30 text-red-400 hover:text-red-300 transition-all duration-200"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
export default AudioResultCard;