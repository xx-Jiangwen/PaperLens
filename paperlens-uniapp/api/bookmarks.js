/**
 * 收藏相关 API
 */

import { request } from './client.js'

/**
 * 获取收藏列表
 * @param {object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.size - 每页数量
 * @returns {Promise}
 */
export function getBookmarks(params = {}) {
  const queryParts = []
  if (params.page) queryParts.push(`page=${params.page}`)
  if (params.size) queryParts.push(`size=${params.size}`)
  const queryString = queryParts.length > 0 ? `?${queryParts.join('&')}` : ''
  return request(`/bookmarks${queryString}`)
}

/**
 * 添加收藏
 * @param {string} paperId - 论文 ID
 * @returns {Promise}
 */
export function addBookmark(paperId) {
  return request(`/bookmarks/${encodeURIComponent(paperId)}`, {
    method: 'POST'
  })
}

/**
 * 取消收藏
 * @param {string} paperId - 论文 ID
 * @returns {Promise}
 */
export function removeBookmark(paperId) {
  return request(`/bookmarks/${encodeURIComponent(paperId)}`, {
    method: 'DELETE'
  })
}