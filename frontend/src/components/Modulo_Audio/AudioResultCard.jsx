import React, { useEffect, useState, useRef } from 'react';
import { Volume2, Download, Trash2, Zap } from 'lucide-react';
import AudioPlayer from './AudioPlayer';
import { API_ENDPOINTS } from '../../services/config';

const AudioResultCard = ({ result, onDownload, onDelete }) => {
  const [audioSrc, setAudioSrc] = useState('');
  const [loadingAudio, setLoadingAudio] = useState(true);
  const [audioError, setAudioError] = useState('');
  const [imageError, setImageError] = useState(false);
  const localFileRef = useRef(null);

  useEffect(() => {
    let cancelled = false;

    const loadAudio = async () => {
      if (!result?.audio_url || result.audio_url === '#') {
        setAudioSrc('');
        setAudioError('Audio no disponible');
        setLoadingAudio(false);
        return;
      }

      // Check if it's a direct audio file URL
      const extLooksLikeAudio = /\.(mp3|wav|ogg|m4a|webm)$/i.test(result.audio_url);
      if (extLooksLikeAudio) {
        setAudioSrc(result.audio_url);
        setLoadingAudio(false);
        return;
      }

      try {
        setLoadingAudio(true);
        const resp = await fetch(result.audio_url, {
          mode: 'cors',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (!resp.ok) throw new Error(`Error ${resp.status}`);

        const contentType = (resp.headers.get('content-type') || '').toLowerCase();
        if (!contentType.startsWith('audio')) {
          throw new Error('El recurso no es un archivo de audio');
        }

        const blob = await resp.blob();
        const objectUrl = URL.createObjectURL(blob);

        if (!cancelled) {
          setAudioSrc(objectUrl);
          setLoadingAudio(false);
        }
      } catch (err) {
        console.error('[AudioResultCard] loadAudio error:', err);
        if (!cancelled) {
          setAudioSrc('');
          setAudioError('No se pudo cargar el audio');
          setLoadingAudio(false);
        }
      }
    };

    loadAudio();
    return () => {
      cancelled = true;
    };
  }, [result?.audio_url]);


  // Retry manual fetch
  const handleRetryFetch = () => {
    setAudioSrc('');
    setLoadingAudio(true);
    setAudioError('');

    // Small delay to allow state to update
    setTimeout(() => {
      setAudioSrc(result?.audio_url || '');
    }, 100);
  };

  // Handle download certificate
  const handleDownloadCertificate = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.error('No authentication token found');
        return;
      }

      const response = await fetch(
        `${API_ENDPOINTS.AUDIO}/certificado/${result.id}/`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `certificado-audio-${result.id}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('[AudioResultCard] handleDownloadCertificate error:', error);
    }
  };

  // Permitir al usuario cargar un archivo local para reproducir (debug / fallback)
  const handleLocalFile = (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    const url = URL.createObjectURL(file);
    setAudioSrc(url);
    setAudioError('');
    setLoadingAudio(false);
  };

  const getConfidencePercentage = (confidence, isAI) => {
    // confidence ya viene normalizado a 0-100 desde Dashboard_Audio
    // Este valor representa la probabilidad de que sea IA
    
    console.log('getConfidencePercentage input:', { confidence, isAI });
    
    let finalConfidence;

    if (isAI) {
      // Si es IA, la confianza es directamente el valor de probabilidad
      finalConfidence = confidence;
    } else {
      // Si es Humano, la confianza es 100 - probabilidad_IA
      finalConfidence = 100 - confidence;
    }

    const result = Math.max(0, Math.min(100, Math.round(finalConfidence)));
    console.log('getConfidencePercentage output:', result);
    return result;
  };

  const finalConfidencePercentage = getConfidencePercentage(result.probabilidad, result.es_ia);

  // Obtener colores basados en el porcentaje
  const getConfidenceColor = (percent) => {
    if (percent >= 80) return 'text-green-400'; // Alta confianza
    if (percent >= 60) return 'text-yellow-400'; // Confianza media (ajustado de 50 a 60 para más rigor)
    return 'text-red-400'; // Baja confianza
  };

  // Obtener descripción de nivel de confianza
  const getConfidenceLevel = (percent) => {
    if (percent >= 80) return 'Alta confianza';
    if (percent >= 60) return 'Confianza media';
    return 'Baja confianza';
  };

  // Get result explanation based on confidence
  const getResultExplanation = (isAI, confidence) => {
    const confidencePercent = getConfidencePercentage(confidence);
    const confidenceText = ` (${confidencePercent}% de confianza)`;

    if (isAI) {
      if (confidencePercent >= 80) return 'Muy probablemente generado por IA' + confidenceText;
      if (confidencePercent >= 50) return 'Posiblemente generado por IA' + confidenceText;
      return 'Incierto - podría ser IA' + confidenceText;
    } else {
      if (confidencePercent >= 80) return 'Muy probablemente voz humana' + confidenceText;
      if (confidencePercent >= 50) return 'Posiblemente voz humana' + confidenceText;
      return 'Incierto - podría ser humano' + confidenceText;
    }
  };

  return (
    <div className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900/90 to-slate-800/90 border border-cyan-500/30 shadow-2xl backdrop-blur-sm hover:border-cyan-400/50 transition-all duration-300">
      {/* Efecto de glow animado */}
      <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 via-purple-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      <div className="relative p-6 space-y-4">
        {/* Header con icono animado */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500">
              <Zap className="w-5 h-5 text-white animate-pulse" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Resultado del Análisis
            </h3>
          </div>
        </div>

        {/* Resultado principal */}
        <div className="mb-6 text-center">
          <div className={`text-4xl font-bold mb-2 ${result.es_ia ? 'text-red-400' : 'text-green-400'
            }`}>
            {result.es_ia ? 'GENERADO POR IA' : 'VOZ HUMANA'}
          </div>
          <div className="text-slate-400">
            Nivel de confianza: <span className="font-medium">{getConfidencePercentage(result.probabilidad)}%</span>
          </div>

          {/* Barra de confianza visual */}
          <div className="space-y-2 mt-4 mb-6">
            <div className="flex justify-between text-sm text-slate-400 mb-1">
              <span>Nivel de confianza</span>
              <span>{getConfidencePercentage(result.probabilidad)}%</span>
            </div>
            <div className="w-full bg-slate-700/50 rounded-full h-3 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-1000 ease-out ${result.es_ia
                  ? 'bg-gradient-to-r from-yellow-400 to-red-500'
                  : 'bg-gradient-to-r from-yellow-400 to-green-500'
                  }`}
                style={{
                  width: `${getConfidencePercentage(result.probabilidad)}%`,
                  opacity: 0.3 + (getConfidencePercentage(result.probabilidad) / 100) * 0.7
                }}
              />
            </div>
            <div className="flex justify-between text-xs text-slate-500">
              <span>Baja</span>
              <span>Alta</span>
            </div>
          </div>
        </div>

        {/* Audio Player Component */}
        <div className="mb-4">
          <AudioPlayer
            audioUrl={audioSrc}
            fileName={result.original_filename}
            onDownloadCertificate={handleDownloadCertificate}
          />

          {!loadingAudio && !audioSrc && !audioError && (
            <div className="text-center py-4 text-slate-400">
              No hay audio disponible para reproducir
            </div>
          )}

          {audioError && (
            <div className="text-center py-2 text-orange-400 text-sm">
              {audioError}
            </div>
          )}
        </div>

        {/* Fallback for audio error */}
        {!loadingAudio && !audioSrc && (
          <div className="space-y-2">
            <p className="text-sm text-orange-400">{audioError || 'No hay audio para reproducir'}</p>


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

        {/* Mostrar explicación breve del resultado */}
        <div className="mt-3 text-sm text-slate-400">
          {getResultExplanation(result.es_ia, result.probabilidad)}
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