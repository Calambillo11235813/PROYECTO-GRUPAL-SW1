import React, { useState } from 'react';
import textAnalysisService from '../../../services/textAnalysisService';
import TextInput from '../TextAnalyzer/TextInput';
import ModelCard from './ModelCard';
import ComparisonChart from './ComparisonChart';

const ModelComparison = ({ onComparisonComplete }) => {
  const [text, setText] = useState('');
  const [comparison, setComparison] = useState(null);
  const [isComparing, setIsComparing] = useState(false);
  const [error, setError] = useState('');
  const [viewMode, setViewMode] = useState('cards'); // 'cards', 'chart', 'both'

  // Manejar comparación
  const handleCompare = async () => {
    if (!text.trim()) {
      setError('Por favor ingresa un texto para comparar');
      return;
    }

    setError('');
    setIsComparing(true);
    setComparison(null);

    try {
      console.log('⚖️ Iniciando comparación de modelos...');
      const result = await textAnalysisService.compareModels(text);
      
      if (result.success) {
        setComparison(result);
        onComparisonComplete?.(result);
        console.log('✅ Comparación completada:', result);
      } else {
        setError(result.error || 'Error en la comparación');
      }
    } catch (err) {
      console.error('❌ Error en comparación:', err);
      setError('Error de conexión con el servidor');
    } finally {
      setIsComparing(false);
    }
  };

  // Limpiar comparación
  const clearComparison = () => {
    setComparison(null);
    setError('');
  };

  // Limpiar error
  const clearError = () => {
    setError('');
  };

  // Determinar si hay consenso
  const hasConsensus = comparison?.data?.modelo_b?.prediccion === comparison?.data?.modelo_n?.prediccion;
  
  // Modelo ganador (mayor confianza)
  const getWinnerModel = () => {
    if (!comparison?.data?.modelo_b || !comparison?.data?.modelo_n) return null;
    
    const modelBConfidence = Math.max(
      comparison.data.modelo_b.probabilidad_ia || 0,
      comparison.data.modelo_b.probabilidad_humano || 0
    );
    
    const modelNConfidence = Math.max(
      comparison.data.modelo_n.probabilidad_ia || 0,
      comparison.data.modelo_n.probabilidad_humano || 0
    );
    
    return modelBConfidence > modelNConfidence ? 'B' : 'N';
  };

  const winnerModel = getWinnerModel();

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white mb-2">
          Comparación de Modelos de IA
        </h2>
        <p className="text-cyber-text-secondary">
          Compara los resultados de ambos modelos de detección de IA para obtener una perspectiva más completa
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-cyber-error/10 border border-cyber-error/30 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-cyber-error mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <span className="text-cyber-error text-sm">{error}</span>
            </div>
            <button onClick={clearError} className="text-cyber-error hover:text-cyber-error/80">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Text Input */}
      <TextInput
        value={text}
        onChange={setText}
        placeholder="Texto para comparar entre modelos..."
        disabled={isComparing}
      />

      {/* Action Buttons */}
      <div className="flex space-x-4">
        <button 
          onClick={handleCompare}
          disabled={!text.trim() || isComparing}
          className={`
            flex-1 flex items-center justify-center px-4 py-2 rounded-lg font-medium transition-all duration-300
            ${!text.trim() || isComparing
              ? 'bg-cyber-bg-secondary text-cyber-text-muted cursor-not-allowed'
              : 'bg-cyber-button text-white hover:bg-cyber-button-hover shadow-cyber-glow'
            }
          `}
        >
          {isComparing ? (
            <>
              <svg className="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Comparando...
            </>
          ) : (
            <>⚖️ Comparar Modelos</>
          )}
        </button>
        
        {comparison && (
          <button 
            onClick={clearComparison}
            className="px-6 py-2 rounded-lg font-medium bg-cyber-bg-secondary text-cyber-text-secondary hover:text-white hover:bg-cyber-bg-primary/50 transition-all duration-300"
          >
            🗑️ Limpiar
          </button>
        )}
      </div>

      {/* Results Section */}
      {comparison && comparison.success && (
        <div className="space-y-6">
          
          {/* View Mode Toggle */}
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-white">
              📊 Resultados de la Comparación
            </h3>
            
            <div className="flex space-x-1 bg-cyber-bg-secondary/80 p-1 rounded-lg border border-cyber-border-primary/40">
              {[
                {
                  id: 'cards',
                  label: 'Tarjetas',
                  icon: '📊'
                },
                {
                  id: 'chart',
                  label: 'Gráfico',
                  icon: '📈'
                },
                {
                  id: 'both',
                  label: 'Ambos',
                  icon: '🔬'
                }
              ].map((mode) => (
                <button
                  key={mode.id}
                  onClick={() => setViewMode(mode.id)}
                  className={`
                    px-3 py-1 rounded text-sm font-medium transition-all duration-200
                    ${viewMode === mode.id 
                      ? 'bg-cyber-button text-white shadow-cyber-glow' 
                      : 'text-cyber-text-secondary hover:text-white hover:bg-cyber-bg-primary/50'
                    }
                  `}
                >
                  <span className="mr-1">{mode.icon}</span>
                  {mode.label}
                </button>
              ))}
            </div>
          </div>

          {/* Summary */}
          <div className={`
            p-4 rounded-lg border text-center
            ${hasConsensus 
              ? 'bg-cyber-success/10 border-cyber-success/30' 
              : 'bg-yellow-400/10 border-yellow-400/30'
            }
          `}>
            <div className="flex items-center justify-center space-x-2 mb-2">
              <span className="text-2xl">
                {hasConsensus ? '🎯' : '⚖️'}
              </span>
              <div>
                <div className={`font-bold ${
                  hasConsensus ? 'text-cyber-success' : 'text-yellow-400'
                }`}>
                  {hasConsensus ? 'CONSENSO ALCANZADO' : 'RESULTADOS DIVERGENTES'}
                </div>
                <div className="text-sm text-cyber-text-secondary">
                  {hasConsensus 
                    ? `Ambos modelos coinciden: ${comparison.data.modelo_b.prediccion}` 
                    : `Modelo B: ${comparison.data.modelo_b.prediccion} • Modelo N: ${comparison.data.modelo_n.prediccion}`
                  }
                  {winnerModel && (
                    <span className="ml-2 text-xs">
                      (Mayor confianza: Modelo {winnerModel})
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Model Cards View */}
          {(viewMode === 'cards' || viewMode === 'both') && (
            <div className="grid md:grid-cols-2 gap-6">
              <ModelCard
                modelName="Modelo B"
                modelDescription="Sensible - Detecta patrones sutiles de IA"
                result={comparison.data.modelo_b}
                color="cyan"
                isHighlighted={winnerModel === 'B'}
              />
              
              <ModelCard
                modelName="Modelo N"
                modelDescription="Conservador - Análisis más preciso"
                result={comparison.data.modelo_n}
                color="purple"
                isHighlighted={winnerModel === 'N'}
              />
            </div>
          )}

          {/* Chart View */}
          {(viewMode === 'chart' || viewMode === 'both') && (
            <ComparisonChart
              modelBResult={comparison.data.modelo_b}
              modelNResult={comparison.data.modelo_n}
              showDetails={true}
            />
          )}

          {/* Recommendations */}
          <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-6">
            <h4 className="text-lg font-bold text-white mb-4 flex items-center">
              💡 Recomendaciones
            </h4>
            
            <div className="space-y-3 text-sm">
              {hasConsensus ? (
                <div className="flex items-start space-x-3">
                  <span className="text-cyber-success mt-0.5">✅</span>
                  <div>
                    <div className="text-white font-medium">Resultado Confiable</div>
                    <div className="text-cyber-text-secondary">
                      Ambos modelos están de acuerdo. El resultado tiene alta confiabilidad.
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex items-start space-x-3">
                  <span className="text-yellow-400 mt-0.5">⚠️</span>
                  <div>
                    <div className="text-white font-medium">Revisión Recomendada</div>
                    <div className="text-cyber-text-secondary">
                      Los modelos no coinciden. Se sugiere análisis manual adicional.
                    </div>
                  </div>
                </div>
              )}
              
              <div className="flex items-start space-x-3">
                <span className="text-cyber-accent-primary mt-0.5">🔍</span>
                <div>
                  <div className="text-white font-medium">Análisis Complementario</div>
                  <div className="text-cyber-text-secondary">
                    Considera factores como longitud del texto, complejidad y contexto.
                  </div>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <span className="text-cyber-text-accent mt-0.5">📊</span>
                <div>
                  <div className="text-white font-medium">Interpretación de Probabilidades</div>
                  <div className="text-cyber-text-secondary">
                    {/* ✅ CORREGIDO: Escapar caracteres especiales */}
                    Valores &gt; 70% indican alta confianza. Valores 40-70% requieren precaución.
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Timestamp */}
          <div className="text-xs text-cyber-text-muted text-center">
            Comparación realizada el {new Date().toLocaleString()}
          </div>
        </div>
      )}
    </div>
  );
};

export default ModelComparison;