import React, { useState } from 'react'
import StatCard from '../components/StatCard'
import api from '../services/api'

const DataImports: React.FC = () => {
  const [busy,setBusy]=useState(''); const [datasets,setDatasets]=useState<any>(null); const [result,setResult]=useState<any>(null)
  const run=async(label:string, fn:()=>Promise<any>)=>{ setBusy(label); setResult(null); try{ const r=await fn(); setResult(r.data||r) } catch(e:any){ setResult({error:e?.response?.data?.detail||e.message}) } finally{ setBusy('') } }
  return (
    <div className="page">
      <div><h1 className="page-title">Data Imports & Datasets</h1><p className="page-subtitle">Load the synthetic BUSE demo dataset, view recommended public datasets, and use validated imports. No real records without permission/ethics/compliance.</p></div>
      <div className="stat-grid">
        <StatCard title="Demo Dataset" value={result?.counts?.students ?? 'BUSE'} icon="📁" color="blue" />
        <StatCard title="Students" value={result?.counts?.students ?? 0} icon="🎓" color="green" />
        <StatCard title="Enrolments" value={result?.counts?.course_enrolments ?? 0} icon="📚" color="purple" />
        <StatCard title="Assessments" value={result?.counts?.assessment_records ?? 0} icon="📝" color="yellow" />
      </div>
      <div className="card card-pad">
        <h3 className="section-title mb-3">Actions</h3>
        <div className="flex flex-wrap gap-2">
          <button className="btn-primary" disabled={!!busy} onClick={()=>run('load',()=>api.post('/data-import/load-demo'))}>{busy==='load'?'Loading…':'Load Synthetic BUSE Dataset'}</button>
          <button className="btn-secondary" disabled={!!busy} onClick={()=>run('list',async()=>{const r=await api.get('/data-import/datasets'); setDatasets(r.data); return r.data})}>{busy==='list'?'Loading…':'Show Datasets Used / Recommended'}</button>
        </div>
        {result?.counts && <div className="mt-4 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-3 text-sm text-emerald-100">Loaded synthetic demo data: {JSON.stringify(result.counts)}</div>}
        {result?.error && <div className="mt-4 rounded-xl border border-rose-500/20 bg-rose-500/10 p-3 text-sm text-rose-200">{result.error}</div>}
      </div>
      {datasets && <div className="card card-pad space-y-3">
        <h3 className="section-title">Datasets</h3>
        <div><div className="text-sm font-semibold text-white">Currently used (synthetic demo)</div><pre className="mt-2 overflow-auto rounded-xl bg-slate-950/60 p-3 text-xs text-slate-300">{JSON.stringify(datasets.synthetic_datasets, null, 2)}</pre></div>
        <div><div className="text-sm font-semibold text-white">Datasets we could have used (public/research)</div>
          <div className="mt-2 table-wrap"><table className="table"><thead><tr><th>Name</th><th>Why useful</th></tr></thead><tbody>{(datasets.recommended_public_datasets||[]).map((d:any)=>(<tr key={d.name}><td className="font-medium text-white">{d.name}</td><td className="text-slate-300">{d.why}</td></tr>))}</tbody></table></div>
        </div>
        <div className="text-xs text-slate-400">{datasets.note}</div>
      </div>}
    </div>
  )
}
export default DataImports
