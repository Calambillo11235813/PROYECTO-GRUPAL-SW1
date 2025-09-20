import React from 'react';

const FileAnalysisResults = ({ result, modelName = "Modelo" }) => {
  if (!result || !result.success) {
    return (
      <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-4">
        <div className="text-cyber-error">
          ❌ Error: {result?.error || 'Error desconocido'}
        </div>
      </div>
    );
  }

  const { data } = result;
  const isAI = data.resultado === 'IA';
  const confidence = data.probabilidad_ia || 0;

  return (
    <div className="bg-cyber-bg-card border border-cyber-border-primary/30 rounded-lg p-6">
      <h3 className="text-lg font-bold text-white mb-4 flex items-center">
        📄 Resultado del Análisis de Archivo - {modelName}
      </h3>
      <div className="mb-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-cyber-text-secondary">Predicción:</span>
          <span className={`font-bold text-lg ${isAI ? 'text-cyber-error' : 'text-cyber-success'}`}>
            {isAI ? '🤖 Generado por IA' : '👤 Escrito por Humano'}
          </span>
        </div>
        <div className="text-sm text-cyber-text-secondary mb-2">
          <strong>Archivo:</strong> {data.archivo_info?.nombre} <br />
          <strong>Tamaño:</strong> {data.archivo_info?.tamano} bytes <br />
          <strong>Tipo:</strong> {data.archivo_info?.tipo}
        </div>
        <div className="bg-cyber-bg-secondary/50 rounded-lg p-4 mb-2">
          <strong>Texto extraído:</strong>
          <div className="text-xs text-cyber-text-muted mt-2 max-h-40 overflow-y-auto">
            {data.texto_extraido || 'No se extrajo texto del archivo.'}
          </div>
        </div>
        <div className="flex justify-between">
          <span style={{ color: '#ff3b3b', fontWeight: 'bold' }}>
            Confianza IA: {Math.round(confidence)}%
          </span>
          <span style={{ color: '#00e676', fontWeight: 'bold' }}>
            Confianza Humano: {Math.round(data.probabilidad_humano || 0)}%
          </span>
        </div>
      </div>
      <div className="text-xs text-cyber-text-muted text-center pt-3 border-t border-cyber-border-secondary/30 mt-4">
        Análisis completado el {data.fecha_analisis ? new Date(data.fecha_analisis).toLocaleString() : new Date().toLocaleString()}
      </div>
    </div>
  );
};

export default FileAnalysisResults;