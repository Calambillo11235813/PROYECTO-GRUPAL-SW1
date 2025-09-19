import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/authContext'
import { Login, Dashboard } from './pages/pageExports'
import ProtectedRoute from './components/auth/ProtectedRoute'
import DashboardAudio from './pages/Dashboard_Audio'; // Importa el componente
import './App.css'
import Navbar from './components/Navbar/Navbar';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen w-full bg-cyber-bg-primary">
          <Navbar />
          <div className="pt-20">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route 
                path="/text" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/audio" 
                element={
                  <ProtectedRoute>
                    <DashboardAudio />
                  </ProtectedRoute>
                }
              />
              <Route path="/" element={<Navigate to="/text" replace />} />
            </Routes>
          </div>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
