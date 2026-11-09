import React, { useEffect, useState } from 'react'
import api from '../services/api'

const badge = (p:string)=>p==='High'?'badge-red':p==='Medium'?'badge-yellow':'badge-green'
const Recommendations: React.FC = () => {
  const [rows,setRows]=useState<any[]>([]); const [msg,setMsg]=useState('')
  useEffect(()=>{(async()=>{ try{ const r=await api.get('/recommendations/generated',{params:{period_id:2,checkpoint:'week_4'}}); setRows(r.data?.items||[]) } catch(e:any){ setMsg(e?.response?.data?.detail||'Run predictions first.') } })()},[])
  return (
    <div className="page">
      <div><h1 className="page-title">Recommendations</h1><p className="page-subtitle">Rule-based, staff-reviewable interventions generated from risk predictions. Decision support only.</p></div>
      {msg && <div className="card card-pad border-amber-500/20 text-amber-100">{msg}</div>}
      <div className="card overflow-hidden">
        <div className="border-b border-slate-700/60 px-5 py-4"><h3 className="section-title">Suggested Actions ({rows.length})</h3></div>
        {rows.length===0 ? <div className="empty">No recommendations yet.</div> : <div className="table-wrap"><table className="table"><thead><tr><th>Student</th><th>Course</th><th>Risk</th><th>Rule</th><th>Action</th><th>Responsible</th><th>Priority</th><th>Status</th></tr></thead><tbody>{rows.slice(0,150).map((r,i)=>(<tr key={i}><td className="font-medium text-white">{r.student_pseudonym}</td><td>{r.course_code}</td><td><span className={`badge ${r.risk_band==='high'?'badge-red':'badge-yellow'}`}>{Math.round(r.risk_probability*100)}% {r.risk_band}</span></td><td>{r.rule}</td><td>{r.action}</td><td>{r.responsible_role}</td><td><span className={`badge ${badge(r.priority)}`}>{r.priority}</span></td><td><span className="badge badge-blue">{r.status}</span></td></tr>))}</tbody></table></div>}
      </div>
    </div>
  )
}
export default Recommendations
