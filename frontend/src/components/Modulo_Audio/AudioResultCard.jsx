import React, { useEffect, useState, useRef } from 'react';
import { Upload, Volume2, Play, Pause, Download, Trash2, RefreshCw, AlertCircle, CheckCircle, Clock, FileAudio, Zap } from 'lucide-react';

// Componente AudioResultCard mejorado
const AudioResultCard = ({ result, onDownload, onDelete }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioSrc, setAudioSrc] = useState(result?.audio_url || null);
  const [loadingAudio, setLoadingAudio] = useState(false);
  const [audioError, setAudioError] = useState('');
  const [imageError, setImageError] = useState(false);
  const [fetchDetail, setFetchDetail] = useState(null);
  const audioRef = useRef(null);
  const localFileRef = useRef(null);

  // Mostrar el resultado en consola para depuración
  useEffect(() => {
    console.log('[AudioResultCard] result completo:', result);
    console.log('[AudioResultCard] audio_url raw:', result?.audio_url);
    console.log('[AudioResultCard] spectrogram_url:', result?.spectrogram_url);
  }, [result]);

  useEffect(() => {
    let objectUrl = null;
    let cancelled = false;

    const loadAudio = async () => {
      console.log('[AudioResultCard] loadAudio start ->', { audio_url: result?.audio_url });
      setAudioError('');
      setFetchDetail(null);

      if (!result?.audio_url || result.audio_url === '#') {
        console.warn('[AudioResultCard] audio_url inválido o placeholder (#). No se intentará fetch.');
        setAudioSrc(null);
        setAudioError('Audio no disponible (backend entregó placeholder "#").');
        setFetchDetail({ reason: 'placeholder' });
        return;
      }

      const extLooksLikeAudio = /\.(mp3|wav|ogg|m4a|webm)$/i.test(result.audio_url);
      if (extLooksLikeAudio) {
        console.log('[AudioResultCard] audio_url parece archivo de audio por extensión. Usando directamente.');
        setAudioSrc(result.audio_url);
        return;
      }

      try {
        setLoadingAudio(true);
        console.log('[AudioResultCard] fetching audio desde URL:', result.audio_url);
        const resp = await fetch(result.audio_url, { mode: 'cors' });
        console.log('[AudioResultCard] fetch response status:', resp.status);
        setFetchDetail({ status: resp.status, url: result.audio_url });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const contentType = (resp.headers.get('content-type') || '').toLowerCase();
        console.log('[AudioResultCard] fetch content-type:', contentType);
        if (!contentType.startsWith('audio')) {
          console.error('[AudioResultCard] contenido obtenido NO es audio según content-type:', contentType);
          throw new Error('Recurso no es audio (content-type=' + contentType + ')');
        }
        const blob = await resp.blob();
        console.log('[AudioResultCard] blob obtenido, size bytes:', blob.size, 'type:', blob.type);
        objectUrl = URL.createObjectURL(blob);
        console.log('[AudioResultCard] objectURL creado:', objectUrl);
        if (!cancelled) setAudioSrc(objectUrl);
      } catch (err) {
        console.error('[AudioResultCard] Audio load error:', err);
        setAudioSrc(null);
        setAudioError('No se puede reproducir el audio (CORS, 404 o formato incorrecto). ' + err.message);
        setFetchDetail({ error: err.message });
      } finally {
        setLoadingAudio(false);
      }
    };

    loadAudio();
    return () => {
      cancelled = true;
      if (objectUrl) {
        console.log('[AudioResultCard] revocando objectURL:', objectUrl);
        URL.revokeObjectURL(objectUrl);
      }
    };
  }, [result?.audio_url]);

  // Listeners para el elemento audio: play, pause, error, ended, timeupdate
  useEffect(() => {
    const audioEl = audioRef.current;
    if (!audioEl) return;
    const onPlay = () => {
      console.log('[AudioResultCard] audio play event');
      setIsPlaying(true);
    };
    const onPause = () => {
      console.log('[AudioResultCard] audio pause event');
      setIsPlaying(false);
    };
    const onError = (e) => {
      console.error('[AudioResultCard] audio element error:', e);
      setAudioError('Error reproductor: no se puede reproducir el audio en este navegador.');
    };
    const onEnded = () => {
      console.log('[AudioResultCard] audio ended');
      setIsPlaying(false);
    };

    audioEl.addEventListener('play', onPlay);
    audioEl.addEventListener('pause', onPause);
    audioEl.addEventListener('error', onError);
    audioEl.addEventListener('ended', onEnded);

    return () => {
      audioEl.removeEventListener('play', onPlay);
      audioEl.removeEventListener('pause', onPause);
      audioEl.removeEventListener('error', onError);
      audioEl.removeEventListener('ended', onEnded);
    };
  }, [audioSrc]);

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) audioRef.current.pause();
      else audioRef.current.play();
    }
  };

  // Retry manual fetch (usa el mismo flujo que loadAudio)
  const handleRetryFetch = () => {
    console.log('[AudioResultCard] retry fetch audio solicitado');
    // forzar re-ejecución del effect cambiando audio_url temporalmente:
    setAudioSrc(null);
    setTimeout(() => {
      // trigger effect: creating a new object by updating audioSrc from result (no-op but re-renders)
      setAudioSrc(result?.audio_url || null);
    }, 50);
  };

  // Permitir al usuario cargar un archivo local para reproducir (debug / fallback)
  const handleLocalFile = (e) => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    console.log('[AudioResultCard] archivo local seleccionado:', f.name, f.type, f.size);
    const url = URL.createObjectURL(f);
    setAudioSrc(url);
    setAudioError('');
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
        <div className="mb-4">
          {loadingAudio && <p className="text-sm text-slate-400">Cargando audio…</p>}
          {audioSrc ? (
            <audio ref={audioRef} controls src={audioSrc} className="w-full" />
          ) : (
            <div className="space-y-2">
              <p className="text-sm text-orange-400">{audioError || 'No hay audio para reproducir'}</p>

              {/* Mostrar detalle técnico para debugging */}
              {fetchDetail && (
                <pre className="text-xs text-slate-500 bg-slate-800 p-2 rounded">{JSON.stringify(fetchDetail, null, 2)}</pre>
              )}

              <div className="flex items-center space-x-2">
                {/* Retry solo si backend proporcionó alguna URL distinta de placeholder */}
                {result?.audio_url && result.audio_url !== '#' && (
                  <button onClick={handleRetryFetch} className="px-3 py-1 rounded bg-cyan-500 text-black text-sm">
                    Reintentar fetch
                  </button>
                )}
                {/* Input local para reproducir archivo manualmente */}
                <label className="px-3 py-1 rounded bg-slate-700 text-sm cursor-pointer">
                  Cargar audio local
                  <input ref={localFileRef} type="file" accept="audio/*" onChange={handleLocalFile} className="hidden" />
                </label>
              </div>
            </div>
          )}
        </div>

        {/* Espectrograma con fallback si la URL externa falla */}
        {result.spectrogram_url && (
          <div className="space-y-2">
            <h4 className="text-cyan-400 font-medium flex items-center space-x-2">
              <Volume2 className="w-4 h-4" />
              <span>Análisis Espectral</span>
            </h4>
            <div className="relative group/img">
              {!imageError ? (
                <img
                  src={result.spectrogram_url}
                  alt="Espectrograma"
                  onError={(e) => {
                    console.error('[AudioResultCard] spectrogram image load failed:', e);
                    setImageError(true);
                  }}
                  className="w-full rounded-xl border border-cyan-500/30 shadow-lg hover:shadow-cyan-500/20 transition-shadow duration-300"
                />
              ) : (
                <div className="w-full h-48 rounded-xl bg-gradient-to-r from-slate-800 to-slate-700 flex items-center justify-center text-slate-400">
                  <span>Espectrograma no disponible (fallback)</span>
                </div>
              )}
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