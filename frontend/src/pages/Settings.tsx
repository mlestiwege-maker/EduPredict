import React from 'react'

const Settings: React.FC = () => (
  <div className="page">
    <div><h1 className="page-title">Settings</h1><p className="page-subtitle">System preferences and academic configuration (changes should be audited and institution-approved).</p></div>
    <div className="grid gap-4 lg:grid-cols-2">
      <div className="card card-pad">
        <h3 className="section-title mb-3">Institution & Project</h3>
        <dl className="space-y-2 text-sm">
          <div className="flex justify-between gap-4"><dt className="text-slate-400">Target institution</dt><dd className="text-white font-medium">Bindura University of Science Education (BUSE)</dd></div>
          <div className="flex justify-between gap-4"><dt className="text-slate-400">Mode</dt><dd className="text-amber-200">Tertiary prototype — synthetic data</dd></div>
          <div className="flex justify-between gap-4"><dt className="text-slate-400">Deployment</dt><dd className="text-slate-200">Local (Kali) now; remote-ready design</dd></div>
        </dl>
      </div>
      <div className="card card-pad">
        <h3 className="section-title mb-3">Prediction Configuration</h3>
        <dl className="space-y-2 text-sm">
          <div className="flex justify-between gap-4"><dt className="text-slate-400">Checkpoints</dt><dd className="text-slate-200">Week 0 / 4 / 8 / 12</dd></div>
          <div className="flex justify-between gap-4"><dt className="text-slate-400">Default pass mark</dt><dd className="text-slate-200">50% (confirm with BUSE)</dd></div>
          <div className="flex justify-between gap-4"><dt className="text-slate-400">Risk bands</dt><dd className="text-slate-200">High / Medium / Low (validated)</dd></div>
          <div className="flex justify-between gap-4"><dt className="text-slate-400">Leakage control</dt><dd className="text-emerald-300">Required (checkpoint-safe features)</dd></div>
        </dl>
      </div>
    </div>
  </div>
)
export default Settings
