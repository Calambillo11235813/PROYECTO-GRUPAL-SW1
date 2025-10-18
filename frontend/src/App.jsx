<<<<<<< HEAD
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
=======
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { AuthProvider } from './context/authContext'
import { Login, Dashboard } from './pages/pageExports'
import Profile from './pages/Profile'
import ProtectedRoute from './components/auth/ProtectedRoute'
import DashboardAudio from './pages/Dashboard_Audio'
import './App.css'
import Navbar from './components/Navbar/Navbar'

function AppContent() {
  const location = useLocation()
  const hideNavbar = location.pathname === '/login'

  return (
    <div className="min-h-screen w-full bg-cyber-bg-primary">
      {!hideNavbar && <Navbar />}
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
          <Route 
            path="/profile" 
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } 
          />
          <Route path="/" element={<Navigate to="/text" replace />} />
        </Routes>
      </div>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
>>>>>>> UNION
  )
}

export default App
