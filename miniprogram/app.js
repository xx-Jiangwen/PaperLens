App({
  globalData: {
    token: null,
    userId: null,
  },

  onLaunch() {
    // 读取本地 Token
    const token = wx.getStorageSync('token')
    if (token) this.globalData.token = token
  },

  /**
   * 微信登录，获取 openid 并换取 JWT Token
   * 在需要登录的页面调用 app.wxLogin()
   */
  wxLogin() {
    return new Promise((resolve, reject) => {
      wx.login({
        success: (res) => {
          wx.request({
            url: 'https://your-api-domain.com/api/v1/auth/wx-login',
            method: 'POST',
            data: { code: res.code },
            success: (resp) => {
              const { token, user_id } = resp.data.data
              this.globalData.token = token
              this.globalData.userId = user_id
              wx.setStorageSync('token', token)
              resolve(token)
            },
            fail: reject,
          })
        },
        fail: reject,
      })
    })
  },
})
