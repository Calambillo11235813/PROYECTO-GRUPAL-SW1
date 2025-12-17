import React, { useState } from 'react';
import textAnalysisService from '../../../services/textAnalysisService';
import TextInput from './TextInput';
import AnalysisResults from './AnalysisResults';
import Button from '../../ui/Button'; // Cambiado: eliminé las llaves { }

const TextAnalyzer = ({ onAnalysisComplete, modelo = 'B' }) => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Por favor ingresa un texto para analizar');
      return;
    }

    setError('');
    setIsAnalyzing(true);
    setResult(null);

    try {
      console.log('🔍 Iniciando análisis de texto...');
      const analysisResult = await textAnalysisService.analyzeText(text, modelo);
      
      if (analysisResult.success) {
        setResult(analysisResult);
        onAnalysisComplete?.(analysisResult); // Callback al parent
      } else {
        setError(analysisResult.error || 'Error en el análisis');
      }
    } catch (err) {
      console.error('❌ Error en análisis:', err);
      setError('Error de conexión con el servidor');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const clearAnalysis = () => {
    setResult(null);
    setError('');
  };

  return (
    <div className="space-y-16">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent mb-2">
          Análisis de Texto IA
        </h2>
        <p className="text-cyber-text-secondary">
          Ingresa el texto que deseas analizar para detectar si fue generado por IA
        </p>
      </div>

      {/* Error Message */}
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

      {/* Text Input */}
      <TextInput
        value={text}
        onChange={setText}
        placeholder="Escribe o pega aquí el texto que quieres analizar..."
        disabled={isAnalyzing}
      
      />

      {/* Action Buttons */}
      <div className="flex space-x-4">
        <Button 
          onClick={handleAnalyze}
          loading={isAnalyzing}
          disabled={!text.trim() || isAnalyzing}
          className="flex-1"
        >
          🔍 Analizar Texto 
        </Button>
        
        {result && (
          <Button 
            onClick={clearAnalysis}
            variant="ghost"
            className="px-4"
          >
            🗑️ Limpiar
          </Button>
        )}
      </div>

      {/* Results */}
      {result && (
        <AnalysisResults 
          result={result} 
          modelName={`Modelo ${modelo}`}
        />
      )}
    </div>
  );
};

export default TextAnalyzer;