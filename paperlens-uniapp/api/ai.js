/**
 * AI 相关 API
 */

import config from './config.js'

const BASE_URL = config.apiUrl

/**
 * ArrayBuffer 转 String
 */
function arrayBufferToString(buffer) {
  try {
    // 尝试使用 TextDecoder
    if (typeof TextDecoder !== 'undefined') {
      return new TextDecoder('utf-8').decode(buffer)
    }
    // 降级方案
    const uint8Array = new Uint8Array(buffer)
    let result = ''
    for (let i = 0; i < uint8Array.length; i++) {
      result += String.fromCharCode(uint8Array[i])
    }
    // 处理 UTF-8 多字节字符
    return decodeURIComponent(escape(result))
  } catch (e) {
    console.error('ArrayBuffer 转字符串失败', e)
    return ''
  }
}

/**
 * 解析 SSE 数据行
 */
function parseSSELines(text, callbacks) {
  const lines = text.split('\n')
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6)
      if (data === '[DONE]') {
        callbacks.onDone && callbacks.onDone()
        return true
      }
      try {
        const parsed = JSON.parse(data)
        if (parsed.error) {
          callbacks.onError && callbacks.onError(parsed.error)
          return true
        } else if (parsed.section && parsed.delta) {
          callbacks.onChunk && callbacks.onChunk(parsed.section, parsed.delta)
        }
      } catch (e) {
        // JSON 解析失败，可能是不完整的数据，忽略
      }
    }
  }
  return false
}

/**
 * 流式生成摘要（使用 enableChunked 实现真正的流式）
 * @param {string} paperId - 论文 ID
 * @param {object} callbacks - 回调函数
 */
export function streamSummary(paperId, { onChunk, onDone, onError }) {
  const token = uni.getStorageSync('token')

  // 累积的文本，用于处理跨 chunk 的不完整数据
  let accumulatedText = ''

  const requestTask = uni.request({
    url: `${BASE_URL}/ai/summarize/${encodeURIComponent(paperId)}/stream`,
    method: 'GET',
    responseType: 'arraybuffer',  // 关键：使用 arraybuffer
    enableChunked: true,          // 关键：开启流式传输
    header: {
      'Accept': 'text/event-stream',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    success: (res) => {
      // 请求完成，处理剩余数据
      if (accumulatedText) {
        parseSSELines(accumulatedText, { onChunk, onDone, onError })
      }
    },
    fail: (err) => {
      onError && onError(err.errMsg || '网络错误')
    }
  })

  // 监听数据分块接收事件
  requestTask.onChunkReceived((response) => {
    if (!response.data) return

    // 将 ArrayBuffer 转为字符串
    const chunkText = arrayBufferToString(response.data)
    accumulatedText += chunkText

    // 尝试解析完整的行
    const lines = accumulatedText.split('\n')
    // 最后一个可能是不完整的行，保留
    accumulatedText = lines.pop() || ''

    // 处理完整的行
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        if (data === '[DONE]') {
          onDone && onDone()
          requestTask.abort()  // 停止请求
          return
        }
        try {
          const parsed = JSON.parse(data)
          if (parsed.error) {
            onError && onError(parsed.error)
          } else if (parsed.section && parsed.delta) {
            onChunk && onChunk(parsed.section, parsed.delta)
          }
        } catch (e) {
          // JSON 解析失败，忽略
        }
      }
    }
  })

  return requestTask
}

/**
 * 查询摘要生成状态
 * @param {string} paperId - 论文 ID
 * @returns {Promise}
 */
export function getSummaryStatus(paperId) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token')

    uni.request({
      url: `${BASE_URL}/ai/summarize/${encodeURIComponent(paperId)}/status`,
      method: 'GET',
      header: {
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      },
      success: (res) => {
        resolve(res.data)
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}