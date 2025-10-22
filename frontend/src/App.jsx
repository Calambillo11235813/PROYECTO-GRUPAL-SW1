import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from "react-router-dom";
import { AuthProvider } from "./context/authContext";
import { Login, Dashboard } from "./pages/pageExports";
import Profile from "./pages/Profile";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import DashboardAudio from "./pages/Dashboard_Audio";
import "./App.css";
import Navbar from "./components/Navbar/Navbar";

function AppContent() {
  const location = useLocation();
  const hideNavbar = location.pathname === "/login";

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
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
