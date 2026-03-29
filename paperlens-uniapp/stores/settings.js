/**
 * 设置状态管理
 */

import { defineStore } from 'pinia'
import { getSettings, updateSettings } from '../api/settings.js'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    // 兴趣方向
    categories: [],
    // 每日推送数量
    dailyCount: 5,
    // 推送开关
    pushEnabled: true,
    // 推送时间
    pushTime: '08:00',
    // 语言
    language: 'zh',
    // LLM 配置
    llmBaseUrl: '',
    llmModelName: '',
    llmApiKeySet: false,
    // 加载状态
    loading: false
  }),

  getters: {
    /**
     * 是否已配置 LLM
     */
    hasLLMConfig: (state) => {
      return state.llmApiKeySet && state.llmBaseUrl && state.llmModelName
    },

    /**
     * 选中的分类数量
     */
    categoryCount: (state) => state.categories.length
  },

  actions: {
    /**
     * 获取设置
     */
    async fetchSettings() {
      this.loading = true
      try {
        const res = await getSettings()
        if (res.code === 200 && res.data) {
          this.categories = res.data.preferred_categories || []
          this.dailyCount = res.data.daily_count || 5
          this.pushEnabled = res.data.push_enabled ?? true
          this.pushTime = res.data.push_time || '08:00'
          this.language = res.data.language || 'zh'
          this.llmBaseUrl = res.data.llm_base_url || ''
          this.llmModelName = res.data.llm_model_name || ''
          this.llmApiKeySet = res.data.llm_api_key_set || false
        }
        return res
      } catch (e) {
        console.error('获取设置失败', e)
        return { code: 500, msg: '获取失败', data: null }
      } finally {
        this.loading = false
      }
    },

    /**
     * 更新设置
     * @param {object} data - 设置数据
     */
    async saveSettings(data) {
      try {
        const res = await updateSettings(data)
        if (res.code === 200) {
          // 更新本地状态
          if (data.preferred_categories !== undefined) {
            this.categories = data.preferred_categories
          }
          if (data.daily_count !== undefined) {
            this.dailyCount = data.daily_count
          }
          if (data.push_enabled !== undefined) {
            this.pushEnabled = data.push_enabled
          }
          if (data.push_time !== undefined) {
            this.pushTime = data.push_time
          }
          if (data.language !== undefined) {
            this.language = data.language
          }
          if (data.llm_base_url !== undefined) {
            this.llmBaseUrl = data.llm_base_url
          }
          if (data.llm_model_name !== undefined) {
            this.llmModelName = data.llm_model_name
          }
          if (data.llm_api_key) {
            this.llmApiKeySet = true
          }
        }
        return res
      } catch (e) {
        console.error('保存设置失败', e)
        return { code: 500, msg: '保存失败', data: null }
      }
    },

    /**
     * 切换分类选择
     * @param {string} category - 分类
     */
    toggleCategory(category) {
      const index = this.categories.indexOf(category)
      if (index > -1) {
        this.categories.splice(index, 1)
      } else if (this.categories.length < 5) {
        this.categories.push(category)
      }
    },

    /**
     * 设置每日推送数量
     * @param {number} count - 数量（1-10）
     */
    setDailyCount(count) {
      this.dailyCount = Math.max(1, Math.min(10, count))
    }
  }
})