/**
 * API 请求封装
 * 自动注入 Token，统一处理响应
 */

// const BASE_URL = 'https://api.paperlens.io/api/v1'
const BASE_URL = 'http://localhost:8000/api/v1'  // 开发环境

/**
 * 封装 uni.request
 * @param {string} url - 相对路径
 * @param {object} options - 请求配置
 * @returns {Promise} - 返回 res.data
 */
export function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token')

    uni.request({
      url: `${BASE_URL}${url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.header
      },
      success: (res) => {
        // 处理 HTTP 状态码
        if (res.statusCode === 401) {
          // Token 过期，清除本地存储
          uni.removeStorageSync('token')
          uni.removeStorageSync('userId')
          resolve({ code: 401, msg: '登录已过期', data: null })
        } else {
          resolve(res.data)
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}