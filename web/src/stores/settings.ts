import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '../api/client'

export const useSettingsStore = defineStore('settings', () => {
  const llmBaseUrl = ref('')
  const llmModelName = ref('')
  const llmApiKeySet = ref(false)
  const preferredCategories = ref<string[]>([])
  const language = ref<'zh' | 'en'>('zh')

  async function fetchSettings() {
    const { data } = await client.get('/settings')
    if (data.data) {
      llmBaseUrl.value = data.data.llm_base_url || ''
      llmModelName.value = data.data.llm_model_name || ''
      llmApiKeySet.value = data.data.llm_api_key_set
      preferredCategories.value = data.data.preferred_categories || []
      language.value = data.data.language || 'zh'
    }
  }

  async function saveSettings(payload: object) {
    await client.put('/settings', payload)
    await fetchSettings()
  }

  return { llmBaseUrl, llmModelName, llmApiKeySet, preferredCategories, language, fetchSettings, saveSettings }
})
