import React, { useState } from 'react';
import { AlertCircle, CheckCircle, Clock, ChevronDown, ChevronUp } from 'lucide-react';

// Tarjeta para mostrar resultado de análisis
export default function VideoResultCard({ result }) {
  const { id, video, score, verdict, created_at, details } = result;
  const scorePct = Math.round((Number(score) || 0) * 100);
  const isDeepfake = verdict === 'DEEPFAKE';
  const [showTimestamps, setShowTimestamps] = useState(false);
  
  // Extraer frames sospechosos de los detalles
  const suspiciousFrames = details?.suspicious_frames || [];
  const hasSuspiciousFrames = isDeepfake && suspiciousFrames.length > 0;

  return (
    <div className="bg-slate-900/50 p-6 rounded-lg backdrop-blur-sm border border-slate-700/50">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          {isDeepfake ? (
            <AlertCircle className="w-8 h-8 text-orange-400" />
          ) : (
            <CheckCircle className="w-8 h-8 text-green-400" />
          )}
          <div>
            <h4 className="text-xl font-bold text-cyan-300">Resultado del Análisis</h4>
            <p className="text-xs text-slate-400">{new Date(created_at).toLocaleString()}</p>
          </div>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${isDeepfake ? 'text-orange-400' : 'text-green-400'}`}>
            {verdict}
          </div>
        </div>
      </div>
      
      <div className="space-y-3">
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-slate-300 font-medium">Puntuación de confianza</span>
            <span className="text-sm font-bold text-slate-200">{scorePct}%</span>
          </div>
          <div className="w-full bg-slate-700 h-3 rounded-full overflow-hidden">
            <div 
              className={`h-3 transition-all duration-500 ${
                isDeepfake 
                  ? 'bg-gradient-to-r from-orange-500 via-red-500 to-pink-500' 
                  : 'bg-gradient-to-r from-green-500 via-cyan-500 to-blue-500'
              }`} 
              style={{ width: `${scorePct}%` }} 
            />
          </div>
        </div>

        <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700/30">
          <h5 className="text-sm font-semibold text-cyan-300 mb-2">¿Qué significa este resultado?</h5>
          <p className="text-xs text-slate-300 leading-relaxed">
            {isDeepfake ? (
              <>
                <span className="font-semibold text-orange-400">Score alto ({scorePct}%):</span> El modelo detectó que este video tiene una alta probabilidad de ser un deepfake. 
                Esto indica que se encontraron patrones sospechosos en las características faciales, movimientos o inconsistencias visuales típicas de contenido manipulado por IA.
              </>
            ) : (
              <>
                <span className="font-semibold text-green-400">Score bajo ({scorePct}%):</span> El modelo considera que este video es auténtico. 
                Las características faciales, movimientos y patrones visuales analizados son consistentes con un video real sin manipulación aparente por inteligencia artificial.
              </>
            )}
          </p>
        </div>

        {/* Sección de marcas de tiempo sospechosas */}
        {hasSuspiciousFrames && (
          <div className="bg-red-900/20 border border-red-500/30 rounded-lg overflow-hidden">
            <button
              onClick={() => setShowTimestamps(!showTimestamps)}
              className="w-full flex items-center justify-between p-4 hover:bg-red-900/30 transition-colors"
            >
              <div className="flex items-center gap-3">
                <Clock className="w-5 h-5 text-red-400" />
                <div className="text-left">
                  <h5 className="text-sm font-semibold text-red-300">
                    Momentos Sospechosos Detectados
                  </h5>
                  <p className="text-xs text-slate-400">
                    {suspiciousFrames.length} frame{suspiciousFrames.length !== 1 ? 's' : ''} con anomalías
                  </p>
                </div>
              </div>
              {showTimestamps ? (
                <ChevronUp className="w-5 h-5 text-slate-400" />
              ) : (
                <ChevronDown className="w-5 h-5 text-slate-400" />
              )}
            </button>

            {showTimestamps && (
              <div className="p-4 pt-0 space-y-2 max-h-64 overflow-y-auto">
                <div className="text-xs text-slate-400 mb-3">
                  Los siguientes momentos del video presentan características sospechosas de manipulación:
                </div>
                {suspiciousFrames.map((frame, idx) => (
                  <div 
                    key={idx}
                    className="flex items-center justify-between bg-slate-800/70 p-3 rounded-lg border border-red-500/20"
                  >
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-red-400" />
                        <span className="text-sm font-mono text-red-300 font-semibold">
                          {frame.timestamp_formatted}
                        </span>
                      </div>
                      <span className="text-xs text-slate-400">
                        Frame #{frame.frame_number}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-slate-400">Confianza:</span>
                      <span className="text-sm font-semibold text-orange-400">
                        {Math.round(frame.score * 100)}%
                      </span>
                    </div>
                  </div>
                ))}
                <div className="mt-4 p-3 bg-slate-800/50 rounded border border-slate-700/50">
                  <p className="text-xs text-slate-400 leading-relaxed">
                    💡 <span className="font-semibold text-cyan-300">Tip:</span> Revisa estos momentos específicos 
                    del video para identificar las anomalías detectadas por el modelo de IA.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
