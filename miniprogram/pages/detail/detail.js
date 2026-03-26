const { getPaper } = require('../../api/papers')

const BASE_URL = 'https://your-api-domain.com/api/v1'

Page({
  data: {
    paper: null,
    summary: { what: '', how: '', why: '' },
    generating: false,
  },

  onLoad(options) {
    const id = decodeURIComponent(options.id)
    getPaper(id).then((res) => {
      const paper = res.data
      this.setData({ paper })
      if (paper.summary_status === 'done') {
        this.setData({
          summary: { what: paper.summary_what, how: paper.summary_how, why: paper.summary_why },
        })
      }
    })
  },

  openPdf() {
    const { pdf_url } = this.data.paper
    if (pdf_url) wx.navigateTo({ url: `/pages/pdf/pdf?url=${encodeURIComponent(pdf_url)}` })
  },

  openArxiv() {
    const { url } = this.data.paper
    if (url) wx.setClipboardData({ data: url, success: () => wx.showToast({ title: '链接已复制' }) })
  },

  // V1.0：微信内置 TTS 朗读摘要
  speakSummary() {
    const { what, how, why } = this.data.summary
    const text = `问题与方案：${what}。技术路径：${how}。贡献与意义：${why}`
    // 微信小程序使用 wx.createInnerAudioContext + TTS（需使用云函数或第三方）
    // V1.0 先用微信截图/复制文字方案，V2.0 接入 BaseTTS
    wx.setClipboardData({ data: text, success: () => wx.showToast({ title: '摘要已复制' }) })
  },
})
