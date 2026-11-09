import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import './index.css'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Layout from './layouts/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import StudentRecords from './pages/StudentRecords'
import DataImports from './pages/DataImports'
import AcademicAnalytics from './pages/AcademicAnalytics'
import RiskMonitoring from './pages/RiskMonitoring'
import Recommendations from './pages/Recommendations'
import InterventionTracking from './pages/InterventionTracking'
import Reports from './pages/Reports'
import UserManagement from './pages/UserManagement'
import ModelManagement from './pages/ModelManagement'
import AuditLogs from './pages/AuditLogs'
import Settings from './pages/Settings'

const ProtectedRoute: React.FC<{ children: React.ReactNode; roles?: string[] }> = ({ children, roles }) => {
  const { isAuthenticated, loading, user } = useAuth()
  const location = useLocation()
  if (loading) return <div style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', background: '#0f172a', color: '#e2e8f0' }}>Loading EduPredict…</div>
  if (!isAuthenticated) return <Navigate to="/login" state={{ from: location }} replace />
  if (roles && roles.length && !roles.some(r => user?.roles?.includes(r))) {
    return <Layout><div style={{ color: '#fecaca', background: 'rgba(239,68,68,0.12)', padding: 16, borderRadius: 12 }}>You do not have permission to access this page.</div></Layout>
  }
  return <Layout>{children}</Layout>
}

function AppRoutes() {
  const admin = ['system_admin']
  const staff = ['system_admin', 'lecturer', 'academic_advisor', 'head_of_department', 'dean', 'registry']
  const support = ['system_admin', 'lecturer', 'academic_advisor', 'head_of_department']
  const imports = ['system_admin', 'registry']
  const audit = ['system_admin', 'registry']
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<ProtectedRoute roles={staff}><Dashboard /></ProtectedRoute>} />
      <Route path="/students" element={<ProtectedRoute roles={staff}><StudentRecords /></ProtectedRoute>} />
      <Route path="/data-imports" element={<ProtectedRoute roles={imports}><DataImports /></ProtectedRoute>} />
      <Route path="/analytics" element={<ProtectedRoute roles={staff}><AcademicAnalytics /></ProtectedRoute>} />
      <Route path="/risk-monitoring" element={<ProtectedRoute roles={staff}><RiskMonitoring /></ProtectedRoute>} />
      <Route path="/recommendations" element={<ProtectedRoute roles={support}><Recommendations /></ProtectedRoute>} />
      <Route path="/interventions" element={<ProtectedRoute roles={support}><InterventionTracking /></ProtectedRoute>} />
      <Route path="/reports" element={<ProtectedRoute roles={staff}><Reports /></ProtectedRoute>} />
      <Route path="/users" element={<ProtectedRoute roles={admin}><UserManagement /></ProtectedRoute>} />
      <Route path="/models" element={<ProtectedRoute roles={admin}><ModelManagement /></ProtectedRoute>} />
      <Route path="/audit-logs" element={<ProtectedRoute roles={audit}><AuditLogs /></ProtectedRoute>} />
      <Route path="/settings" element={<ProtectedRoute roles={staff}><Settings /></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  )
}
