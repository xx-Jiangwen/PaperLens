import type { ApiResponse } from '@/types'
import { useUserStore } from '@/stores/user'

const BASE_URL = 'https://your-api-domain.com/api/v1'

interface RequestConfig {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, unknown>
  header?: Record<string, string>
}

export function request<T>(url: string, config: RequestConfig = {}): Promise<ApiResponse<T>> {
  return new Promise((resolve, reject) => {
    const userStore = useUserStore()
    const token = userStore.token

    uni.request({
      url: BASE_URL + url,
      method: config.method || 'GET',
      data: config.data,
      header: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...config.header,
      },
      success: (res) => {
        resolve(res.data as ApiResponse<T>)
      },
      fail: (err) => {
        reject(err)
      },
    })
  })
}