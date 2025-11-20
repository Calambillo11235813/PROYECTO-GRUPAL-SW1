import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Play, Pause, RefreshCw, FileAudio, FileText } from 'lucide-react';

const AudioPlayer = ({ audioUrl, fileName, onDownloadCertificate }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const audioRef = useRef(null);

  // Resetear estados cuando cambia la URL
  useEffect(() => {
    if (audioUrl) {
      setLoading(true);
      setError(null);
      setIsPlaying(false);
    }
  }, [audioUrl]);

  const togglePlayPause = useCallback(async () => {
    const audio = audioRef.current;
    if (!audio) return;

    try {
      if (audio.paused) {
        await audio.play();
      } else {
        audio.pause();
      }
    } catch (e) {
      console.error('Error al interactuar con el audio:', e);
    }
  }, []);

  // Manejo de eventos del audio nativo
  const handleLoadedData = () => {
    setLoading(false);
    setError(null);
  };

  const handleError = (e) => {
    const audio = e.target;
    console.error('Error nativo de audio:', audio.error);
    
    let msg = 'No se puede reproducir el audio';
    if (audio.error) {
      switch (audio.error.code) {
        case 1: msg = 'Aborted: La carga fue cancelada'; break;
        case 2: msg = 'Network: Error de red al cargar'; break;
        case 3: msg = 'Decode: Error al decodificar el audio'; break;
        case 4: msg = 'Source Not Supported: Formato no soportado o URL inválida'; break;
        default: break;
      }
    }
    setError(msg);
    setLoading(false);
    setIsPlaying(false);
  };

  const handlePlay = () => setIsPlaying(true);
  const handlePause = () => setIsPlaying(false);
  const handleEnded = () => setIsPlaying(false);

  return (
    <div className="mb-4 bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-cyan-400 font-medium flex items-center space-x-2">
          <FileAudio className="w-5 h-5" />
          <span>Audio</span>
        </h4>
        {onDownloadCertificate && (
          <button
            onClick={onDownloadCertificate}
            className="flex items-center space-x-1 px-3 py-1.5 text-xs font-medium rounded-lg bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500/20 transition-colors border border-cyan-500/20"
            title="Descargar certificado"
          >
            <FileText className="w-3 h-3" />
            <span>Certificado</span>
          </button>
        )}
      </div>

      {/* Mensaje de error */}
      {error && (
        <div className="text-center py-2 mb-2 bg-red-500/10 rounded text-red-400 text-sm border border-red-500/20">
          {error}
        </div>
      )}

      <div className="flex items-center space-x-4">
        {/* Botón de Control */}
        <button
          onClick={togglePlayPause}
          disabled={loading || !!error || !audioUrl}
          className={`p-3 rounded-full transition-all duration-200 flex-shrink-0 ${
            loading || !audioUrl
              ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
              : isPlaying
                ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30 hover:scale-105 border border-red-500/30'
                : 'bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30 hover:scale-105 border border-cyan-500/30'
          }`}
        >
          {loading ? (
            <RefreshCw className="w-5 h-5 animate-spin" />
          ) : isPlaying ? (
            <Pause className="w-5 h-5 fill-current" />
          ) : (
            <Play className="w-5 h-5 fill-current" />
          )}
        </button>

        {/* Player Nativo (Oculto visualmente pero funcional) y metadatos */}
        <div className="flex-1 min-w-0 flex flex-col justify-center">
            {/* Usamos el tag audio real.
               React maneja los eventos directamente con props (onPlay, onPause, etc)
               Esto es mucho más seguro que addEventListener manuales.
            */}
            <audio
              ref={audioRef}
              src={audioUrl}
              preload="metadata"
              onPlay={handlePlay}
              onPause={handlePause}
              onEnded={handleEnded}
              onLoadedData={handleLoadedData}
              onError={handleError}
              className="hidden" // Lo ocultamos para usar nuestros controles personalizados
            />
            
            {/* Barra de progreso visual simple (opcional, solo estética) */}
            <div className="w-full h-1.5 bg-slate-700 rounded-full overflow-hidden mb-2">
                <div className={`h-full bg-cyan-500 ${loading ? 'animate-pulse w-full opacity-50' : 'w-0'}`} />
            </div>

            {fileName && (
              <div className="text-xs text-slate-400 truncate font-mono" title={fileName}>
                {fileName}
              </div>
            )}
        </div>
      </div>
    </div>
  );
};

export default AudioPlayer;