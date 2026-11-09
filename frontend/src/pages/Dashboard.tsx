import { useAuth } from '../contexts/AuthContext'

const Dashboard = () => {
  const { user } = useAuth()
  const role = (user?.roles || [])[0] || 'user'
  const roleTitle: Record<string,string> = { system_admin:'System Administrator', lecturer:'Lecturer', academic_advisor:'Academic Advisor', head_of_department:'Head of Department', dean:'Dean', registry:'Registry Staff' }
  const cardsByRole: Record<string,{title:string;value:string;icon:string;color:string}[]> = {
    lecturer: [ {title:'My Courses',value:'4',icon:'📚',color:'#3b82f6'},{title:'High Risk (My Courses)',value:'12',icon:'⚠️',color:'#ef4444'},{title:'Interventions Due',value:'5',icon:'✅',color:'#10b981'},{title:'Avg Pass Rate',value:'72%',icon:'📈',color:'#f59e0b'} ],
    academic_advisor: [ {title:'Assigned Advisees',value:'48',icon:'🎓',color:'#3b82f6'},{title:'High Risk Advisees',value:'7',icon:'⚠️',color:'#ef4444'},{title:'Follow-ups',value:'9',icon:'📅',color:'#f59e0b'},{title:'Cases Resolved',value:'14',icon:'✅',color:'#10b981'} ],
    head_of_department: [ {title:'Department Courses',value:'18',icon:'🏛️',color:'#3b82f6'},{title:'Students Flagged',value:'41',icon:'⚠️',color:'#ef4444'},{title:'Dept Pass Rate',value:'69%',icon:'📈',color:'#10b981'},{title:'Reports Ready',value:'6',icon:'📄',color:'#f59e0b'} ],
    dean: [ {title:'Programmes',value:'9',icon:'🎓',color:'#3b82f6'},{title:'Faculty At-Risk',value:'128',icon:'⚠️',color:'#ef4444'},{title:'Retention Trend',value:'Stable',icon:'📈',color:'#10b981'},{title:'Term Reports',value:'4',icon:'📄',color:'#f59e0b'} ],
    registry: [ {title:'Cohort Records',value:'3,240',icon:'🗂️',color:'#3b82f6'},{title:'Pending Imports',value:'2',icon:'📁',color:'#f59e0b'},{title:'Data Quality Issues',value:'17',icon:'🔎',color:'#ef4444'},{title:'Progression Reports',value:'8',icon:'📄',color:'#10b981'} ],
  }
  const cards = cardsByRole[role] || [ {title:'Total Students (demo)',value:'1,248',icon:'🎓',color:'#3b82f6'},{title:'High Risk',value:'86',icon:'⚠️',color:'#ef4444'},{title:'Medium Risk',value:'156',icon:'⚡',color:'#f59e0b'},{title:'Low Risk',value:'1,006',icon:'✅',color:'#10b981'} ]

  return (
    <div>
      <div style={{ marginBottom: 22, display:'flex', justifyContent:'space-between', gap:12, flexWrap:'wrap' }}>
        <div>
          <h1 style={{ fontSize: 30, fontWeight: 800, color: 'white', marginBottom: 6 }}>Dashboard</h1>
          <p style={{ color: '#94a3b8', margin:0 }}>{roleTitle[role] || 'User'} · BUSE prototype · synthetic demo indicators</p>
        </div>
        <div style={{ padding:'10px 12px', borderRadius:12, background:'rgba(245,158,11,0.12)', border:'1px solid rgba(245,158,11,0.25)', color:'#fde68a', fontSize:12, maxWidth:520 }}>
          Predictions shown in this prototype are decision-support estimates from configured data/models, not verdicts. Use synthetic data only until BUSE permission, ethics, and data-protection requirements are met.
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16, marginBottom: 22 }}>
        {cards.map((stat, i) => (
          <div key={i} style={{ background: 'rgba(30, 41, 59, 0.7)', border: '1px solid rgba(59, 130, 246, 0.1)', borderRadius: 16, padding: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <p style={{ color: '#94a3b8', fontSize: 13, margin: '0 0 8px' }}>{stat.title}</p>
                <p style={{ color: 'white', fontSize: 32, fontWeight: 800, margin:0 }}>{stat.value}</p>
              </div>
              <div style={{ width: 54, height: 54, borderRadius: 12, background: `${stat.color}22`, display: 'grid', placeItems:'center', fontSize: 26 }}>{stat.icon}</div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(300px,1fr))', gap: 16 }}>
        <div style={{ background: 'rgba(30, 41, 59, 0.7)', border: '1px solid rgba(59, 130, 246, 0.1)', borderRadius: 16, padding: 20 }}>
          <h3 style={{ color: 'white', fontSize: 18, margin: '0 0 14px' }}>Risk Distribution (demo)</h3>
          {[{ label: 'High Risk', value: 86, total: 1248, color: '#ef4444' },{ label: 'Medium Risk', value: 156, total: 1248, color: '#f59e0b' },{ label: 'Low Risk', value: 1006, total: 1248, color: '#10b981' }].map((item) => (
            <div key={item.label} style={{ marginBottom: 14 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize:13 }}>
                <span style={{ color: '#e2e8f0' }}>{item.label}</span>
                <span style={{ color: '#94a3b8' }}>{item.value} ({Math.round(item.value/item.total*100)}%)</span>
              </div>
              <div style={{ width: '100%', height: 8, background: 'rgba(148, 163, 184, 0.2)', borderRadius: 4 }}>
                <div style={{ width: `${item.value/item.total*100}%`, height: '100%', background: item.color, borderRadius:4 }} />
              </div>
            </div>
          ))}
        </div>
        <div style={{ background: 'rgba(30, 41, 59, 0.7)', border: '1px solid rgba(59, 130, 246, 0.1)', borderRadius: 16, padding: 20 }}>
          <h3 style={{ color: 'white', fontSize: 18, margin: '0 0 14px' }}>Next implementation steps</h3>
          <ul style={{ margin:0, paddingLeft:18, color:'#cbd5e1', lineHeight:1.8, fontSize:14 }}>
            <li>Connect dashboards to live `/api/v1` role-scoped endpoints.</li>
            <li>Add synthetic BUSE dataset generator + validated CSV/XLSX import.</li>
            <li>Run 6-model ML pipeline (LR/DT/RF/SVM/XGBoost/MLP), checkpoints W0/4/8/12, SHAP.</li>
            <li>Enable rule-based recommendations, intervention tracking, and PDF/Excel reports.</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
