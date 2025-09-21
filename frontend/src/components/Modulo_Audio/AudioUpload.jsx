import React, { useState, useRef } from 'react';
import { FileAudio, Upload, RefreshCw, Zap, Trash2, AlertCircle } from 'lucide-react';

const AudioUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef(null);

  // Evita "flicker" de drag cuando se entra/sale sobre elementos hijos
  const dragCounter = useRef(0);

  const handleFileChange = (selectedFile) => {
    if (selectedFile) {
      // Validar tipo de archivo
      const validTypes = ['audio/mp3', 'audio/wav', 'audio/ogg', 'audio/m4a', 'audio/webm'];
      if (!validTypes.includes(selectedFile.type) && !selectedFile.name.match(/\.(mp3|wav|ogg|m4a|webm)$/i)) {
        setError('Formato de archivo no compatible. Use MP3, WAV, OGG, M4A o WEBM.');
        return;
      }
      
      // Validar tamaño (max 50MB)
      if (selectedFile.size > 50 * 1024 * 1024) {
        setError('El archivo es demasiado grande. Máximo 50MB.');
        return;
      }

      setFile(selectedFile);
      setError('');
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current += 1;
    // marcar visualmente que estamos en zona válida
    setDragOver(true);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current = 0;
    setDragOver(false);
    const droppedFile = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    if (!droppedFile) {
      setError('No se detectó archivo al soltar. Intenta arrastrar desde el explorador/desktop.');
      return;
    }
    handleFileChange(droppedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    // importante indicar al navegador que queremos permitir drop
    if (e.dataTransfer) e.dataTransfer.dropEffect = 'copy';
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    // decrementa contador para evitar que salir sobre hijos quite el estado
    dragCounter.current -= 1;
    if (dragCounter.current <= 0) {
      dragCounter.current = 0;
      setDragOver(false);
    }
  };

  const simulateProgress = () => {
    setProgress(0);
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 95) {
          clearInterval(interval);
          return 95;
        }
        return prev + Math.random() * 15;
      });
    }, 200);
    return interval;
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Selecciona un archivo de audio');
      return;
    }
    
    setLoading(true);
    setError('');
    const progressInterval = simulateProgress();
    
    try {
      // Simular delay para mostrar progreso
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const token = localStorage.getItem('access');
      // await uploadAudio(file, token);
      
      clearInterval(progressInterval);
      setProgress(100);
      
      setTimeout(() => {
        setLoading(false);
        setFile(null);
        setProgress(0);
        onUploadSuccess && onUploadSuccess();
      }, 500);
      
    } catch (err) {
      clearInterval(progressInterval);
      setError('Error al analizar el audio. Inténtalo de nuevo.');
      setLoading(false);
      setProgress(0);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
          Análisis de Audio IA
        </h2>
        <p className="text-slate-400">
          Detecta si tu audio fue generado por Inteligencia Artificial
        </p>
      </div>

      {/* Zona de drop */}
      <div
        className={`relative group border-2 border-dashed rounded-2xl p-8 transition-all duration-300 cursor-pointer
          ${dragOver 
            ? 'border-cyan-400 bg-cyan-500/10 shadow-lg shadow-cyan-500/20' 
            : file 
            ? 'border-green-500/50 bg-green-500/5' 
            : 'border-slate-600 hover:border-cyan-500/50 bg-slate-800/30'
          }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*,.mp3,.wav,.ogg,.m4a,.webm"
          className="hidden"
          onChange={(e) => handleFileChange(e.target.files && e.target.files[0])}
          disabled={loading}
        />

        <div className="text-center space-y-4">
          {file ? (
            <>
              <div className="p-4 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 w-16 h-16 mx-auto flex items-center justify-center">
                <FileAudio className="w-8 h-8 text-white" />
              </div>
              <div>
                <div className="text-lg font-medium text-green-400">{file.name}</div>
                <div className="text-sm text-slate-400 mt-1">
                  {formatFileSize(file.size)} • {file.type}
                </div>
              </div>
            </>
          ) : (
            <>
              <div className={`p-4 rounded-full w-16 h-16 mx-auto flex items-center justify-center transition-all duration-300
                ${dragOver 
                  ? 'bg-gradient-to-r from-cyan-500 to-purple-500 shadow-lg' 
                  : 'bg-slate-700 group-hover:bg-gradient-to-r group-hover:from-cyan-500/80 group-hover:to-purple-500/80'
                }`}>
                <Upload className="w-8 h-8 text-white" />
              </div>
              <div>
                <div className="text-xl font-medium text-slate-300 mb-2">
                  {dragOver ? 'Suelta tu archivo aquí' : 'Arrastra tu audio o haz clic'}
                </div>
                <div className="text-sm text-slate-500">
                  Soportamos MP3, WAV, OGG, M4A, WEBM (máx. 50MB)
                </div>
              </div>
            </>
          )}
        </div>

        {/* Efecto de glow */}
        {dragOver && (
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 via-purple-500/20 to-pink-500/20 rounded-2xl animate-pulse" />
        )}
      </div>

      {/* Barra de progreso */}
      {loading && (
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-slate-400">
            <span>Analizando audio...</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {/* Botón de análisis */}
      <div className="flex space-x-4">
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className={`flex-1 flex items-center justify-center space-x-2 py-3 px-6 rounded-xl font-medium transition-all duration-200 transform
            ${!file || loading
              ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-400 hover:to-purple-400 text-white shadow-lg hover:shadow-cyan-500/25 hover:scale-105'
            }`}
        >
          {loading ? (
            <>
              <RefreshCw className="w-5 h-5 animate-spin" />
              <span>Analizando...</span>
            </>
          ) : (
            <>
              <Zap className="w-5 h-5" />
              <span>Analizar Audio</span>
            </>
          )}
        </button>

        {file && !loading && (
          <button
            onClick={() => {
              setFile(null);
              setError('');
            }}
            className="px-4 py-3 rounded-xl bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white transition-all duration-200"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center space-x-2 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
export default AudioUpload;