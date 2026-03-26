const { getTodayPapers, getPapers } = require('../../api/papers')

Page({
  data: {
    papers: [],
    loading: false,
    activeCategory: '',
    categories: ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML'],
  },

  onLoad() {
    this.fetchPapers()
  },

  onPullDownRefresh() {
    this.fetchPapers().finally(() => wx.stopPullDownRefresh())
  },

  async fetchPapers() {
    this.setData({ loading: true })
    try {
      const res = await getTodayPapers()
      this.setData({ papers: res.data || [] })
    } catch (e) {
      wx.showToast({ title: '加载失败', icon: 'error' })
    } finally {
      this.setData({ loading: false })
    }
  },

  onCategoryTap(e) {
    const cat = e.currentTarget.dataset.cat
    this.setData({ activeCategory: cat })
    getPapers({ category: cat || undefined }).then((res) => {
      this.setData({ papers: res.data || [] })
    })
  },

  onPaperTap(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({ url: `/pages/detail/detail?id=${encodeURIComponent(id)}` })
  },
})
