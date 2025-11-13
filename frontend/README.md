# 🤖 Sistema de Detección de Contenido Generado por IA

## 📱 **Frontend React + Vite**

Sistema web moderno para detectar si un texto fue generado por Inteligencia Artificial o escrito por un humano, con interfaz futurista y tecnología de vanguardia.

---

## 🎯 **Descripción del Proyecto**

Aplicación frontend desarrollada en React que se conecta con un backend Django para proporcionar análisis instantáneo de texto mediante modelos de Machine Learning especializados en detección de contenido generado por IA.

### **🌟 Características Principales**

- ✅ **Interfaz Cyberpunk** - Diseño futurista con gradientes neón
- ✅ **Análisis en Tiempo Real** - Detección instantánea de contenido IA
- ✅ **Carga de Archivos** - Soporte para TXT, PDF, DOCX
- ✅ **Análisis Dual** - Comparación entre múltiples modelos
- ✅ **Visualización Avanzada** - Gráficos de probabilidades
- ✅ **Responsive Design** - Funciona en móviles y desktop

---

## 🏗️ **Stack Tecnológico**

### **⚛️ Framework Principal**

- **React 18** - Framework de interfaz de usuario
- **Vite** - Build tool ultra-rápido
- **JavaScript ES6+** - Lenguaje de programación

### **🎨 Diseño y Estilos**

- **Tailwind CSS v3.4.17** - Framework de CSS utility-first
- **PostCSS** - Procesador de CSS
- **Autoprefixer** - Compatibilidad de navegadores

### **🔌 Integraciones**

- **Axios** - Cliente HTTP para APIs
- **React Router** - Navegación SPA
- **React Hooks** - Manejo de estado moderno

---

## 🎨 **Tema de Diseño: Gradiente Cibernético**

### **🌈 Paleta de Colores**

```css
🔵 Azul Neón:     #06B6D4 (cyan-500)
🟣 Púrpura Neón:  #A855F7 (purple-500)
🟡 Amarillo Acento: #FDE047 (yellow-300)
⚫ Fondo Oscuro:   #0F172A (slate-900)
⚪ Texto Claro:    #F1F5F9 (slate-100)
🟢 Éxito:         #22C55E (green-500)
🔴 Peligro:       #F97316 (orange-500)
```

### **✨ Efectos Visuales**

- Gradientes animados
- Efectos de glow y neón
- Transiciones suaves
- Animaciones cyberpunk
- Partículas de fondo

---

## 🚀 **Funcionalidades Implementadas**

### **📝 HU-002: Análisis de Texto Directo**

- Input de texto con syntax highlighting
- Análisis instantáneo mientras escribes
- Visualización de probabilidades en tiempo real

### **📁 HU-001: Carga de Archivos**

- Drag & drop futurista
- Soporte para múltiples formatos
- Preview del contenido antes del análisis
- Validación visual de archivos

### **📊 HU-003: Visualización de Probabilidades**

- Gráficos circulares animados
- Barras de progreso con efectos neón
- Comparación visual entre modelos
- Historial de análisis

---

## ⚡ **Instalación y Configuración**

### **📋 Prerrequisitos**

- Node.js 18+
- npm 9+
- Backend Django corriendo en puerto 8000

### **🔧 Instalación**

```bash
# Clonar repositorio
git clone [repository-url]
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env

# Iniciar servidor de desarrollo
npm run dev
```

### **🌐 URLs**

- **Desarrollo**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/texto

---

## 📱 **Estructura de la Aplicación**

### **🗂️ Páginas Principales**

```
├── 🏠 Home - Página principal con opciones
├── 📝 TextAnalysis - Análisis de texto directo
├── 📁 FileAnalysis - Carga y análisis de archivos
├── 🔄 ModelComparison - Comparación de modelos
└── 📊 History - Historial de análisis
```

### **🧩 Componentes Principales**

```
components/
├── forms/
│   ├── TextInput.jsx        # Input de texto cyberpunk
│   ├── FileUpload.jsx       # Carga de archivos futurista
│   └── ModelSelector.jsx    # Selector de modelos IA
├── results/
│   ├── AnalysisResult.jsx   # Resultado con efectos neón
│   ├── ProbabilityChart.jsx # Gráficos animados
│   └── ModelComparison.jsx  # Comparación visual
└── ui/
    ├── Button.jsx           # Botones cyberpunk
    ├── Card.jsx             # Tarjetas con glow
    └── LoadingSpinner.jsx   # Spinner futurista
```

---

## 🔗 **Integración con Backend**

### **🔌 Endpoints Conectados**

```http
POST /api/texto/analizar/          # Análisis texto directo
POST /api/texto/analizar-archivo/  # Análisis de archivos
POST /api/texto/comparar/          # Comparación de modelos
GET  /api/texto/estado/            # Estado del sistema
```

### **📡 Servicios API**

- `textAnalysis.js` - Análisis de texto
- `fileUpload.js` - Carga de archivos
- `modelComparison.js` - Comparación de modelos
- `systemStatus.js` - Estado del sistema

---

## 🧪 **Testing y Calidad**

### **🔍 Tests Implementados**

- Tests unitarios de componentes
- Tests de integración con APIs
- Tests de interfaz de usuario
- Tests de accesibilidad

### **📊 Herramientas de Calidad**

- ESLint - Linting de código
- Prettier - Formateo automático
- Lighthouse - Performance audit
- Vite Bundle Analyzer - Análisis de bundle

---

## 📈 **Performance y Optimización**

### **⚡ Optimizaciones Implementadas**

- Code splitting automático
- Lazy loading de componentes
- Optimización de imágenes
- Cache de servicios API
- Minificación y compresión

### **📱 Responsive Design**

- Mobile-first approach
- Breakpoints optimizados
- Touch-friendly interface
- PWA ready

---

## 🔮 **Funcionalidades Futuras**

### **🚀 Roadmap V2**

- [ ] Análisis en lotes de archivos
- [ ] Exportación de reportes PDF
- [ ] Dashboard de estadísticas
- [ ] Sistema de usuarios
- [ ] API de terceros
- [ ] Modo offline

---

## 👥 **Equipo de Desarrollo**

**Proyecto Académico - Ingeniería de Software I**

- Universidad: [Nombre de la Universidad]
- Semestre: Décimo
- Tecnologías: React + Django + PostgreSQL + AI/ML

---

## 📞 **Soporte y Documentación**

### **📚 Documentación Adicional**

- [README_DESARROLLADOR.md](./README_DESARROLLADOR.md) - Guía para desarrolladores
- [API_DOCS.md](./docs/API_DOCS.md) - Documentación de APIs
- [DEPLOYMENT.md](./docs/DEPLOYMENT.md) - Guía de despliegue

### **🐛 Reportar Issues**

- GitHub Issues para bugs
- Feature requests vía Pull Requests
- Documentación en el Wiki del proyecto

---

**🎯 Estado: En Desarrollo Activo | 🚀 Version: 1.0.0-beta | 📅 Última Actualización: Septiembre 2025**

---

**🤖 ¡Explora el futuro de la detección de IA con nuestra interfaz cyberpunk!** ⚡
