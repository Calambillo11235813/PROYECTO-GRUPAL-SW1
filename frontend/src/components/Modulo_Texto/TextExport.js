// ===== EXPORTACIONES DEL MÓDULO DE TEXTO =====

// Importar primero localmente los componentes
import TextAnalyzer from './TextAnalyzer/TextAnalyzer';
import TextInput from './TextAnalyzer/TextInput';
import AnalysisResults from './TextAnalyzer/AnalysisResults';
import ModelComparison from './ModelComparison/ModelComparison';
import ModelCard from './ModelComparison/ModelCard';
import ComparisonChart from './ModelComparison/ComparisonChart';
import FileAnalysis from './FileAnalysis/FileAnalysis';
import FileUploader from './FileAnalysis/FileUploader';
import FilePreview from './FileAnalysis/FilePreview';
import ServiceStatus from './ServiceStatus/ServiceStatus';
import StatusIndicator from './ServiceStatus/StatusIndicator';
import AnalysisCard from './shared/AnalysisCard';
import LoadingSpinner from './shared/LoadingSpinner';
import ErrorMessage from './shared/ErrorMessage';

// Exportar los componentes
export { TextAnalyzer, TextInput, AnalysisResults };
export { ModelComparison, ModelCard, ComparisonChart };
export { FileAnalysis, FileUploader, FilePreview };
export { ServiceStatus, StatusIndicator };
export { AnalysisCard, LoadingSpinner, ErrorMessage };

// Exportaciones agrupadas para conveniencia
export const TextComponents = {
  TextAnalyzer,
  TextInput,
  AnalysisResults
};

export const ModelComponents = {
  ModelComparison,
  ModelCard,
  ComparisonChart
};

export const FileComponents = {
  FileAnalysis,
  FileUploader,
  FilePreview
};

export const ServiceComponents = {
  ServiceStatus,
  StatusIndicator
};

export const SharedComponents = {
  AnalysisCard,
  LoadingSpinner,
  ErrorMessage
};