const BASE_URL = 'https://your-api-domain.com/api/v1' // 生产环境替换

/**
 * 封装 wx.request，自动注入 Token，返回 Promise
 */
function request(url, method = 'GET', data = {}) {
  return new Promise((resolve, reject) => {
    const token = wx.getStorageSync('token')
    wx.request({
      url: BASE_URL + url,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      success: (res) => resolve(res.data),
      fail: reject,
    })
  })
}

module.exports = { request }
