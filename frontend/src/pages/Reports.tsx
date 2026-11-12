import React, { useEffect, useState } from 'react'
import api from '../services/api'

const reports=[
  {type:'course_risk',name:'Course Risk Report',scope:'Lecturer'},
  {type:'advisee_profile',name:'Advisee Profile',scope:'Academic Advisor'},
  {type:'department_summary',name:'Department Summary',scope:'Head of Department'},
  {type:'faculty_overview',name:'Faculty Overview',scope:'Dean'},
  {type:'cohort_progression',name:'Cohort & Progression',scope:'Registry Staff'},
  {type:'data_quality',name:'Data Quality Report',scope:'Registry / Admin'},
]

const Reports: React.FC = () => {
  const [jobs,setJobs]=useState<any[]>([])
  const [msg,setMsg]=useState('')
  const [busy,setBusy]=useState<string|null>(null)
  const [dlBusy,setDLBusy]=useState<number|null>(null)

  const load=async()=>{ try{ const r=await api.get('/reports/'); setJobs(r.data||[]) } catch{} }
  useEffect(()=>{load()},[])

  const gen=async(type:string)=>{ setBusy(type); setMsg(''); try{ const r=await api.post('/reports/generate',{report_type:type,report_format:'excel',period_id:2,checkpoint:'week_4'}); setMsg(`Generated: ${r.data.title} (${r.data.rows} rows).`); load() } catch(e:any){ setMsg(e?.response?.data?.detail||'Generate failed') } finally{ setBusy(null) } }

  const download=async(id:number)=>{ setDLBusy(id); try{
    const res=await api.get(`/reports/${id}/download`,{responseType:'blob'})
    const url=window.URL.createObjectURL(new Blob([res.data]))
    const a=document.createElement('a')
    a.href=url
    const disp=res.headers['content-disposition']||''
    const fname=disp.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)?.[1]?.replace(/['"]/g,'') || `report_${id}.xlsx`
    a.download=fname
    document.body.appendChild(a); a.click(); document.body.removeChild(a); window.URL.revokeObjectURL(url)
  } catch(e:any){ setMsg(e?.response?.data?.detail||'Download failed') } finally{ setDLBusy(null) } }

  return (
    <div className="page">
      <div><h1 className="page-title">Reports</h1><p className="page-subtitle">Generate role-scoped Excel reports from predictions and data.</p></div>
      {msg && <div className={`card card-pad ${msg.startsWith('Generated')?'border-emerald-500/20 text-emerald-100':'border-amber-500/20 text-amber-100'}`}>{msg}</div>}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{reports.map(r=>(<div key={r.type} className="card card-pad flex flex-col"><div className="flex items-start justify-between gap-3"><h3 className="section-title text-base">{r.name}</h3><span className="badge badge-blue">{r.scope}</span></div><div className="mt-4"><button className="btn-primary w-full" disabled={!!busy} onClick={()=>gen(r.type)}>{busy===r.type?'Generating…':'Generate Excel'}</button></div></div>))}</div>
      <div className="card overflow-hidden"><div className="border-b border-slate-700/60 px-5 py-4"><h3 className="section-title">Generated Reports</h3></div>{jobs.length===0?<div className="empty">No reports generated yet. Click "Generate Excel" above to create one.</div>:<div className="table-wrap"><table className="table"><thead><tr><th>ID</th><th>Title</th><th>Type</th><th>Status</th><th>Generated</th><th>Download</th></tr></thead><tbody>{jobs.map(j=>(<tr key={j.id}><td>{j.id}</td><td className="text-white font-medium">{j.title}</td><td>{j.report_type}</td><td><span className={`badge ${j.status==='completed'?'badge-green':'badge-yellow'}`}>{j.status}</span></td><td className="text-slate-400">{String(j.generated_at||'').replace('T',' ').slice(0,19)}</td><td><button className="btn-secondary w-full" disabled={dlBusy===j.id} onClick={()=>download(j.id)}>{dlBusy===j.id?'Downloading…':'Download'}</button></td></tr>))}</tbody></table></div>}</div>
    </div>
  )
}
export default Reports