import React, { useEffect, useMemo, useState } from 'react';
import { History, Filter, Download, Search, ChevronDown, X, Video, Gauge, Trash2, AlertTriangle } from 'lucide-react';
import VideoService from '../../services/VideoService';

export default function VideoHistoryFull() {
  const [allResults, setAllResults] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    verdict: '', // 'DEEPFAKE' | 'REAL'
    model: '',
    start: '',
    end: '',
    minScore: '',
  });

  useEffect(() => {
    let active = true;
    const load = async () => {
      setLoading(true);
      try {
        const res = await VideoService.listAnalyses();
        if (active) {
          const data = Array.isArray(res.data) ? res.data : [];
          // Ordenar desc por fecha
          data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
          setAllResults(data);
          setFiltered(data);
        }
      } catch (e) {
        console.error('Error cargando historial de video:', e);
      } finally {
        active && setLoading(false);
      }
    };
    load();
    return () => { active = false; };
  }, []);

  const applyFilters = () => {
    const s = (filters.model || '').trim().toLowerCase();
    const min = parseFloat(filters.minScore);
    const startTs = filters.start ? new Date(filters.start).getTime() : null;
    const endTs = filters.end ? new Date(filters.end).getTime() : null;

    const out = allResults.filter((r) => {
      if (filters.verdict && r.verdict !== filters.verdict) return false;
      if (s && !(r.model_name || '').toLowerCase().includes(s)) return false;
      if (!Number.isNaN(min) && isFinite(min)) {
        const score = Number(r.score) || 0;
        if (score < min) return false;
      }
      if (startTs || endTs) {
        const t = new Date(r.created_at).getTime();
        if (startTs && t < startTs) return false;
        if (endTs && t > endTs) return false;
      }
      return true;
    });
    setFiltered(out);
  };

  const clearFilters = () => {
    setFilters({ verdict: '', model: '', start: '', end: '', minScore: '' });
    setFiltered(allResults);
  };

  const exportJSON = () => {
    const blob = new Blob([JSON.stringify(filtered, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `historial_video_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const handleDelete = async (id) => {
    if (!confirm('¿Estás seguro de eliminar este análisis?')) return;
    try {
      await VideoService.deleteAnalysis(id);
      const updated = allResults.filter(r => r.id !== id);
      setAllResults(updated);
      setFiltered(filtered.filter(r => r.id !== id));
    } catch (e) {
      console.error('Error eliminando análisis:', e);
      alert('Error al eliminar el análisis');
    }
  };

  const handleDeleteAll = async () => {
    if (!confirm('¿Estás seguro de eliminar TODO el historial? Esta acción no se puede deshacer.')) return;
    try {
      await VideoService.deleteAllAnalyses();
      setAllResults([]);
      setFiltered([]);
    } catch (e) {
      console.error('Error eliminando historial:', e);
      alert('Error al eliminar el historial');
    }
  };

  const Count = useMemo(() => filtered.length, [filtered]);

  if (loading && filtered.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <History className="w-8 h-8 text-cyan-400" />
          <div>
            <h2 className="text-2xl font-bold text-slate-100">Historial de Análisis</h2>
            <p className="text-sm text-slate-400">{Count} resultados</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleDeleteAll}
            className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
            disabled={Count === 0}
          >
            <AlertTriangle className="w-4 h-4" />
            <span>Eliminar Todo</span>
          </button>
          <button
            onClick={exportJSON}
            className="flex items-center space-x-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Exportar</span>
          </button>
          <button
            onClick={() => setShowFilters((v) => !v)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${showFilters ? 'bg-cyan-600 text-white' : 'bg-slate-700 text-slate-200 hover:bg-slate-600'}`}
          >
            <Filter className="w-4 h-4" />
            <span>Filtros</span>
            <ChevronDown className={`w-4 h-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
          </button>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Veredicto</label>
              <select
                value={filters.verdict}
                onChange={(e) => setFilters({ ...filters, verdict: e.target.value })}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              >
                <option value="">Todos</option>
                <option value="DEEPFAKE">DEEPFAKE</option>
                <option value="REAL">REAL</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Modelo</label>
              <input
                type="text"
                value={filters.model}
                onChange={(e) => setFilters({ ...filters, model: e.target.value })}
                placeholder="modelo_deepfake_final..."
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Fecha inicio</label>
              <input
                type="date"
                value={filters.start}
                onChange={(e) => setFilters({ ...filters, start: e.target.value })}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Fecha fin</label>
              <input
                type="date"
                value={filters.end}
                onChange={(e) => setFilters({ ...filters, end: e.target.value })}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Score mínimo</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                value={filters.minScore}
                onChange={(e) => setFilters({ ...filters, minScore: e.target.value })}
                placeholder="0.5"
                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={applyFilters}
              className="flex items-center space-x-2 px-6 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-colors"
            >
              <Search className="w-4 h-4" />
              <span>Aplicar Filtros</span>
            </button>
            <button
              onClick={clearFilters}
              className="flex items-center space-x-2 px-6 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg transition-colors"
            >
              <X className="w-4 h-4" />
              <span>Limpiar</span>
            </button>
          </div>
        </div>
      )}

      {/* Listado */}
      <div className="space-y-3">
        {filtered.length === 0 ? (
          <div className="text-center py-12 bg-slate-800/50 border border-slate-700/50 rounded-xl">
            <Video className="w-16 h-16 text-slate-600 mx-auto mb-4" />
            <p className="text-slate-400">No hay resultados</p>
          </div>
        ) : (
          filtered.map((r) => {
            const scorePct = Math.round((Number(r.score) || 0) * 100);
            const isDeepfake = r.verdict === 'DEEPFAKE';
            return (
              <div key={r.id} className="bg-slate-800/50 border border-slate-700/50 hover:border-cyan-500/50 rounded-xl p-4 transition-all">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-lg text-cyan-300">Resultado #{r.id}</h4>
                    <p className="text-sm text-slate-300">Modelo: {r.model_name}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <div className={`text-sm font-semibold ${isDeepfake ? 'text-orange-400' : 'text-green-400'}`}>{r.verdict}</div>
                      <div className="text-xs text-slate-400">{new Date(r.created_at).toLocaleString()}</div>
                    </div>
                    <button
                      onClick={() => handleDelete(r.id)}
                      className="p-2 bg-red-600/20 hover:bg-red-600 text-red-400 hover:text-white rounded-lg transition-colors"
                      title="Eliminar análisis"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <div className="mt-3">
                  <div className="w-full bg-slate-700 h-2 rounded overflow-hidden">
                    <div className={`h-2 ${isDeepfake ? 'bg-gradient-to-r from-purple-500 via-cyan-400 to-pink-400' : 'bg-gradient-to-r from-green-500 to-cyan-400'}`} style={{ width: `${scorePct}%` }} />
                  </div>
                  <p className="text-sm text-slate-300 mt-1 flex items-center gap-2">
                    <Gauge className="w-4 h-4 text-slate-400" /> Score: {r.score} ({scorePct}%)
                  </p>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
