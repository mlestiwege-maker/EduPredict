import React, { useEffect, useState } from 'react'
import StatCard from '../components/StatCard'
import api from '../services/api'

const AcademicAnalytics: React.FC = () => {
  const [s,setS]=useState<any>(null)
  useEffect(()=>{(async()=>{ try{ setS((await api.get('/analytics/summary')).data) } catch{} })()},[])
  return (
    <div className="page">
      <div><h1 className="page-title">Academic Analytics</h1><p className="page-subtitle">Descriptive academic indicators from institutional data.</p></div>
      <div className="stat-grid">
        <StatCard title="Total Students" value={s?.total_students ?? '—'} icon="🎓" color="blue"/>
        <StatCard title="Average Mark" value={s ? `${s.overall_average_mark}%` : '—'} icon="📈" color="green"/>
        <StatCard title="Avg Attendance" value={s ? `${s.overall_attendance_rate}%` : '—'} icon="📅" color="purple"/>
        <StatCard title="Submission Rate" value={s ? `${s.overall_submission_rate}%` : '—'} icon="📝" color="indigo"/>
      </div>
      <div className="card card-pad"><h3 className="section-title mb-2">Source</h3><p className="text-sm text-slate-300">{s?.data_source || 'Institutional academic records'}</p></div>
    </div>
  )
}
export default AcademicAnalytics
