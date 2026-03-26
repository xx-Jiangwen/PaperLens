<template>
  <div class="settings">
    <h1>设置</h1>
    <section>
      <h2>大模型配置（BYOK）</h2>
      <p class="hint">填入你自己的 API Key，支持 OpenAI、DeepSeek、本地 Ollama 等兼容 OpenAI 协议的模型。</p>

      <label>API Base URL</label>
      <input v-model="form.llm_base_url" placeholder="https://api.openai.com/v1" />

      <label>Model Name</label>
      <input v-model="form.llm_model_name" placeholder="gpt-4o-mini" />

      <label>API Key</label>
      <input v-model="form.llm_api_key" type="password"
             :placeholder="settingsStore.llmApiKeySet ? '已设置（留空不修改）' : '输入 API Key'" />

      <button @click="testLLM" :disabled="testing">{{ testing ? '测试中...' : '测试连通性' }}</button>
      <span class="test-result">{{ testResult }}</span>
    </section>

    <section>
      <h2>阅读偏好</h2>
      <label>摘要语言</label>
      <select v-model="form.language">
        <option value="zh">中文</option>
        <option value="en">English</option>
      </select>
    </section>

    <button class="save-btn" @click="save">保存设置</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '../stores/settings'
import client from '../api/client'

const settingsStore = useSettingsStore()
const form = ref({ llm_base_url: '', llm_model_name: '', llm_api_key: '', language: 'zh' as 'zh' | 'en' })
const testing = ref(false)
const testResult = ref('')

onMounted(async () => {
  await settingsStore.fetchSettings()
  form.value.llm_base_url = settingsStore.llmBaseUrl
  form.value.llm_model_name = settingsStore.llmModelName
  form.value.language = settingsStore.language
})

async function testLLM() {
  testing.value = true
  testResult.value = ''
  try {
    const { data } = await client.post('/settings/test-llm')
    testResult.value = data.msg
  } finally {
    testing.value = false
  }
}

async function save() {
  const payload: Record<string, unknown> = {
    llm_base_url: form.value.llm_base_url,
    llm_model_name: form.value.llm_model_name,
    language: form.value.language,
  }
  if (form.value.llm_api_key) payload.llm_api_key = form.value.llm_api_key
  await settingsStore.saveSettings(payload)
  alert('保存成功')
}
</script>
