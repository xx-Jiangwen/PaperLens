/**
 * 用户状态管理
 */

import { wxLogin } from '../api/auth'

const userStore = {
  state: {
    token: null,
    userId: null
  },

  /**
   * 初始化状态（从本地存储恢复）
   */
  init() {
    this.state.token = uni.getStorageSync('token') || null
    this.state.userId = uni.getStorageSync('userId') || null
  },

  /**
   * 设置 Token
   * @param {string} token
   * @param {number} userId
   */
  setToken(token, userId) {
    this.state.token = token
    this.state.userId = userId
    uni.setStorageSync('token', token)
    uni.setStorageSync('userId', userId)
  },

  /**
   * 清除状态
   */
  clear() {
    this.state.token = null
    this.state.userId = null
    uni.removeStorageSync('token')
    uni.removeStorageSync('userId')
  },

  /**
   * 是否已登录
   */
  isLoggedIn() {
    return !!this.state.token
  },

  /**
   * 执行微信登录
   * @returns {Promise<boolean>}
   */
  async performWxLogin() {
    try {
      // 获取微信登录 code
      const loginRes = await new Promise((resolve, reject) => {
        uni.login({
          success: resolve,
          fail: reject
        })
      })

      if (!loginRes.code) {
        return false
      }

      // 发送到后端换取 Token
      const res = await wxLogin(loginRes.code)

      if (res.code === 200 && res.data) {
        this.setToken(res.data.token, res.data.user_id)
        return true
      }

      return false
    } catch (e) {
      console.error('微信登录失败', e)
      return false
    }
  },

  /**
   * 确保已登录
   * @returns {Promise<boolean>}
   */
  async ensureLoggedIn() {
    if (this.isLoggedIn()) {
      return true
    }
    return this.performWxLogin()
  }
}

export default userStore