import React, { useEffect, useState } from 'react'
import StatCard from '../components/StatCard'
import api from '../services/api'

const StudentRecords: React.FC = () => {
  const [students, setStudents] = useState<any[]>([]); const [loading,setLoading]=useState(true); const [err,setErr]=useState('')
  useEffect(()=>{(async()=>{ try{ const res=await api.get('/academic/students',{params:{limit:200}}); setStudents(Array.isArray(res.data)?res.data:(res.data?.items||[])) } catch(e:any){ setErr(e?.response?.data?.detail||'Could not load students. Use Data Imports → Load Institutional Dataset.') } finally{ setLoading(false) } })()},[])
  return (
    <div className="page">
      <div><h1 className="page-title">Student Records</h1><p className="page-subtitle">Pseudonymised student records (scope-filtered by role).</p></div>
      <div className="stat-grid"><StatCard title="Records" value={students.length} icon="👥" color="blue"/><StatCard title="Active" value={students.filter(s=>s.enrollment_status==='Active').length} icon="✅" color="green"/><StatCard title="Year 1" value={students.filter(s=>s.year_of_study===1).length} icon="🎓" color="purple"/><StatCard title="Other Years" value={students.filter(s=>s.year_of_study && s.year_of_study!==1).length} icon="📚" color="indigo"/></div>
      {err && <div className="card card-pad border-amber-500/20 text-amber-100">{err}</div>}
      <div className="card overflow-hidden"><div className="border-b border-slate-700/60 px-5 py-4"><h3 className="section-title">Student List</h3></div>
        {loading?<div className="empty">Loading…</div>:students.length===0?<div className="empty">No records loaded. Use Data Imports → Load Institutional Dataset.</div>:(
          <div className="table-wrap"><table className="table"><thead><tr><th>Pseudonym</th><th>Year</th><th>Status</th><th>Gender</th><th>Residence</th><th>Funding</th></tr></thead><tbody>{students.map((s:any)=>(<tr key={s.id}><td className="font-medium text-white">{s.pseudonym}</td><td>Year {s.year_of_study}</td><td><span className="badge badge-green">{s.enrollment_status}</span></td><td>{s.gender||'—'}</td><td>{s.residence_type||'—'}</td><td>{s.funding_type||'—'}</td></tr>))}</tbody></table></div>
        )}
      </div>
    </div>
  )
}
export default StudentRecords
