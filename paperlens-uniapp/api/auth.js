/**
 * 认证相关 API
 */

import { request } from './client'

/**
 * 微信登录
 * @param {string} code - wx.login() 返回的 code
 * @returns {Promise}
 */
export function wxLogin(code) {
  return request('/auth/wx-login', {
    method: 'POST',
    data: { code }
  })
}