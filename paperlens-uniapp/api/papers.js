/**
 * 论文相关 API
 */

import { request } from './client'

/**
 * 获取今日论文
 * @returns {Promise}
 */
export function getTodayPapers() {
  return request('/papers/today')
}

/**
 * 获取论文列表（支持筛选）
 * @param {object} params - { category?, q?, page?, size? }
 * @returns {Promise}
 */
export function getPapers(params = {}) {
  const queryParts = []

  if (params.category) queryParts.push(`category=${encodeURIComponent(params.category)}`)
  if (params.q) queryParts.push(`q=${encodeURIComponent(params.q)}`)
  if (params.page) queryParts.push(`page=${params.page}`)
  if (params.size) queryParts.push(`size=${params.size}`)

  const queryString = queryParts.length > 0 ? `?${queryParts.join('&')}` : ''
  return request(`/papers${queryString}`)
}

/**
 * 搜索论文
 * @param {string} query - 搜索关键词
 * @param {object} options - { page?, size? }
 * @returns {Promise}
 */
export function searchPapers(query, options = {}) {
  return getPapers({ q: query, ...options })
}

/**
 * 获取论文详情
 * @param {string} id - 论文 ID
 * @returns {Promise}
 */
export function getPaper(id) {
  return request(`/papers/${encodeURIComponent(id)}`)
}