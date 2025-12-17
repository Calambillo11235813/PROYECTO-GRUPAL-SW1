import React from 'react';
import { AlertCircle, CheckCircle } from 'lucide-react';

// Tarjeta para mostrar resultado de análisis
export default function VideoResultCard({ result }) {
  const { id, video, score, verdict, created_at } = result;
  const scorePct = Math.round((Number(score) || 0) * 100);
  const isDeepfake = verdict === 'DEEPFAKE';

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
      </div>
    </div>
  );
}
