import React, { useEffect, useState } from 'react'
import StatCard from '../components/StatCard'
import api from '../services/api'

const RiskMonitoring: React.FC = () => {
  const [band,setBand]=useState<'all'|'high'|'medium'|'low'>('all')
  const [rows,setRows]=useState<any[]>([]); const [busy,setBusy]=useState(false); const [msg,setMsg]=useState('')
  const load=async(b=band)=>{ setBusy(true); setMsg(''); try{ const r=await api.get('/predictions/at-risk',{params:{period_id:2,checkpoint:'week_4',risk_band:b}}); setRows(r.data||[]) } catch(e:any){ setMsg(e?.response?.data?.detail||'Load predictions first (Model Management → Run Predictions).') } finally{ setBusy(false) } }
  useEffect(()=>{ load('all') },[])
  return (
    <div className="page">
      <div><h1 className="page-title">Risk Monitoring</h1><p className="page-subtitle">Early-warning predictions (Week 4, synthetic BUSE demo). Estimates support staff decisions; they are not verdicts.</p></div>
      <div className="stat-grid">
        <StatCard title="Flagged" value={rows.length} icon="⚠️" color="red" />
        <StatCard title="High" value={rows.filter(r=>r.risk_band==='high').length} icon="🔴" color="red" />
        <StatCard title="Medium" value={rows.filter(r=>r.risk_band==='medium').length} icon="🟡" color="yellow" />
        <StatCard title="Low" value={rows.filter(r=>r.risk_band==='low').length} icon="🟢" color="green" />
      </div>
      <div className="card overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-700/60 px-5 py-4">
          <h3 className="section-title">At-Risk Students</h3>
          <div className="flex flex-wrap gap-2">{(['all','high','medium','low'] as const).map(b=> <button key={b} className={band===b?'btn-primary':'btn-secondary'} onClick={()=>{setBand(b); load(b)}}>{b[0].toUpperCase()+b.slice(1)}</button>)}<button className="btn-secondary" onClick={()=>load(band)}>Refresh</button></div>
        </div>
        {msg && <div className="px-5 pt-4 text-sm text-amber-100">{msg}</div>}
        {busy ? <div className="empty">Loading…</div> : rows.length===0 ? <div className="empty">No predictions found. Go to Model Management and click “Run Predictions”.</div> : (
          <div className="table-wrap"><table className="table"><thead><tr><th>Student</th><th>Course</th><th>Checkpoint</th><th>Risk</th><th>Band</th><th>Outcome (est.)</th><th>Confidence</th><th>Model</th></tr></thead><tbody>{rows.slice(0,150).map((r:any)=>(<tr key={r.id}><td className="font-medium text-white">{r.student_pseudonym}</td><td>{r.course_code}</td><td>{r.checkpoint}</td><td>{Math.round(r.risk_probability*100)}%</td><td><span className={`badge ${r.risk_band==='high'?'badge-red':r.risk_band==='medium'?'badge-yellow':'badge-green'}`}>{r.risk_band}</span></td><td>{r.predicted_outcome}</td><td>{Math.round((r.confidence_score||0)*100)}%</td><td className="text-slate-400">{r.model_version}</td></tr>))}</tbody></table></div>
        )}
      </div>
    </div>
  )
}
export default RiskMonitoring
