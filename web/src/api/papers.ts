import client from './client'
import type { Paper, ApiResponse } from '../types/paper'

export const getPapers = (params: {
  category?: string
  q?: string
  page?: number
  size?: number
}) => client.get<ApiResponse<Paper[]>>('/papers', { params })

export const getTodayPapers = () => client.get<ApiResponse<Paper[]>>('/papers/today')

export const getPaper = (id: string) => client.get<ApiResponse<Paper>>(`/papers/${id}`)

export const searchPapers = (q: string, max = 10) =>
  client.post<ApiResponse<Paper[]>>('/papers/search', { q, max })
