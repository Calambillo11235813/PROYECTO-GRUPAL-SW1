# Frontend — Arquitectura y Flujos (actualizado 19/11/2025)

## Stack y Metas
- Vite + React 19 + React Router 7 + Tailwind.
- Estado global de autenticación con Context/Reducer (`src/context/authContext.jsx`).
- Capa de servicios HTTP en `src/services/*` (fetch/axios) que encapsula endpoints del backend.

## Entradas y Routing
- `src/main.jsx` → monta `src/App.jsx` y el router.
- Ruta protegida: `src/components/auth/ProtectedRoute.jsx` (bloquea rutas si `!isAuthenticated`, renderiza spinner si `isLoading`).
- Páginas exportadas: `src/pages/pageExports.js` (Login, Dashboard, Dashboard_Codigo).

## Autenticación (flujo)
- `authService.js`
  - `POST /api/auth/login/` y `POST /api/auth/register/` → guarda `access_token`, `refresh_token` y `user` en `localStorage`.
  - `GET /api/auth/profile/` para hidratar sesión.
  - `POST /api/auth/logout/` con `refresh` para blacklist, siempre limpia tokens.
  - `POST /api/auth/token/refresh/` para renovar `access` (sin interceptores automáticos).
- `authContext.jsx` hidrata sesión al montar: si hay tokens/usuario, hace `getProfile()`; expone `login`, `register`, `logout` y estado (`isAuthenticated`, `isLoading`).
- `ProtectedRoute.jsx` redirige a `/login` si no autenticado.

## Configuración de API
- `src/services/config.js` define `BASE_URL = 'http://127.0.0.1:8000/api'` y helpers:
  - `API_ENDPOINTS = { AUTH, TEXTO, AUDIO }`.
  - `getAuthHeaders(includeAuth, isFormData)` para JSON/FormData y `Authorization`.
- Nota: actualmente el `BASE_URL` está hardcodeado. Recomendado migrar a `import.meta.env.VITE_API_URL`.

## Capa de Servicios y Endpoints
- Texto — `textAnalysisService.js` (fetch):
  - `GET /api/texto/` → estado del servicio.
  - `POST /api/texto/analizar/` → texto directo (con auth opcional).
  - `POST /api/texto/comparar/` → comparación modelos.
  - `POST /api/texto/analizar-archivo/` → FormData `archivo`, `modelo`.
  - Validaciones en cliente: longitud texto (<10k), tipo/tamaño archivo (<=5MB), headers correctos para FormData.
- Audio — `audioService.js` (axios):
  - `POST /api/audio/upload/` → FormData `file` con `Authorization`.
  - `GET /api/audio/` → historial del usuario autenticado.
  - `GET /api/audio/certificado/:id/` → descarga PDF (responseType 'blob').
- Código — `codeAnalysisService.js` (fetch):
  - `POST /api/codigo/subir/` → FormData `archivo`.
  - `GET /api/codigo/analisis/:id/` → detalle profesional.
  - `GET /api/codigo/historial/` (+ filtros query: nombre, lenguaje, ia, inicio, fin).
  - `POST /api/codigo/historial/comparar/` → comparar IDs.
  - `GET /api/codigo/historial/estadisticas/` → KPIs.
  - `GET /api/codigo/reporte/pdf/:id/` → descarga PDF; `GET /json/:id/` → reporte JSON.
  - `GET /api/codigo/historial/exportar/` → JSON completo del historial (descarga).

## Módulos y Componentes
- Texto — `src/components/Modulo_Texto/*`
  - `TextAnalyzer` (entrada y envío), `ModelComparison` (comparación B/N), `ServiceStatus` (health-check), compartidos: `LoadingSpinner`, `AnalysisCard`, `ErrorMessage`.
- Audio — `src/components/Modulo_Audio/*`
  - `AudioUpload`, `AudioHistory`, `AudioResultCard`, `AudioPlayer` (reproducción), combinan servicio y UI.
- Código — `src/components/Modulo_Codigo/*`
  - `CodeUploader`, `CodeHistory`, `AnalysisDetail`, `CompareAnalysis`, `CodeStatistics`, `AnalysisResults`.
- UI base — `src/components/ui/*` y `Navbar/*`.

## Flujos de Interacción con Backend
- Auth: LocalStorage tokens → headers `Authorization` → CORS permite `localhost:5173`.
- Texto: POST JSON / FormData a `/api/texto/*`, muestra predicción, confianza, fragmentos; estado de servicio vía `/api/texto/`.
- Audio: Subida `multipart/form-data` a `/api/audio/upload/` → backend procesa RF + espectrograma → UI muestra resultado y permite certificado.
- Código: Subida archivo → backend ejecuta análisis HF + AST y métricas → UI muestra detalle, compara, calcula KPIs y exporta JSON.

## Patrones Clave
- Feature-first structure: módulos por dominio (Texto/Audio/Código).
- Service layer: servicios HTTP por dominio, validando inputs.
- Auth context + ProtectedRoute: control de acceso.
- Form handling con FormData y control cuidadoso de headers.
- Descarga de binarios vía blob (PDFs/reportes).

## Riesgos y Mejoras
- Base URL hardcodeada: migrar a `VITE_API_URL` y `.env`.
- Interceptores/refresh: crear cliente axios central con interceptores 401 → `authService.refreshAccessToken()` y reintentos.
- Consistencia HTTP: unificar uso de axios (hoy hay mezcla fetch/axios) con timeouts y manejo de errores homogéneo.
- Paginación: preparar UI para paginar historias grandes (audio/código); hoy se asume listados completos.
- Estados de carga/errores: ya existen, pero falta estandarizar toasts/alerts en todos los módulos.
- Seguridad: evitar dejar tokens indefinidamente en localStorage; considerar expiración/idle timeout.

## Roadmap rápido
- Config: `VITE_API_URL`, `VITE_TIMEOUT_MS`, `VITE_ENABLE_MOCKS`.
- HTTP client: `apiClient.ts/js` con axios, baseURL de env, interceptores, retries backoff.
- Hooks: `useApi`, `useAsync` para estandarizar loading/error/data.
- Tests: unitarios de servicios (msw/jest) y de componentes críticos.
- Accesibilidad: estados de foco, roles, y mensajes de error legibles.

## Contratos API (resumen)
- Auth: `/api/auth/{register,login,logout,profile,token/refresh/}`.
- Texto: `/api/texto/{,analizar/,comparar/,analizar-archivo/}`.
- Audio: `/api/audio/{upload/, ,certificado/:id/}`.
- Código: `/api/codigo/{subir/,analisis/:id/,historial/,historial/comparar/,historial/estadisticas/,historial/exportar/,reporte/(pdf|json)/:id/}`.

## Referencias
- Configuración de Vite: `vite.config.js`.
- Dependencias principales: ver `package.json`.
