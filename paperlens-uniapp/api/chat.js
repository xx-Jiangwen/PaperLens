/**
 * AI 对话相关 API
 */

import { request } from './client.js'

/**
 * 与论文对话
 * @param {string} paperId - 论文 ID
 * @param {string} question - 问题
 * @returns {Promise}
 */
export function chatPaper(paperId, question) {
  return request(`/chat/paper/${encodeURIComponent(paperId)}`, {
    method: 'POST',
    data: { question }
  })
}

/**
 * 获取 AI 摘要状态
 * @param {string} paperId - 论文 ID
 * @returns {Promise}
 */
export function getSummaryStatus(paperId) {
  return request(`/ai/summarize/${encodeURIComponent(paperId)}/status`)
}