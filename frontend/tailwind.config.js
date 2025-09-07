/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          // Fondos - Más oscuros para mejor contraste
          bg: {
            primary: '#0a0f1c',    // Más oscuro que slate-900
            secondary: '#151b2e',  // Más oscuro que slate-800
            card: '#1a1f35',       // Fondo de cards más oscuro
          },
          // Textos - Mayor contraste
          text: {
            primary: '#ffffff',    // Blanco puro para máximo contraste
            secondary: '#e2e8f0',  // Gris muy claro (slate-200)
            accent: '#00e5ff',     // Cyan más brillante
            muted: '#94a3b8',      // slate-400 (mantener)
          },
          // Acentos - Más vibrantes
          accent: {
            primary: '#9333ea',    // purple-600 (más oscuro)
            secondary: '#0891b2',  // cyan-600 (más oscuro)
            highlight: '#fbbf24',  // amber-400 (más visible)
          },
          // Estados - Mejor contraste
          success: '#10b981',      // emerald-500
          error: '#ef4444',        // red-500
          warning: '#f59e0b',      // amber-500
          info: '#3b82f6',         // blue-500
          // Bordes - Más visibles
          border: {
            primary: '#0891b2',    // cyan-600
            secondary: '#475569',  // slate-600
            muted: '#334155',      // slate-700
          }
        }
      },
      // Gradientes actualizados
      backgroundImage: {
        'cyber-gradient': 'linear-gradient(135deg, #0a0f1c 0%, rgba(147, 51, 234, 0.15) 50%, #0a0f1c 100%)',
        'cyber-button': 'linear-gradient(135deg, #9333ea 0%, #0891b2 100%)',
        'cyber-card': 'linear-gradient(135deg, rgba(26, 31, 53, 0.9) 0%, rgba(26, 31, 53, 0.95) 100%)',
      },
      // Sombras actualizadas
      boxShadow: {
        'cyber-glow': '0 0 25px rgba(147, 51, 234, 0.4)',
        'cyber-glow-lg': '0 0 40px rgba(147, 51, 234, 0.5)',
        'cyber-glow-cyan': '0 0 25px rgba(8, 145, 178, 0.4)',
        'cyber-glow-green': '0 0 25px rgba(16, 185, 129, 0.4)',
      },
    },
  },
  plugins: [],
}