import React, { useEffect, useState } from 'react'
import api from '../services/api'
import StatCard from '../components/StatCard'

const InterventionTracking: React.FC = () => {
  const [rows,setRows]=useState<any[]>([]); const [msg,setMsg]=useState('')
  const load=async()=>{ try{ const r=await api.get('/recommendations/interventions'); setRows(r.data||[]) } catch(e:any){ setMsg(e?.response?.data?.detail||'Could not load interventions.') } }
  useEffect(()=>{load()},[])
  return (
    <div className="page">
      <div><h1 className="page-title">Intervention Tracking</h1><p className="page-subtitle">Record staff actions and outcomes for recommended support (auditable workflow).</p></div>
      <div className="stat-grid"><StatCard title="Total" value={rows.length} icon="📋" color="blue"/><StatCard title="Planned" value={rows.filter(r=>r.status==='planned').length} icon="📅" color="yellow"/><StatCard title="In Progress" value={rows.filter(r=>r.status==='in_progress').length} icon="⚡" color="purple"/><StatCard title="Completed" value={rows.filter(r=>r.status==='completed').length} icon="✅" color="green"/></div>
      {msg && <div className="card card-pad border-amber-500/20 text-amber-100">{msg}</div>}
      <div className="card card-pad"><button className="btn-secondary" onClick={load}>Refresh</button><div className="empty mt-3">{rows.length?`${rows.length} intervention(s) recorded.`:'No interventions yet. Accept a recommendation and record action via API/workflow (UI create form can be added next).'}</div></div>
    </div>
  )
}
export default InterventionTracking
