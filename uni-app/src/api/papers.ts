import { request } from './client'
import type { Paper, ApiResponse } from '@/types'

export function getPapers(params: {
  category?: string
  q?: string
  page?: number
  size?: number
}): Promise<ApiResponse<Paper[]>> {
  const query = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(String(v))}`)
    .join('&')
  return request(`/papers${query ? '?' + query : ''}`)
}

export function getTodayPapers(): Promise<ApiResponse<Paper[]>> {
  return request('/papers/today')
}

export function getPaper(id: string): Promise<ApiResponse<Paper>> {
  return request(`/papers/${encodeURIComponent(id)}`)
}