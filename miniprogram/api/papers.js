const { request } = require('./client')

const getPapers = (params = {}) => {
  const query = Object.entries(params)
    .filter(([, v]) => v)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return request(`/papers${query ? '?' + query : ''}`)
}

const getTodayPapers = () => request('/papers/today')
const getPaper = (id) => request(`/papers/${encodeURIComponent(id)}`)

module.exports = { getPapers, getTodayPapers, getPaper }
