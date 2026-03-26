import { request } from './client'
import type { WxLoginResponse, UserSettings, ApiResponse } from '@/types'

// 微信登录
export function wxLogin(code: string): Promise<ApiResponse<WxLoginResponse>> {
  return request('/auth/wx-login', {
    method: 'POST',
    data: { code }
  })
}

// 获取用户设置
export function getSettings(): Promise<ApiResponse<UserSettings>> {
  return request('/settings')
}

// 更新用户设置
export function updateSettings(data: Record<string, unknown>): Promise<ApiResponse<null>> {
  return request('/settings', {
    method: 'PUT',
    data
  })
}

// 测试 LLM 连通性
export function testLLM(): Promise<ApiResponse<null>> {
  return request('/settings/test-llm', { method: 'POST' })
}