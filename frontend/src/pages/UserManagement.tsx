import React, { useEffect, useState } from 'react'
import StatCard from '../components/StatCard'
import api from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const ROLES = [
  { key: 'system_admin', label: 'System Administrator', icon: '🛡️', color: 'red' as const },
  { key: 'lecturer', label: 'Lecturer', icon: '👨‍🏫', color: 'blue' as const },
  { key: 'academic_advisor', label: 'Academic Advisor', icon: '💼', color: 'green' as const },
  { key: 'head_of_department', label: 'Head of Department', icon: '🏛️', color: 'purple' as const },
  { key: 'dean', label: 'Dean', icon: '🎓', color: 'indigo' as const },
  { key: 'registry', label: 'Registry Staff', icon: '📄', color: 'yellow' as const },
]

type UserRow = { id: number; email: string; full_name: string; is_active: boolean; roles?: string[] }

const UserManagement: React.FC = () => {
  const { user } = useAuth()
  const [users, setUsers] = useState<UserRow[]>([])
  const [loading, setLoading] = useState(true)
  const [showAdd, setShowAdd] = useState(false)
  const [saving, setSaving] = useState(false)
  const [msg, setMsg] = useState<{ type: 'ok' | 'err'; text: string } | null>(null)
  const [form, setForm] = useState({ email: '', password: '', full_name: '', role_id: 2 })

  const load = async () => {
    setLoading(true)
    try {
      const r = await api.get('/users', { params: { limit: 200 } })
      setUsers(Array.isArray(r.data) ? r.data : (r.data?.items || []))
    } catch (e: any) {
      setUsers([])
      setMsg({ type: 'err', text: e?.response?.data?.detail || 'Could not load users from API.' })
    } finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])

  const addUser = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true); setMsg(null)
    try {
      await api.post('/auth/register', form)
      setMsg({ type: 'ok', text: 'User created.' }); setShowAdd(false); setForm({ email: '', password: '', full_name: '', role_id: 2 }); load()
    } catch (e: any) { setMsg({ type: 'err', text: e?.response?.data?.detail || 'Failed to create user (admin permission required on backend).' }) }
    finally { setSaving(false) }
  }

  const countFor = (role: string) => users.filter(u => (u.roles || []).includes(role)).length

  return (
    <div className="page">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div><h1 className="page-title">User Management</h1><p className="page-subtitle">Manage system accounts and role assignments · signed in as {user?.full_name}</p></div>
        <button className="btn-primary" onClick={() => setShowAdd(v => !v)}>{showAdd ? 'Close' : '+ Add User'}</button>
      </div>

      {msg && <div className={`card card-pad ${msg.type==='ok' ? 'border-emerald-500/30 text-emerald-200' : 'border-amber-500/30 text-amber-100'}`}>{msg.text}</div>}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {ROLES.map(r => <StatCard key={r.key} title={r.label} value={countFor(r.key) || (users.length ? 0 : '—')} icon={r.icon} color={r.color} />)}
      </div>

      {showAdd && (
        <form onSubmit={addUser} className="card card-pad grid gap-4 sm:grid-cols-2">
          <div><label className="block text-sm text-slate-300 mb-1">Full name</label><input required className="w-full px-3 py-2.5" value={form.full_name} onChange={e=>setForm({...form, full_name:e.target.value})} /></div>
          <div><label className="block text-sm text-slate-300 mb-1">Email</label><input required type="email" className="w-full px-3 py-2.5" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} /></div>
          <div><label className="block text-sm text-slate-300 mb-1">Password</label><input required type="password" minLength={6} className="w-full px-3 py-2.5" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} /></div>
          <div><label className="block text-sm text-slate-300 mb-1">Role</label>
            <select className="w-full px-3 py-2.5" value={form.role_id} onChange={e=>setForm({...form, role_id:Number(e.target.value)})}>
              {ROLES.map((r,i)=><option key={r.key} value={i+1}>{r.label}</option>)}
            </select>
          </div>
          <div className="sm:col-span-2"><button disabled={saving} className="btn-primary">{saving?'Saving…':'Create user'}</button></div>
        </form>
      )}

      <div className="card overflow-hidden">
        <div className="flex items-center justify-between gap-3 border-b border-slate-700/60 px-5 py-4">
          <h3 className="section-title">System Users</h3>
          <button className="btn-secondary" onClick={load}>Refresh</button>
        </div>
        {loading ? <div className="empty">Loading users…</div> : users.length === 0 ? <div className="empty">No users found.</div> : (
          <div className="table-wrap"><table className="table">
            <thead><tr><th>Name</th><th>Email</th><th>Role(s)</th><th>Status</th></tr></thead>
            <tbody>{users.map(u => (
              <tr key={u.id}>
                <td className="font-medium text-white">{u.full_name}</td>
                <td className="text-slate-300">{u.email}</td>
                <td>{(u.roles||[]).map(r => <span key={r} className="badge badge-blue mr-1">{ROLES.find(x=>x.key===r)?.label || r}</span>)}</td>
                <td><span className={`badge ${u.is_active ? 'badge-green' : 'badge-red'}`}>{u.is_active ? 'Active' : 'Inactive'}</span></td>
              </tr>
            ))}</tbody>
          </table></div>
        )}
      </div>
    </div>
  )
}
export default UserManagement
