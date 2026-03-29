/**
 * 用户相关 API
 */

import { request } from './client.js'

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export function getUserInfo() {
  return request('/users/me')
}

/**
 * 获取用户阅读统计
 * @returns {Promise}
 */
export function getUserStats() {
  return request('/users/stats')
}