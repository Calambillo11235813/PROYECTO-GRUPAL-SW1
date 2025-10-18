# Frontend — visión general y puntos clave

## Entradas principales
- src/main.jsx → src/App.jsx (routing)
- Rutas y protección: src/components/auth/ProtectedRoute.jsx
- Estado global: src/context/authContext.jsx

## Servicios HTTP
- src/services/
  - textAnalysisService.js — analiza texto / carga de archivos
  - audioService.js — subidas y análisis de audio
  - authService.js — autenticación
- Usar VITE_API_URL desde .env.example

## Componentes y módulos
- Modulo_Texto/ — TextAnalyzer, FileAnalysis, ModelComparison
- Modulo_Audio/ — AudioUpload, AudioHistory, AudioResultCard
- ui/ — Button, Input, LoadingSpinner
- Navbar/ — navegación y mobile menu

## Flujo de datos (simplificado)
1. Usuario envía texto o archivo desde UI.
2. Componente usa servicio (textAnalysisService / audioService) para POST.
3. Servicio devuelve JSON con probabilidades/metadatos.
4. Componentes muestran resultados y persisten historial local/consulta endpoint.

## Buenas prácticas observadas
- Separación por características.
- Componentes presentacionales reutilizables.
- Uso de Vite + Tailwind para rendimiento y dev ergonomics.

## Recomendaciones rápidas
- Crear cliente HTTP central (axios) con baseURL/timeouts/interceptors.
- Validaciones y límites en cliente (size/type) y mostrar progreso en uploads.
- Documentar contratos API y agregar tests unitarios para servicios.
- Añadir health-check UI y manejo robusto de errores/reintentos.
