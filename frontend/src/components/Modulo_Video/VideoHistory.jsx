import React, { useEffect, useState } from 'react';
import VideoService from '../../services/VideoService';
import VideoResultCard from './VideoResultCard';

// Historial de análisis de videos (HU-14)
export default function VideoHistory() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    VideoService.listAnalyses()
      .then((res) => {
        if (mounted) setResults(res.data);
      })
      .catch(() => {})
      .finally(() => mounted && setLoading(false));
    return () => (mounted = false);
  }, []);

  return (
    <div className="max-w-full">
      <div className="bg-slate-900 p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-semibold text-cyan-400 mb-2">Historial de Análisis</h2>
        <p className="text-slate-400 mb-4">Consulta los últimos resultados de detección de deepfakes</p>
        {loading && <p className="text-slate-400">Cargando...</p>}
        {!loading && results.length === 0 && <p className="text-slate-400">No hay resultados aún.</p>}
        <div className="space-y-3">
          {results.map((r) => (
            <VideoResultCard key={r.id} result={r} />
          ))}
        </div>
      </div>
    </div>
  );
}
