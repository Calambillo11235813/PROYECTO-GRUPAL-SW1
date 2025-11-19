import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  Download,
  FileJson,
  FileText,
  ArrowLeft,
  Code2,
  Eye,
  EyeOff,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import codeAnalysisService from "../../services/codeAnalysisService";
import AnalysisResults from "./AnalysisResults";

const AnalysisDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showCode, setShowCode] = useState(false);
  const [showAST, setShowAST] = useState(false);

  useEffect(() => {
    const loadAnalysisDetail = async () => {
      setLoading(true);
      try {
        const data = await codeAnalysisService.getAnalysisDetail(id);
        setAnalysisData(data);
      } catch (error) {
        console.error("Error al cargar análisis:", error);
      } finally {
        setLoading(false);
      }
    };

    if (id) loadAnalysisDetail();
  }, [id]);

  const handleDownloadPDF = async () => {
    try {
      await codeAnalysisService.downloadPDFReport(id);
    } catch (error) {
      console.error("Error al descargar PDF:", error);
    }
  };

  const handleDownloadJSON = async () => {
    try {
      const jsonData = await codeAnalysisService.getJSONReport(id);
      const blob = new Blob([JSON.stringify(jsonData, null, 2)], {
        type: "application/json",
      });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `reporte_${id}.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Error al descargar JSON:", error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  if (!analysisData) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-400">No se encontró el análisis</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center space-x-2 text-slate-400 hover:text-cyan-400 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Volver</span>
          </button>

          <div className="flex items-center space-x-3">
            <button
              onClick={handleDownloadJSON}
              className="flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
            >
              <FileJson className="w-4 h-4" />
              <span>JSON</span>
            </button>

            <button
              onClick={handleDownloadPDF}
              className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-purple-500 hover:shadow-lg hover:shadow-cyan-500/50 text-white rounded-lg transition-all"
            >
              <Download className="w-4 h-4" />
              <span>Descargar PDF</span>
            </button>
          </div>
        </div>

        {/* Main Analysis Results */}
        <AnalysisResults analysisData={analysisData} />

        {/* Código Original */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl overflow-hidden">
          <button
            onClick={() => setShowCode(!showCode)}
            className="w-full flex items-center justify-between p-4 hover:bg-slate-700/50 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <Code2 className="w-6 h-6 text-cyan-400" />
              <h3 className="text-lg font-bold text-slate-100">
                Código Original
              </h3>
            </div>
            {showCode ? (
              <EyeOff className="w-5 h-5 text-slate-400" />
            ) : (
              <Eye className="w-5 h-5 text-slate-400" />
            )}
          </button>

          {showCode && (
            <div className="p-6 bg-slate-900/50 border-t border-slate-700/50">
              <pre className="text-sm text-slate-300 font-mono overflow-x-auto bg-slate-950 p-4 rounded-lg">
                <code>{analysisData.codigo_original}</code>
              </pre>
            </div>
          )}
        </div>

        {/* AST */}
        {analysisData.ast && (
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl overflow-hidden">
            <button
              onClick={() => setShowAST(!showAST)}
              className="w-full flex items-center justify-between p-4 hover:bg-slate-700/50 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <FileText className="w-6 h-6 text-purple-400" />
                <h3 className="text-lg font-bold text-slate-100">
                  Abstract Syntax Tree (AST)
                </h3>
              </div>
              {showAST ? (
                <EyeOff className="w-5 h-5 text-slate-400" />
              ) : (
                <Eye className="w-5 h-5 text-slate-400" />
              )}
            </button>

            {showAST && (
              <div className="p-6 bg-slate-900/50 border-t border-slate-700/50">
                <pre className="text-sm text-purple-300 font-mono overflow-x-auto bg-slate-950 p-4 rounded-lg max-h-96">
                  <code>{analysisData.ast}</code>
                </pre>
              </div>
            )}
          </div>
        )}

        {/* Timestamp */}
        <div className="text-center text-sm text-slate-500">
          Análisis realizado el{" "}
          {new Date(analysisData.timestamp_analisis).toLocaleString()}
        </div>
      </div>
    </div>
  );
};

export default AnalysisDetail;
