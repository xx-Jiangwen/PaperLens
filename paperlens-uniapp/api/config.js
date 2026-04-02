/**
 * API 配置
 *
 * 开发环境切换：
 * - 模拟器调试：使用 localhost
 * - 真机调试：使用开发机局域网 IP
 */

// 开发环境 BASE_URL
// 模拟器使用 localhost，真机使用局域网 IP
const DEV_BASE_URL = 'http://172.26.126.208:8000'  // 真机调试时改为你的局域网 IP

// 生产环境 BASE_URL
const PROD_BASE_URL = 'https://api.paperlens.io'

// 当前环境
const BASE_URL = process.env.NODE_ENV === 'production' ? PROD_BASE_URL : DEV_BASE_URL

export const config = {
  baseUrl: BASE_URL,
  apiPrefix: '/api/v1',
  // 完整 API 地址
  apiUrl: `${BASE_URL}${'/api/v1'}`,
  // 获取上传地址（用于文件上传等需要完整路径的场景）
  getUploadUrl(path) {
    return `${this.baseUrl}${path}`
  }
}

export default config