/**
 * SSE 流式摘要请求封装
 * 用法：
 *   streamSummary(paperId, token, (section, delta) => { ... })
 */
export async function streamSummary(
  paperId: string,
  token: string | null,
  onDelta: (section: 'what' | 'how' | 'why', delta: string) => void,
  onDone: () => void,
  onError: (err: string) => void,
) {
  const url = `/api/v1/ai/summarize/${paperId}/stream`
  const headers: Record<string, string> = {}
  if (token) headers['Authorization'] = `Bearer ${token}`

  const response = await fetch(url, { headers })
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const text = decoder.decode(value)
    for (const line of text.split('\n')) {
      if (!line.startsWith('data: ')) continue
      const payload = line.slice(6).trim()
      if (payload === '[DONE]') { onDone(); return }
      try {
        const data = JSON.parse(payload)
        if (data.error) { onError(data.error); return }
        if (data.section && data.delta) onDelta(data.section, data.delta)
      } catch { /* ignore parse error */ }
    }
  }
}
