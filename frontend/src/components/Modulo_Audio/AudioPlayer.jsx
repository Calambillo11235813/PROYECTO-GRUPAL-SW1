import { useState, useRef, useEffect, useCallback } from 'react';
import { Play, Pause, RefreshCw, FileAudio, FileText } from 'lucide-react';

const AudioPlayer = ({ audioUrl, fileName, onDownloadCertificate }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const audioRef = useRef(null);

  // Handle play/pause
  const togglePlayPause = useCallback(async () => {
    if (!audioRef.current) return;
    
    try {
      if (isPlaying) {
        await audioRef.current.pause();
      } else {
        await audioRef.current.play();
      }
    } catch (e) {
      console.error('Error al reproducir/pausar:', e);
      setError('No se pudo reproducir el audio');
      setLoading(false);
      setIsPlaying(false);
    }
  }, [isPlaying]);

  // Handle audio source changes and event listeners
  useEffect(() => {
    // Create a new audio element with preload set to 'metadata'
    const audio = new Audio();
    audio.preload = 'metadata';
    audioRef.current = audio;

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);
    const handleEnded = () => setIsPlaying(false);
    
    const handleError = (e) => {
      console.error('Audio error:', e);
      setError('No se puede reproducir el audio');
      setLoading(false);
      setIsPlaying(false);
    };
    
    const handleLoadedData = () => {
      setLoading(false);
      setError(null);
    };
    
    // Add event listeners
    audio.addEventListener('play', handlePlay);
    audio.addEventListener('pause', handlePause);
    audio.addEventListener('error', handleError);
    audio.addEventListener('loadeddata', handleLoadedData);
    audio.addEventListener('ended', handleEnded);
    
    // Set initial source if available
    if (audioUrl) {
      audio.src = audioUrl;
      try {
        // Some browsers might not return a Promise from load()
        const loadPromise = audio.load();
        if (loadPromise && typeof loadPromise.catch === 'function') {
          loadPromise.catch(handleError);
        }
      } catch (e) {
        handleError(e);
      }
    }
    
    // Cleanup function
    return () => {
      audio.pause();
      audio.removeEventListener('play', handlePlay);
      audio.removeEventListener('pause', handlePause);
      audio.removeEventListener('error', handleError);
      audio.removeEventListener('loadeddata', handleLoadedData);
      audio.removeEventListener('ended', handleEnded);
      
      // Clean up the audio element
      audio.src = '';
      if (audioRef.current === audio) {
        audioRef.current = null;
      }
    };
  }, [audioUrl]);

  // Update audio source when URL changes
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;
    
    // Reset state for new audio
    setLoading(true);
    setError(null);
    setIsPlaying(false);
    
    if (!audioUrl) {
      setLoading(false);
      setError('No hay URL de audio disponible');
      return;
    }
    
    // Set the new source
    audio.src = audioUrl;
    
    // Handle audio loading with better cross-browser support
    const handleCanPlay = () => {
      setLoading(false);
      audio.removeEventListener('canplay', handleCanPlay);
      audio.removeEventListener('error', handleLoadError);
    };
    
    const handleLoadError = (err) => {
      console.error('Error al cargar el audio:', err);
      setError('Error al cargar el audio');
      setLoading(false);
      audio.removeEventListener('canplay', handleCanPlay);
      audio.removeEventListener('error', handleLoadError);
    };
    
    // Add event listeners
    audio.addEventListener('canplay', handleCanPlay);
    audio.addEventListener('error', handleLoadError);
    
    // Try to load the audio
    try {
      const loadPromise = audio.load();
      if (loadPromise && typeof loadPromise.catch === 'function') {
        loadPromise.catch(handleLoadError);
      }
    } catch (e) {
      handleLoadError(e);
    }
    
    // Set a timeout in case the audio never loads
    const timeoutId = setTimeout(() => {
      if (loading) {
        console.warn('Audio loading timed out');
        setLoading(false);
        audio.removeEventListener('canplay', handleCanPlay);
        audio.removeEventListener('error', handleLoadError);
      }
    }, 10000); // 10 seconds timeout
    
    // Cleanup function
    return () => {
      clearTimeout(timeoutId);
      audio.removeEventListener('canplay', handleCanPlay);
      audio.removeEventListener('error', handleLoadError);
    };
  }, [audioUrl]);

  return (
    <div className="mb-4 bg-slate-800/50 rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <h4 className="text-cyan-400 font-medium flex items-center space-x-2">
          <FileAudio className="w-5 h-5" />
          <span>Audio</span>
        </h4>
        {onDownloadCertificate && (
          <button
            onClick={onDownloadCertificate}
            className="flex items-center space-x-1 px-3 py-1.5 text-sm rounded-lg bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30 transition-colors"
            title="Descargar certificado"
          >
            <FileText className="w-4 h-4" />
            <span>Certificado</span>
          </button>
        )}
      </div>

      {loading ? (
        <div className="flex items-center justify-center p-4">
          <RefreshCw className="w-5 h-5 animate-spin text-cyan-400 mr-2" />
          <span className="text-slate-400">Cargando audio…</span>
        </div>
      ) : error ? (
        <div className="text-center py-4 text-orange-400">
          {error}
        </div>
      ) : (
        <div className="flex items-center space-x-4">
          <button
            onClick={togglePlayPause}
            className={`p-2 rounded-full transition-all duration-200 ${
              loading 
                ? 'bg-slate-700 text-slate-500 cursor-not-allowed' 
                : isPlaying 
                  ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30' 
                  : 'bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30 hover:scale-105'
            }`}
            aria-label={isPlaying ? 'Pausar' : 'Reproducir'}
            disabled={!audioUrl || loading}
          >
            {loading ? (
              <RefreshCw className="w-5 h-5 animate-spin" />
            ) : isPlaying ? (
              <Pause className="w-5 h-5" />
            ) : (
              <Play className="w-5 h-5" />
            )}
          </button>
          <div className="flex-1 min-w-0">
            <audio 
              ref={audioRef} 
              src={audioUrl} 
              className="w-full"
              preload="metadata"
            />
            {fileName && (
              <div className="text-xs text-slate-400 mt-1 truncate" title={fileName}>
                {fileName}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AudioPlayer;
