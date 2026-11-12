import React, { useState } from 'react'
import StatCard from '../components/StatCard'
import api from '../services/api'

const ModelManagement: React.FC = () => {
  const [busy, setBusy] = useState('')
  const [result, setResult] = useState<any>(null)
  const [status, setStatus] = useState<any>(null)
  const run = async (fn: ()=>Promise<any>, label:string) => { setBusy(label); setResult(null); try { const r=await fn(); setResult(r.data) } catch(e:any){ setResult({error:e?.response?.data?.detail||e.message}) } finally { setBusy('') } }
  const train = (cp:string)=>run(()=>api.post(`/predictions/train/${cp}`),`train ${cp}`)
  const predict = (cp:string)=>run(()=>api.post(`/predictions/run/2/${cp}`),`predict ${cp}`)
  const getStatus = ()=>run(async()=>{ const r=await api.get('/predictions/status'); setStatus(r.data); return r.data },'status')
  const rows = (result?.results || result?.selected_metrics && [result.selected_metrics] || []) as any[]
  return (
    <div className="page">
      <div><h1 className="page-title">Model Management & AI</h1><p className="page-subtitle">Train/evaluate 6 models (LR, DT, RF, SVM, Gradient Boosting, MLP) and generate checkpoint predictions on institutional data.</p></div>
      <div className="stat-grid">
        <StatCard title="Models" value={status?.models?.length ?? 0} icon="🤖" color="blue" />
        <StatCard title="Reports" value={status?.reports?.length ?? 0} icon="📄" color="purple" />
        <StatCard title="Dataset Ready" value={status?.dataset_exists ? 'Yes' : '—'} icon="📊" color="green" />
        <StatCard title="Last Summary" value={result?.summary ? `H${result.summary.high}/M${result.summary.medium}/L${result.summary.low}` : '—'} icon="⚠️" color="yellow" />
      </div>
      <div className="card card-pad">
        <h3 className="section-title mb-3">Actions</h3>
        <div className="flex flex-wrap gap-2">
          <button className="btn-secondary" disabled={!!busy} onClick={getStatus}>{busy==='status'?'Working…':'Refresh Status'}</button>
          {['week_0','week_4','week_8','week_12'].map(cp => <button key={'t'+cp} className="btn-secondary" disabled={!!busy} onClick={()=>train(cp)}>{busy===`train ${cp}`?'Training…':`Train ${cp}`}</button>)}
          <button className="btn-primary" disabled={!!busy} onClick={()=>predict('week_4')}>{busy==='predict week_4'?'Running…':'Run Predictions (week_4, period 2)'}</button>
        </div>
        <p className="mt-3 text-xs text-slate-400">Uses checkpoint-safe features (no final-mark leakage), group temporal-style split, recall-oriented thresholding. Gradient Boosting stands in for XGBoost in this local env if XGBoost is unavailable. SHAP-style local factor contributions are generated from model importances/coefficients in this lightweight runtime.</p>
      </div>
      {result && (
        <div className="card card-pad">
          <h3 className="section-title mb-3">Result</h3>
          {result.error ? <div className="text-rose-300 text-sm">{result.error}</div> : (
            <div className="space-y-3 text-sm">
              {result.selected_model && <div><span className="text-slate-400">Selected model:</span> <b className="text-white">{result.selected_model}</b> · records {result.n_records} · test {result.n_test}</div>}
              {result.model_name && result.summary && <div><span className="text-slate-400">Prediction run:</span> <b className="text-white">{result.model_name}</b> · total {result.total_predictions} · High {result.summary.high} / Medium {result.summary.medium} / Low {result.summary.low}</div>}
              
              {!!rows.length && <div className="table-wrap"><table className="table"><thead><tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>ROC-AUC</th><th>Brier</th></tr></thead><tbody>{rows.map((r:any,i:number)=>(<tr key={i}><td className="font-medium text-white">{r.model}</td><td>{r.accuracy}</td><td>{r.precision}</td><td>{r.recall}</td><td>{r.f1}</td><td>{r.roc_auc}</td><td>{r.brier}</td></tr>))}</tbody></table></div>}
              <pre className="overflow-auto rounded-xl bg-slate-950/60 p-3 text-xs text-slate-300 max-h-72">{JSON.stringify(result, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
export default ModelManagement
