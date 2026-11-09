import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { User } from '../contexts/AuthContext'

interface SidebarProps {
  user: User
  onLogout: () => void
}

const Sidebar: React.FC<SidebarProps> = ({ user, onLogout }) => {
  const location = useLocation()

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊', roles: ['*'] },
    { path: '/students', label: 'Student Records', icon: '👤', roles: ['*'] },
    { path: '/data-imports', label: 'Data Imports', icon: '📁', roles: ['system_admin', 'registry'] },
    { path: '/analytics', label: 'Academic Analytics', icon: '📈', roles: ['*'] },
    { path: '/risk-monitoring', label: 'Risk Monitoring', icon: '⚠️', roles: ['*'] },
    { path: '/recommendations', label: 'Recommendations', icon: '💡', roles: ['lecturer', 'academic_advisor', 'head_of_department'] },
    { path: '/interventions', label: 'Intervention Tracking', icon: '✅', roles: ['lecturer', 'academic_advisor', 'head_of_department'] },
    { path: '/reports', label: 'Reports', icon: '📄', roles: ['*'] },
    { path: '/users', label: 'User Management', icon: '👥', roles: ['system_admin'] },
    { path: '/models', label: 'Model Management', icon: '🤖', roles: ['system_admin'] },
    { path: '/audit-logs', label: 'Audit Logs', icon: '🔍', roles: ['system_admin', 'registry'] },
    { path: '/settings', label: 'Settings', icon: '⚙️', roles: ['*'] },
  ]

  const hasAccess = (roles: string[]) => {
    if (roles.includes('*')) return true
    return roles.some(role => user.roles.includes(role))
  }

  const filteredItems = menuItems.filter(item => hasAccess(item.roles))

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-2xl font-bold text-primary-600">EduPredict</h1>
        <p className="text-xs text-gray-500 mt-1">Academic Intelligence System</p>
      </div>

      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {filteredItems.map((item) => {
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`
                flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors
                ${isActive
                  ? 'bg-primary-50 text-primary-700 border-r-4 border-primary-600'
                  : 'text-gray-700 hover:bg-gray-100'
                }
              `}
            >
              <span className="mr-3 text-lg">{item.icon}</span>
              {item.label}
            </Link>
          )
        })}
      </nav>

      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center mb-3">
          <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
            <span className="text-primary-700 font-semibold">
              {user.full_name.charAt(0).toUpperCase()}
            </span>
          </div>
          <div className="ml-3 flex-1">
            <p className="text-sm font-medium text-gray-900 truncate">{user.full_name}</p>
            <p className="text-xs text-gray-500 truncate">{user.roles.join(', ')}</p>
          </div>
        </div>
        <button
          onClick={onLogout}
          className="w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          Logout
        </button>
      </div>
    </div>
  )
}

export default Sidebar
