import React, { useState, useRef } from "react";
import { Upload, File, X, CheckCircle2, AlertCircle } from "lucide-react";
import codeAnalysisService from "../../../services/codeAnalysisService";

const CodeUploader = ({ onAnalysisComplete }) => {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const allowedExtensions = [
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".php",
    ".rb",
    ".go",
    ".rs",
    ".kt",
    ".swift",
  ];

  const validateFile = (file) => {
    const fileName = file.name.toLowerCase();
    const isValid = allowedExtensions.some((ext) => fileName.endsWith(ext));

    if (!isValid) {
      setError(
        `Archivo no soportado. Extensiones permitidas: ${allowedExtensions.join(
          ", "
        )}`
      );
      return false;
    }

    if (file.size > 5 * 1024 * 1024) {
      // 5MB
      setError("El archivo no debe superar los 5MB");
      return false;
    }

    return true;
  };

  const handleFileSelect = (selectedFile) => {
    setError(null);

    if (validateFile(selectedFile)) {
      setFile(selectedFile);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  };

  const handleFileInputChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError(null);

    try {
      const result = await codeAnalysisService.uploadCodeFile(file);
      onAnalysisComplete(result);
    } catch (err) {
      setError(err.message || "Error al subir el archivo");
    } finally {
      setIsUploading(false);
    }
  };

  const removeFile = () => {
    setFile(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !file && fileInputRef.current?.click()}
        className={`
          relative border-2 border-dashed rounded-xl p-8 transition-all duration-300 cursor-pointer
          ${
            isDragging
              ? "border-cyan-400 bg-cyan-500/10 scale-105"
              : "border-slate-600 bg-slate-800/50 hover:border-cyan-500/50 hover:bg-slate-800/70"
          }
          ${file ? "cursor-default" : "cursor-pointer"}
        `}
      >
        {!file ? (
          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-cyan-500 to-purple-500 flex items-center justify-center">
              <Upload className="w-10 h-10 text-white" />
            </div>
            <div className="text-center">
              <p className="text-lg font-semibold text-cyan-400 mb-2">
                Arrastra tu archivo de código aquí
              </p>
              <p className="text-sm text-slate-400">
                o haz clic para seleccionar
              </p>
              <p className="text-xs text-slate-500 mt-2">
                Soporta: {allowedExtensions.slice(0, 5).join(", ")}...
              </p>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-cyan-500 to-purple-500 flex items-center justify-center">
                <File className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="font-semibold text-slate-200">{file.name}</p>
                <p className="text-sm text-slate-400">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                removeFile();
              }}
              className="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-red-400" />
            </button>
          </div>
        )}

        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileInputChange}
          accept={allowedExtensions.join(",")}
          className="hidden"
        />
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 bg-red-500/10 border border-red-500/50 rounded-lg flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      {/* Upload Button */}
      {file && !error && (
        <button
          onClick={handleUpload}
          disabled={isUploading}
          className={`
            mt-6 w-full py-3 rounded-xl font-semibold transition-all duration-300
            ${
              isUploading
                ? "bg-slate-700 text-slate-400 cursor-not-allowed"
                : "bg-gradient-to-r from-cyan-500 to-purple-500 text-white hover:shadow-lg hover:shadow-cyan-500/50 hover:scale-105"
            }
          `}
        >
          {isUploading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
              <span>Analizando código...</span>
            </div>
          ) : (
            <div className="flex items-center justify-center space-x-2">
              <CheckCircle2 className="w-5 h-5" />
              <span>Analizar Código</span>
            </div>
          )}
        </button>
      )}
    </div>
  );
};

export default CodeUploader;
