import React, { useState, useRef } from 'react';

const FileUploader = ({ 
  onFileSelect, 
  onFileRemove, 
  disabled = false, 
  selectedFile = null 
}) => {
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  // Configuración de archivos permitidos
  const allowedTypes = [
    'text/plain',
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword'
  ];

  const maxSize = 5 * 1024 * 1024; // 5MB

  // Validar archivo
  const validateFile = (file) => {
    if (!file) {
      setError('No se ha seleccionado ningún archivo');
      return false;
    }

    if (!allowedTypes.includes(file.type)) {
      setError('Tipo de archivo no válido. Solo se permiten: TXT, PDF, DOCX');
      return false;
    }

    if (file.size > maxSize) {
      setError(`El archivo es demasiado grande. Máximo ${(maxSize / 1024 / 1024).toFixed(1)}MB`);
      return false;
    }

    setError('');
    return true;
  };

  // Manejar selección de archivo
  const handleFileSelect = (file) => {
    if (validateFile(file)) {
      console.log('📎 Archivo seleccionado:', file.name);
      onFileSelect(file);
    }
  };

  // Manejar input de archivo
  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  // Manejar drag & drop
  const handleDragOver = (e) => {
    e.preventDefault();
    if (!disabled) {
      setDragOver(true);
    }
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);

    if (disabled) return;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  // Abrir selector de archivos
  const openFileSelector = () => {
    if (!disabled && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  // Remover archivo
  const handleRemoveFile = () => {
    setError('');
    onFileRemove();
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Formatear tamaño de archivo
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Obtener icono según tipo de archivo
  const getFileIcon = (fileType) => {
    if (fileType.includes('pdf')) return '📄';
    if (fileType.includes('word') || fileType.includes('document')) return '📝';
    if (fileType.includes('text')) return '📋';
    return '📁';
  };

  return (
    <div className="space-y-4">
      {/* Área de subida */}
      <div
        className={`
          relative border-2 border-dashed rounded-lg p-6 transition-all duration-300 cursor-pointer
          ${dragOver 
            ? 'border-cyber-accent-primary bg-cyber-accent-primary/10' 
            : 'border-cyber-border-primary/40 hover:border-cyber-accent-primary/60'
          }
          ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          ${selectedFile ? 'bg-cyber-bg-secondary/30' : 'bg-cyber-bg-secondary/10'}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={openFileSelector}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.doc,.txt"
          onChange={handleFileInputChange}
          disabled={disabled}
          className="hidden"
        />

        {!selectedFile ? (
          <div className="text-center">
            <div className="mb-4">
              <svg className="mx-auto h-12 w-12 text-cyber-text-muted" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <div className="text-white font-medium mb-2">
              {dragOver ? '📎 Suelta el archivo aquí' : '📁 Seleccionar archivo'}
            </div>
            <p className="text-sm text-cyber-text-muted mb-3">
              Arrastra y suelta o haz clic para seleccionar
            </p>
            <p className="text-xs text-cyber-text-muted">
              Formatos: PDF, DOCX, TXT • Máximo: {(maxSize / 1024 / 1024).toFixed(1)}MB
            </p>
          </div>
        ) : (
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="text-2xl">
                {getFileIcon(selectedFile.type)}
              </div>
              <div>
                <div className="text-white font-medium truncate max-w-xs">
                  {selectedFile.name}
                </div>
                <div className="text-sm text-cyber-text-muted">
                  {formatFileSize(selectedFile.size)} • {selectedFile.type.split('/')[1].toUpperCase()}
                </div>
              </div>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleRemoveFile();
              }}
              disabled={disabled}
              className="text-cyber-error hover:text-cyber-error/80 transition-colors p-1"
              title="Remover archivo"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        )}
      </div>

      {/* Mensaje de error */}
      {error && (
        <div className="bg-cyber-error/10 border border-cyber-error/30 rounded-lg p-3">
          <div className="flex items-center">
            <svg className="w-4 h-4 text-cyber-error mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-cyber-error text-sm">{error}</span>
          </div>
        </div>
      )}

      {/* Información adicional */}
      <div className="bg-cyber-bg-secondary/20 rounded-lg p-3 border border-cyber-border-secondary/30">
        <div className="text-xs text-cyber-text-muted space-y-1">
          <div className="flex items-center">
            <span className="mr-2">✅</span>
            <span>Formatos soportados: PDF, Microsoft Word (.docx), Texto plano (.txt)</span>
          </div>
          <div className="flex items-center">
            <span className="mr-2">📏</span>
            <span>Tamaño máximo: {(maxSize / 1024 / 1024).toFixed(1)}MB por archivo</span>
          </div>
          <div className="flex items-center">
            <span className="mr-2">🔒</span>
            <span>Los archivos se procesan de forma segura y no se almacenan</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUploader;