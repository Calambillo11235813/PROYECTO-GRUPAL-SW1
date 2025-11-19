import React, { useState } from "react";
import { Code2, Upload, History, BarChart3, FileCode2 } from "lucide-react";
import CodeUploader from "../components/Modulo_Codigo/CodeUploader";
import AnalysisResults from "../components/Modulo_Codigo/AnalysisResults";
import CodeHistory from "../components/Modulo_Codigo/CodeHistory";
import CodeStatistics from "../components/Modulo_Codigo/CodeStatistics";
import codeAnalysisService from "../services/codeAnalysisService";

const Dashboard_Codigo = () => {
  const [activeTab, setActiveTab] = useState("upload");
  const [currentAnalysis, setCurrentAnalysis] = useState(null);

  const handleAnalysisComplete = async (result) => {
    // Obtener detalles completos del análisis
    try {
      const detailedAnalysis = await codeAnalysisService.getAnalysisDetail(
        result.id
      );
      setCurrentAnalysis(detailedAnalysis);
      setActiveTab("results");
    } catch (error) {
      console.error("Error al obtener detalles:", error);
    }
  };

  const tabs = [
    { id: "upload", label: "Subir Código", icon: Upload },
    {
      id: "results",
      label: "Resultados",
      icon: FileCode2,
      disabled: !currentAnalysis,
    },
    { id: "history", label: "Historial", icon: History },
    { id: "stats", label: "Estadísticas", icon: BarChart3 },
  ];

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Fixed Background */}
      <div className="fixed inset-0 w-full h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 -z-10" />

      {/* Header */}
      <div className="bg-slate-800/50 border-b border-slate-700/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-cyan-500 to-purple-500 rounded-lg">
                <Code2 className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                  Análisis de Código
                </h1>
                <p className="text-sm text-slate-400">
                  Detección de código generado por IA
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-slate-800/30 border-b border-slate-700/50 sticky top-[73px] z-10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              const isDisabled = tab.disabled;

              return (
                <button
                  key={tab.id}
                  onClick={() => !isDisabled && setActiveTab(tab.id)}
                  disabled={isDisabled}
                  className={`
                    flex items-center space-x-2 px-6 py-3 font-medium transition-all duration-200
                    ${
                      isActive
                        ? "text-cyan-400 border-b-2 border-cyan-400 bg-slate-800/50"
                        : isDisabled
                        ? "text-slate-600 cursor-not-allowed"
                        : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/30"
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === "upload" && (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-slate-100 mb-2">
                Sube tu archivo de código
              </h2>
              <p className="text-slate-400">
                Analizaremos el código para detectar si fue generado por IA
              </p>
            </div>
            <CodeUploader onAnalysisComplete={handleAnalysisComplete} />
          </div>
        )}

        {activeTab === "results" && currentAnalysis && (
          <AnalysisResults analysisData={currentAnalysis} />
        )}

        {activeTab === "history" && <CodeHistory />}

        {activeTab === "stats" && <CodeStatistics />}
      </div>
    </div>
  );
};

export default Dashboard_Codigo;
