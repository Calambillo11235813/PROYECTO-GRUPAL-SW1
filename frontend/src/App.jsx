import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🤖 Sistema de Detección de IA
          </h1>
          <p className="text-gray-600">
            Analiza texto y archivos para detectar contenido generado por IA
          </p>
        </header>

        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
          <div className="text-center">
            <button
              onClick={() => setCount((count) => count + 1)}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition-colors"
            >
              Contador: {count}
            </button>
          </div>
        </div>

        {/* OPCIÓN 1: Azul Tecnológico */}
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4">
          <h3 className="text-blue-700 font-semibold">Resultado: IA Detectada</h3>
          <p className="text-slate-600">Probabilidad: 87.5%</p>
        </div>

        {/* OPCIÓN 2: Púrpura Futurista */}
        <div className="bg-violet-50 border-l-4 border-violet-500 p-4">
          <h3 className="text-violet-700 font-semibold">Resultado: IA Detectada</h3>
          <p className="text-gray-600">Probabilidad: 87.5%</p>
        </div>

        {/* OPCIÓN 4: Gradiente Cibernético */}
        <div className="bg-slate-900 border-l-4 border-cyan-500 p-4">
          <h3 className="text-cyan-400 font-semibold">Resultado: IA Detectada</h3>
          <p className="text-slate-300">Probabilidad: 87.5%</p>
        </div>
      </div>
    </div>
  )
}

export default App
