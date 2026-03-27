/**
 * 设置相关 API
 */

import { request } from './client'

/**
 * 获取用户设置
 * @returns {Promise}
 */
export function getSettings() {
  return request('/settings')
}

/**
 * 更新用户设置
 * @param {object} data - 设置数据
 * @returns {Promise}
 */
export function updateSettings(data) {
  return request('/settings', {
    method: 'PUT',
    data
  })
}

/**
 * 测试 LLM 连通性
 * @returns {Promise}
 */
export function testLLM() {
  return request('/settings/test-llm', {
    method: 'POST'
  })
}