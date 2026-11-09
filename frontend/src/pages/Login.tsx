import React, { useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const Login: React.FC = () => {
  const { login, isAuthenticated, loading } = useAuth()
  const location = useLocation() as any
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  if (!loading && isAuthenticated) {
    return <Navigate to={location.state?.from?.pathname || '/dashboard'} replace />
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await login(email.trim(), password)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed. Check your credentials and ensure the backend is running.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center p-6">
      <div className="w-full max-w-[920px]">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Brand panel */}
          <div className="lg:flex lg:items-center lg:justify-center p-6 lg:p-0">
            <div className="max-w-md mx-auto">
              <div className="inline-flex items-center justify-center h-16 w-16 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg shadow-blue-900/40 mb-6">
                <span className="text-3xl">🎓</span>
              </div>
              <h1 className="text-4xl font-extrabold text-white tracking-tight mb-2">EduPredict</h1>
              <p className="text-xl text-blue-200 mb-6">
                AI Data-Driven Student Academic Performance Prediction &amp; Early-Warning System
              </p>
              <div className="rounded-xl bg-blue-600/10 p-5 border border-blue-500/20">
                <h3 className="text-sm font-semibold text-blue-100 mb-3">Target institution</h3>
                <p className="text-sm text-blue-200 mb-3">Bindura University of Science Education (BUSE)</p>
                <h3 className="text-sm font-semibold text-blue-100 mb-3">Purpose</h3>
                <p className="text-sm text-blue-200 mb-3">
                  Identify at-risk students early so lecturers and advisors can intervene while there is still time to act.
                </p>
                <p className="text-xs text-blue-300/70 mt-3">
                  Prototype — synthetic demo data. Predictions are decision-support estimates, not verdicts.
                </p>
              </div>
            </div>
          </div>

          {/* Sign-in panel */}
          <div className="flex flex-col justify-center p-6 lg:p-8 bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-3xl shadow-2xl shadow-blue-900/20">
            <h2 className="text-2xl font-bold text-white mb-2">Sign in</h2>
            <p className="text-slate-400 mb-8">Access your role-based dashboard</p>

            <form onSubmit={handleSubmit} className="space-y-5">
              {error && (
                <div className="rounded-lg border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-200">
                  {error}
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Institutional email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="name@buse.ac.zw"
                  className="w-full px-4 py-3 rounded-xl border border-slate-600 bg-slate-950/50 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="••••••••"
                  className="w-full px-4 py-3 rounded-xl border border-slate-600 bg-slate-950/50 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full flex items-center justify-center px-4 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold text-sm shadow-lg shadow-blue-900/30 hover:from-blue-500 hover:to-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {submitting ? 'Signing in…' : 'Sign in'}
              </button>
            </form>

            <div className="mt-6 border-t border-slate-700/50 pt-6">
              <p className="text-xs text-slate-500 text-center">
                Roles: System Administrator · Lecturer · Academic Advisor · Head of Department · Dean · Registry Staff
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login