import React, { useEffect, useState } from 'react'
import StatCard from '../components/StatCard'
import api from '../services/api'

const AuditLogs: React.FC = () => {
  const [rows,setRows]=useState<any[]>([]); const [total,setTotal]=useState(0)
  useEffect(()=>{(async()=>{ try{ const r=await api.get('/audit',{params:{limit:100}}); setRows(r.data?.items||[]); setTotal(r.data?.total||0) } catch{} })()},[])
  return (
    <div className="page">
      <div><h1 className="page-title">Audit Logs</h1><p className="page-subtitle">Security-relevant access and administrative activity.</p></div>
      <div className="stat-grid"><StatCard title="Total Events" value={total} icon="📝" color="blue"/><StatCard title="Loaded" value={rows.length} icon="🔍" color="purple"/><StatCard title="Success" value={rows.filter(r=>r.status==='success').length} icon="✅" color="green"/><StatCard title="Other" value={rows.filter(r=>r.status!=='success').length} icon="⚡" color="yellow"/></div>
      <div className="card overflow-hidden"><div className="border-b border-slate-700/60 px-5 py-4"><h3 className="section-title">Recent Activity</h3></div>{rows.length===0?<div className="empty">No audit logs yet (or endpoint access limited by role).</div>:<div className="table-wrap"><table className="table"><thead><tr><th>Time</th><th>User</th><th>Action</th><th>Resource</th><th>Status</th></tr></thead><tbody>{rows.map((r:any)=>(<tr key={r.id}><td className="whitespace-nowrap text-slate-400">{String(r.created_at||'').replace('T',' ').slice(0,19)}</td><td>{r.user_id}</td><td><span className="badge badge-blue">{r.action}</span></td><td>{r.resource_type||'—'}</td><td><span className={`badge ${r.status==='success'?'badge-green':'badge-yellow'}`}>{r.status||'—'}</span></td></tr>))}</tbody></table></div>}</div>
    </div>
  )
}
export default AuditLogs
