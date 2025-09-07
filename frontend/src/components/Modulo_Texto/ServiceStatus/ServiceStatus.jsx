import React, { useState, useEffect, useCallback } from 'react';
import { textAnalysisService } from '../../../services/textAnalysisService';
import StatusIndicator from './StatusIndicator';

/**
 * Componente que monitorea y muestra el estado del servicio de análisis de texto
 * @param {Object} props - Propiedades del componente
 * @param {number} props.refreshInterval - Intervalo de actualización en ms (default: 60000)
 * @param {boolean} props.showDetails - Mostrar detalles adicionales (default: false)
 * @param {Function} props.onStatusChange - Callback cuando cambia el estado
 */
const ServiceStatus = ({ refreshInterval = 60000, showDetails = false, onStatusChange }) => {
  const [status, setStatus] = useState('loading');
  const [statusData, setStatusData] = useState(null);
  const [latency, setLatency] = useState(null);
  const [lastChecked, setLastChecked] = useState(null);
  const [error, setError] = useState(null);

  const checkServiceStatus = useCallback(async () => {
    setStatus('loading');
    const startTime = Date.now();
    
    try {
      const response = await textAnalysisService.getServiceStatus();
      const responseTime = Date.now() - startTime;
      setLatency(responseTime);
      
      if (response.success) {
        const newStatus = {
          status: response.data.status === 'ok' ? 'online' : 'degraded',
          data: response.data
        };
        
        // Si la respuesta tardó demasiado, considerarlo degradado
        if (responseTime > 1000) {
          newStatus.status = 'degraded';
        }
        
        setStatus(newStatus.status);
        setStatusData(newStatus.data);
        setError(null);
        
        // Ejecutar callback si está definido
        if (onStatusChange) {
          onStatusChange(newStatus);
        }
      } else {
        setStatus('degraded');
        setError(response.error);
        if (onStatusChange) {
          onStatusChange({ status: 'degraded', error: response.error });
        }
      }
    } catch (err) {
      console.error('Error al verificar estado del servicio:', err);
      setStatus('offline');
      setError(err.message);
      if (onStatusChange) {
        onStatusChange({ status: 'offline', error: err.message });
      }
    }
    
    setLastChecked(new Date());
  }, [onStatusChange]);

  // Verificar al montar y en intervalos
  useEffect(() => {
    checkServiceStatus();
    
    // Configurar intervalo para verificación periódica
    const intervalId = setInterval(checkServiceStatus, refreshInterval);
    
    // Limpiar intervalo al desmontar
    return () => clearInterval(intervalId);
  }, [checkServiceStatus, refreshInterval]);

  // Formatear última verificación
  const formatLastChecked = () => {
    if (!lastChecked) return 'Nunca';
    
    const now = new Date();
    const diffMs = now - lastChecked;
    const diffSec = Math.floor(diffMs / 1000);
    
    if (diffSec < 60) return `Hace ${diffSec} segundos`;
    if (diffSec < 3600) return `Hace ${Math.floor(diffSec / 60)} minutos`;
    return lastChecked.toLocaleTimeString();
  };

  // Mensaje basado en el estado
  const getMessage = () => {
    if (status === 'loading') return 'Verificando estado del servicio...';
    if (status === 'online') return statusData?.message || 'Servicio operando normalmente';
    if (status === 'degraded') return statusData?.message || 'Rendimiento reducido';
    if (status === 'offline') return error || 'Servicio no disponible';
    return '';
  };

  return (
    <div className="bg-slate-800 bg-opacity-70 p-3 rounded-lg shadow-lg border border-slate-700">
      <div className="flex justify-between items-center">
        <h3 className="text-slate-200 font-medium text-sm">Estado del Servicio</h3>
        
        {/* Botón de actualización manual */}
        <button 
          onClick={checkServiceStatus}
          className="text-xs text-cyan-400 hover:text-cyan-300 transition-colors"
          aria-label="Actualizar estado"
        >
          ↻ Actualizar
        </button>
      </div>
      
      <div className="mt-2">
        <StatusIndicator 
          status={status} 
          message={getMessage()} 
          latency={latency} 
        />
      </div>
      
      {showDetails && (
        <div className="mt-3 border-t border-slate-700 pt-2">
          <div className="text-xs text-slate-400">
            <div>Última verificación: {formatLastChecked()}</div>
            {statusData && statusData.version && (
              <div>Versión API: {statusData.version}</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ServiceStatus;