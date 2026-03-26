const { request } = require('../../api/client')

Page({
  data: {
    form: { llm_base_url: '', llm_model_name: '', llm_api_key: '', language: 'zh' },
    apiKeySet: false,
    testing: false,
  },

  onLoad() {
    request('/settings').then((res) => {
      if (res.data) {
        this.setData({
          'form.llm_base_url': res.data.llm_base_url || '',
          'form.llm_model_name': res.data.llm_model_name || '',
          'form.language': res.data.language || 'zh',
          apiKeySet: res.data.llm_api_key_set,
        })
      }
    })
  },

  onInput(e) {
    const key = e.currentTarget.dataset.key
    this.setData({ [`form.${key}`]: e.detail.value })
  },

  testLLM() {
    this.setData({ testing: true })
    request('/settings/test-llm', 'POST').then((res) => {
      wx.showToast({ title: res.msg, icon: res.code === 200 ? 'success' : 'error' })
    }).finally(() => this.setData({ testing: false }))
  },

  save() {
    const payload = { ...this.data.form }
    if (!payload.llm_api_key) delete payload.llm_api_key
    request('/settings', 'PUT', payload).then(() => {
      wx.showToast({ title: '保存成功', icon: 'success' })
    })
  },
})
