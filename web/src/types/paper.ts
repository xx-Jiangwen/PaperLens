export interface Paper {
  id: string
  title: string
  authors: string[]
  abstract: string
  published_at: string | null
  categories: string[]
  primary_category: string | null
  url: string | null
  pdf_url: string | null
  comment: string | null
  summary_status: 'pending' | 'processing' | 'done' | 'failed'
  summary_what: string | null  // AI 摘要内容
}

export interface UserSettings {
  llm_base_url: string | null
  llm_model_name: string | null
  llm_api_key_set: boolean
  preferred_categories: string[]
  language: 'zh' | 'en'
  daily_digest: boolean
}

export interface ApiResponse<T> {
  code: number
  msg: string
  data: T
}
