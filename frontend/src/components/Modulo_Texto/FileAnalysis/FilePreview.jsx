import React, { useState, useEffect } from 'react';

const FilePreview = ({ file, extractedText = '', isLoading = false }) => {
  const [previewMode, setPreviewMode] = useState('info'); // 'info', 'text', 'raw'

  // Formatear tamaño de archivo
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Obtener información del archivo
  const getFileInfo = () => {
    if (!file) return null;

    return {
      name: file.name,
      size: formatFileSize(file.size),
      type: file.type,
      lastModified: new Date(file.lastModified).toLocaleString(),
      extension: file.name.split('.').pop().toUpperCase()
    };
  };

  // Obtener icono del archivo
  const getFileIcon = (fileType) => {
    if (fileType.includes('pdf')) return { icon: '📄', color: 'text-red-400', bg: 'bg-red-400/10' };
    if (fileType.includes('word') || fileType.includes('document')) return { icon: '📝', color: 'text-blue-400', bg: 'bg-blue-400/10' };
    if (fileType.includes('text')) return { icon: '📋', color: 'text-green-400', bg: 'bg-green-400/10' };
    return { icon: '📁', color: 'text-cyber-text-muted', bg: 'bg-cyber-bg-secondary/20' };
  };

  const fileInfo = getFileInfo();
  const fileIcon = file ? getFileIcon(file.type) : { icon: '📁', color: 'text-cyber-text-muted', bg: 'bg-cyber-bg-secondary/20' };

  if (!file) {
    return (
      <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-6 text-center">
        <div className="text-cyber-text-muted">
          <svg className="mx-auto h-12 w-12 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>No hay archivo seleccionado</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg overflow-hidden">
      {/* Header con información del archivo */}
      <div className="p-4 border-b border-cyber-border-secondary/30">
        <div className="flex items-center space-x-3">
          <div className={`w-12 h-12 rounded-lg flex items-center justify-center text-2xl ${fileIcon.bg}`}>
            <span>{fileIcon.icon}</span>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-white font-medium truncate">
              {fileInfo.name}
            </h3>
            <p className="text-sm text-cyber-text-muted">
              {fileInfo.size} • {fileInfo.extension}
            </p>
          </div>
        </div>
      </div>

      {/* Tabs de navegación */}
      <div className="flex border-b border-cyber-border-secondary/30">
        {[
          { id: 'info', label: 'Información', icon: 'ℹ️' },
          { id: 'text', label: 'Texto Extraído', icon: '📄' },
          { id: 'raw', label: 'Detalles Raw', icon: '🔧' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setPreviewMode(tab.id)}
            className={`
              flex-1 px-4 py-3 text-sm font-medium transition-all duration-200
              ${previewMode === tab.id
                ? 'bg-cyber-accent-primary/20 text-cyber-accent-primary border-b-2 border-cyber-accent-primary'
                : 'text-cyber-text-secondary hover:text-white hover:bg-cyber-bg-secondary/30'
              }
            `}
          >
            <span className="mr-2">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {/* Contenido según el tab seleccionado */}
      <div className="p-4 max-h-96 overflow-y-auto">
        
        {/* Tab: Información */}
        {previewMode === 'info' && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-cyber-text-accent mb-1">
                  Nombre del archivo
                </label>
                <div className="text-white bg-cyber-bg-secondary/30 rounded p-2 text-sm">
                  {fileInfo.name}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-cyber-text-accent mb-1">
                  Tamaño
                </label>
                <div className="text-white bg-cyber-bg-secondary/30 rounded p-2 text-sm">
                  {fileInfo.size}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-cyber-text-accent mb-1">
                  Tipo MIME
                </label>
                <div className="text-white bg-cyber-bg-secondary/30 rounded p-2 text-sm">
                  {fileInfo.type}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-cyber-text-accent mb-1">
                  Última modificación
                </label>
                <div className="text-white bg-cyber-bg-secondary/30 rounded p-2 text-sm">
                  {fileInfo.lastModified}
                </div>
              </div>
            </div>

            {/* Estado del procesamiento */}
            <div className="bg-cyber-bg-secondary/20 rounded-lg p-3 border border-cyber-border-secondary/30">
              <h4 className="text-cyber-text-accent font-medium mb-2">Estado del Procesamiento</h4>
              <div className="flex items-center space-x-2">
                {isLoading ? (
                  <>
                    <svg className="animate-spin h-4 w-4 text-cyber-accent-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span className="text-cyber-text-secondary text-sm">Extrayendo texto del archivo...</span>
                  </>
                ) : extractedText ? (
                  <>
                    <span className="text-cyber-success">✅</span>
                    <span className="text-cyber-success text-sm">Texto extraído correctamente</span>
                  </>
                ) : (
                  <>
                    <span className="text-cyber-text-muted">⏳</span>
                    <span className="text-cyber-text-muted text-sm">Esperando procesamiento</span>
                  </>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Tab: Texto Extraído */}
        {previewMode === 'text' && (
          <div>
            <div className="mb-3 flex items-center justify-between">
              <h4 className="text-cyber-text-accent font-medium">Contenido Extraído</h4>
              {extractedText && (
                <span className="text-xs text-cyber-text-muted">
                  {extractedText.length.toLocaleString()} caracteres
                </span>
              )}
            </div>
            
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <svg className="animate-spin h-8 w-8 text-cyber-accent-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span className="ml-2 text-cyber-text-secondary">Extrayendo texto...</span>
              </div>
            ) : extractedText ? (
              <div className="bg-cyber-bg-secondary/30 rounded-lg p-4 border border-cyber-border-secondary/30">
                <pre className="text-sm text-white whitespace-pre-wrap font-mono">
                  {extractedText}
                </pre>
              </div>
            ) : (
              <div className="text-center py-8 text-cyber-text-muted">
                <svg className="mx-auto h-12 w-12 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p>No hay texto extraído aún</p>
                <p className="text-xs mt-1">Procesa el archivo para ver su contenido</p>
              </div>
            )}
          </div>
        )}

        {/* Tab: Detalles Raw */}
        {previewMode === 'raw' && (
          <div>
            <h4 className="text-cyber-text-accent font-medium mb-3">Datos Raw del Archivo</h4>
            <div className="bg-cyber-bg-secondary/30 rounded-lg p-4 border border-cyber-border-secondary/30">
              <pre className="text-xs text-cyber-text-muted overflow-x-auto">
{JSON.stringify({
  name: file.name,
  size: file.size,
  type: file.type,
  lastModified: file.lastModified,
  lastModifiedDate: new Date(file.lastModified).toISOString(),
  webkitRelativePath: file.webkitRelativePath,
  extractedTextLength: extractedText ? extractedText.length : 0,
  extractedTextPreview: extractedText ? extractedText.substring(0, 100) + '...' : null
}, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FilePreview;