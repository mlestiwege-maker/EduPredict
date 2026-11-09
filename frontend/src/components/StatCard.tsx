import React from 'react'

interface StatCardProps {
  title: string
  value: number | string
  icon: string
  color: 'blue' | 'green' | 'red' | 'yellow' | 'purple' | 'indigo' | 'pink'
  trend?: string
  trendUp?: boolean
}

const tones: Record<string, string> = {
  blue: 'from-blue-500/25 to-blue-600/10 text-blue-300',
  green: 'from-emerald-500/25 to-emerald-600/10 text-emerald-300',
  red: 'from-rose-500/25 to-rose-600/10 text-rose-300',
  yellow: 'from-amber-500/25 to-amber-600/10 text-amber-300',
  purple: 'from-violet-500/25 to-violet-600/10 text-violet-300',
  indigo: 'from-indigo-500/25 to-indigo-600/10 text-indigo-300',
  pink: 'from-pink-500/25 to-pink-600/10 text-pink-300',
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color, trend, trendUp }) => (
  <div className="card card-pad">
    <div className="flex items-start justify-between gap-4">
      <div className="min-w-0">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{title}</p>
        <p className="mt-2 text-3xl font-extrabold text-white leading-none">{value}</p>
        {trend && <p className={`mt-2 text-sm ${trendUp ? 'text-emerald-300' : 'text-rose-300'}`}>{trendUp ? '↑' : '↓'} {trend}</p>}
      </div>
      <div className={`shrink-0 h-12 w-12 rounded-xl bg-gradient-to-br ${tones[color]} grid place-items-center text-2xl`}>{icon}</div>
    </div>
  </div>
)

export default StatCard
