export interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
  roles: string[]
  permissions: Record<string, boolean>
}

export interface Student {
  id: number
  pseudonym: string
  programme_id: number
  year_of_study: number
  enrollment_status: string
  age_band?: string
  gender?: string
  residence_type?: string
  funding_type?: string
}

export interface Prediction {
  id: number
  student_id: number
  course_id: number
  period_id: number
  checkpoint: string
  risk_probability: number
  risk_band: string
  predicted_outcome?: string
  confidence_score: number
  model_version: string
}

export interface Recommendation {
  id: number
  student_id: number
  prediction_id: number
  action: string
  responsible_role?: string
  priority: string
  status: string
}

export interface Intervention {
  id: number
  student_id: number
  recommendation_id?: number
  staff_id: number
  intervention_type: string
  description: string
  action_taken?: string
  status: string
  follow_up_date?: string
}
