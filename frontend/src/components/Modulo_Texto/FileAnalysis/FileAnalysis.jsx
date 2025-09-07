import React, { useState } from 'react';
import textAnalysisService from '../../../services/textAnalysisService';
import FileUploader from './FileUploader';
import FilePreview from './FilePreview';
import AnalysisResults from '../TextAnalyzer/AnalysisResults';
import { Button } from '../../ui/Button';

const FileAnalysis = ({ onAnalysisComplete, modelo = 'B' }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState(1); // 1: Upload, 2: Preview, 3: Analysis

  // Manejar selección de archivo
  const handleFileSelect = (file) => {
    console.log('📎 Archivo seleccionado:', file.name);
    setSelectedFile(file);
    setExtractedText('');
    setAnalysisResult(null);
    setError('');
    setStep(2);
    
    // Simular extracción de texto (en un caso real sería una llamada al backend)
    simulateTextExtraction(file);
  };

  // Remover archivo
  const handleFileRemove = () => {
    setSelectedFile(null);
    setExtractedText('');
    setAnalysisResult(null);
    setError('');
    setStep(1);
  };

  // Simular extracción de texto (reemplazar con llamada real al backend)
  const simulateTextExtraction = async (file) => {
    if (file.type === 'text/plain') {
      // Para archivos de texto, leer directamente
      setIsExtracting(true);
      try {
        const text = await file.text();
        setExtractedText(text);
        console.log('📄 Texto extraído de archivo TXT');
      } catch (err) {
        console.error('❌ Error leyendo archivo TXT:', err);
        setError('Error al leer el archivo de texto');
      } finally {
        setIsExtracting(false);
      }
    } else {
      // Para PDF y DOCX, simular procesamiento
      setIsExtracting(true);
      setTimeout(() => {
        const mockText = `Texto extraído del archivo: ${file.name}

Este es un ejemplo de texto que habría sido extraído del archivo ${file.type.includes('pdf') ? 'PDF' : 'Word'}. 

En una implementación real, aquí aparecería el contenido completo del documento procesado por el backend.

El archivo tiene un tamaño de ${(file.size / 1024).toFixed(1)} KB y fue modificado por última vez el ${new Date(file.lastModified).toLocaleDateString()}.

Este texto puede ser analizado por los modelos de IA para determinar si fue generado artificialmente o escrito por un humano.`;
        
        setExtractedText(mockText);
        setIsExtracting(false);
        console.log('📄 Texto extraído simulado');
      }, 2000);
    }
  };

  // Analizar archivo
  const handleAnalyzeFile = async () => {
    if (!selectedFile) {
      setError('No hay archivo seleccionado');
      return;
    }

    setError('');
    setIsAnalyzing(true);
    setAnalysisResult(null);

    try {
      console.log(`🔍 Analizando archivo con modelo ${modelo}:`, selectedFile.name);
      
      // Opción 1: Analizar archivo directamente
      const result = await textAnalysisService.analyzeFile(selectedFile, modelo);
      
      // Opción 2: Si el backend no soporta archivos, usar texto extraído
      // const result = await textAnalysisService.analyzeText(extractedText, modelo);
      
      if (result.success) {
        setAnalysisResult(result);
        setStep(3);
        onAnalysisComplete?.(result);
        console.log('✅ Análisis de archivo completado');
      } else {
        setError(result.error || 'Error en el análisis del archivo');
      }
    } catch (err) {
      console.error('❌ Error en análisis de archivo:', err);
      setError('Error de conexión con el servidor');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Analizar usando texto extraído (fallback)
  const handleAnalyzeExtractedText = async () => {
    if (!extractedText.trim()) {
      setError('No hay texto extraído para analizar');
      return;
    }

    setError('');
    setIsAnalyzing(true);
    setAnalysisResult(null);

    try {
      console.log(`🔍 Analizando texto extraído con modelo ${modelo}`);
      
      const result = await textAnalysisService.analyzeText(extractedText, modelo);
      
      if (result.success) {
        setAnalysisResult(result);
        setStep(3);
        onAnalysisComplete?.(result);
        console.log('✅ Análisis de texto extraído completado');
      } else {
        setError(result.error || 'Error en el análisis del texto');
      }
    } catch (err) {
      console.error('❌ Error en análisis de texto:', err);
      setError('Error de conexión con el servidor');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Reiniciar proceso
  const handleReset = () => {
    setSelectedFile(null);
    setExtractedText('');
    setAnalysisResult(null);
    setError('');
    setStep(1);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white mb-2">
          Análisis de Archivo
        </h2>
        <p className="text-cyber-text-secondary">
          Sube un archivo (PDF, DOCX, TXT) para extraer su contenido y analizar si fue generado por IA
        </p>
      </div>

      {/* Indicador de progreso */}
      <div className="flex items-center space-x-4 mb-6">
        {[
          { step: 1, label: 'Subir Archivo', icon: '📁' },
          { step: 2, label: 'Vista Previa', icon: '👀' },
          { step: 3, label: 'Análisis', icon: '🔍' }
        ].map((item) => (
          <div key={item.step} className="flex items-center">
            <div className={`
              flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium
              ${step >= item.step 
                ? 'bg-cyber-accent-primary text-white' 
                : 'bg-cyber-bg-secondary text-cyber-text-muted'
              }
            `}>
              {step > item.step ? '✓' : item.step}
            </div>
            <span className={`ml-2 text-sm ${
              step >= item.step ? 'text-white' : 'text-cyber-text-muted'
            }`}>
              {item.icon} {item.label}
            </span>
            {item.step < 3 && (
              <div className={`w-8 h-0.5 ml-4 ${
                step > item.step ? 'bg-cyber-accent-primary' : 'bg-cyber-bg-secondary'
              }`}></div>
            )}
          </div>
        ))}
      </div>

      {/* Mensaje de error global */}
      {error && (
        <div className="bg-cyber-error/10 border border-cyber-error/30 rounded-lg p-4">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-cyber-error mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-cyber-error text-sm">{error}</span>
          </div>
        </div>
      )}

      {/* Contenido según el paso */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Columna izquierda: Upload y controles */}
        <div className="space-y-6">
          {/* Paso 1: Upload de archivo */}
          <FileUploader
            onFileSelect={handleFileSelect}
            onFileRemove={handleFileRemove}
            selectedFile={selectedFile}
            disabled={isExtracting || isAnalyzing}
          />

          {/* Botones de acción */}
          {selectedFile && (
            <div className="space-y-3">
              <div className="flex space-x-3">
                <Button
                  onClick={handleAnalyzeFile}
                  loading={isAnalyzing}
                  disabled={!selectedFile || isAnalyzing || isExtracting}
                  className="flex-1"
                >
                  🔍 Analizar Archivo ({modelo})
                </Button>
                
                {extractedText && (
                  <Button
                    onClick={handleAnalyzeExtractedText}
                    loading={isAnalyzing}
                    disabled={!extractedText || isAnalyzing}
                    variant="secondary"
                    className="flex-1"
                  >
                    📄 Analizar Texto
                  </Button>
                )}
              </div>
              
              <Button
                onClick={handleReset}
                variant="ghost"
                disabled={isAnalyzing || isExtracting}
                className="w-full"
              >
                🔄 Reiniciar
              </Button>
            </div>
          )}
        </div>

        {/* Columna derecha: Preview */}
        <div>
          <FilePreview
            file={selectedFile}
            extractedText={extractedText}
            isLoading={isExtracting}
          />
        </div>
      </div>

      {/* Resultados del análisis */}
      {analysisResult && (
        <div className="mt-6">
          <AnalysisResults 
            result={analysisResult} 
            modelName={`Modelo ${modelo} - Archivo`}
          />
        </div>
      )}
    </div>
  );
};

export default FileAnalysis;