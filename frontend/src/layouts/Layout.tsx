import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const ALL = ['*']
const menuItems: { path: string; label: string; icon: string; roles: string[] }[] = [
  { path: '/dashboard', label: 'Dashboard', icon: '📊', roles: ALL },
  { path: '/students', label: 'Student Records', icon: '🎓', roles: ALL },
  { path: '/data-imports', label: 'Data Imports', icon: '📁', roles: ['system_admin', 'registry'] },
  { path: '/analytics', label: 'Academic Analytics', icon: '📈', roles: ALL },
  { path: '/risk-monitoring', label: 'Risk Monitoring', icon: '⚠️', roles: ALL },
  { path: '/recommendations', label: 'Recommendations', icon: '💡', roles: ['system_admin', 'lecturer', 'academic_advisor', 'head_of_department'] },
  { path: '/interventions', label: 'Interventions', icon: '✅', roles: ['system_admin', 'lecturer', 'academic_advisor', 'head_of_department'] },
  { path: '/reports', label: 'Reports', icon: '📄', roles: ALL },
  { path: '/users', label: 'User Management', icon: '👥', roles: ['system_admin'] },
  { path: '/models', label: 'Model Management', icon: '🤖', roles: ['system_admin'] },
  { path: '/audit-logs', label: 'Audit Logs', icon: '🔍', roles: ['system_admin', 'registry'] },
  { path: '/settings', label: 'Settings', icon: '⚙️', roles: ALL },
]

const roleLabel = (roles: string[] = []) => {
  const map: Record<string, string> = { system_admin: 'System Administrator', lecturer: 'Lecturer', academic_advisor: 'Academic Advisor', head_of_department: 'Head of Department', dean: 'Dean', registry: 'Registry Staff' }
  return roles.map(r => map[r] || r).join(', ') || 'User'
}

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const visible = menuItems.filter(i => i.roles.includes('*') || i.roles.some(r => user?.roles?.includes(r)))

  return (
    <div className={`min-h-screen bg-slate-950 text-slate-200 relative ${sidebarOpen ? 'overflow-hidden' : ''}`}>
      {/* Mobile hamburger */}
      <button
        onClick={() => setSidebarOpen(true)}
        className="lg:hidden fixed top-4 left-4 z-50 rounded-xl bg-slate-800/90 border border-slate-600 px-3 py-2 text-sm font-medium text-white hover:bg-slate-700 transition-all"
      >
        ☰ Menu
      </button>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-[260px] border-r border-slate-800/80 bg-gradient-to-b from-slate-900 to-slate-950 transform transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 lg:shadow-none lg:border-r lg:border-slate-800/80`}
      >
        <div className="flex items-center justify-between p-5 border-b border-slate-800/60">
          <div className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 text-xl shadow-lg shadow-blue-900/30">🎓</div>
            <div>
              <h1 className="text-lg font-extrabold text-white leading-tight">EduPredict</h1>
              <p className="text-[11px] text-slate-400">BUSE Academic Intelligence</p>
            </div>
          </div>
          {sidebarOpen && (
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden rounded-xl bg-slate-800 px-2 py-1.5 text-sm text-slate-300 hover:bg-slate-700"
            >
              ✕ Close
            </button>
          )}
        </div>
        <nav className="px-3 pb-36 space-y-0.5 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 160px)' }}>
          {visible.map((item) => {
            const active = location.pathname === item.path
            return (
              <Link key={item.path} to={item.path}
                onClick={() => setSidebarOpen(false)}
                className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium ${active ? 'bg-blue-600/15 text-white ring-1 ring-inset ring-blue-500/25' : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-100'}`}>
                <span className="text-base w-5 text-center">{item.icon}</span><span className="truncate">{item.label}</span>
              </Link>
            )
          })}
        </nav>
        <div className="border-t border-slate-800/80 bg-slate-950/80 p-4 backdrop-blur">
          <div className="mb-3 flex items-center gap-3">
            <div className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-gradient-to-br from-blue-500 to-blue-700 text-sm font-bold text-white">{(user?.full_name || 'U').charAt(0).toUpperCase()}</div>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-white">{user?.full_name || 'User'}</p>
              <p className="truncate text-[11px] text-slate-400">{roleLabel(user?.roles)}</p>
            </div>
          </div>
          <button onClick={() => { logout(); navigate('/login') }} className="w-full rounded-xl border border-rose-500/25 bg-rose-500/10 px-3 py-2 text-sm font-semibold text-rose-300 hover:bg-rose-500/15">Logout</button>
        </div>
      </aside>

      {/* Main content */}
      <main className={`min-h-screen p-4 sm:p-6 lg:p-8 lg:ml-[260px] z-10`}>
        <div className="mx-auto max-w-7xl">{children}</div>
      </main>
    </div>
  )
}

export default Layout
