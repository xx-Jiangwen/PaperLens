<template>
  <view class="container">
    <view class="section">
      <view class="section-title">大模型配置（BYOK）</view>
      <view class="hint">填入你自己的 API Key，支持 OpenAI、DeepSeek、本地 Ollama 等</view>

      <view class="field">
        <view class="label">API Base URL</view>
        <input
          class="input"
          v-model="form.llm_base_url"
          placeholder="https://api.openai.com/v1"
        />
      </view>

      <view class="field">
        <view class="label">Model Name</view>
        <input
          class="input"
          v-model="form.llm_model_name"
          placeholder="gpt-4o-mini"
        />
      </view>

      <view class="field">
        <view class="label">API Key</view>
        <input
          class="input"
          type="password"
          v-model="form.llm_api_key"
          :placeholder="apiKeySet ? '已设置（留空不修改）' : '输入 API Key'"
        />
      </view>

      <button class="btn-ghost" :loading="testing" @click="testLLM">测试连通性</button>
    </view>

    <button class="btn-primary save-btn" @click="save">保存设置</button>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { request } from '@/api/client'

const form = ref({
  llm_base_url: '',
  llm_model_name: '',
  llm_api_key: '',
  language: 'zh' as 'zh' | 'en'
})

const apiKeySet = ref(false)
const testing = ref(false)

onMounted(async () => {
  try {
    const res = await request<{ llm_base_url: string; llm_model_name: string; llm_api_key_set: boolean; language: string }>('/settings')
    if (res.data) {
      form.value.llm_base_url = res.data.llm_base_url || ''
      form.value.llm_model_name = res.data.llm_model_name || ''
      form.value.language = res.data.language || 'zh'
      apiKeySet.value = res.data.llm_api_key_set
    }
  } catch (e) {
    // 忽略错误，可能是未登录
  }
})

async function testLLM() {
  testing.value = true
  try {
    const res = await request('/settings/test-llm', { method: 'POST' })
    uni.showToast({
      title: res.msg,
      icon: res.code === 200 ? 'success' : 'error'
    })
  } catch (e) {
    uni.showToast({ title: '测试失败', icon: 'error' })
  } finally {
    testing.value = false
  }
}

async function save() {
  const payload: Record<string, unknown> = {
    llm_base_url: form.value.llm_base_url,
    llm_model_name: form.value.llm_model_name,
    language: form.value.language
  }

  if (form.value.llm_api_key) {
    payload.llm_api_key = form.value.llm_api_key
  }

  try {
    await request('/settings', { method: 'PUT', data: payload })
    uni.showToast({ title: '保存成功', icon: 'success' })
    // 更新 apiKeySet 状态
    if (form.value.llm_api_key) {
      apiKeySet.value = true
      form.value.llm_api_key = ''
    }
  } catch (e) {
    uni.showToast({ title: '保存失败', icon: 'error' })
  }
}
</script>

<style lang="scss" scoped>
.container {
  padding: 16px;
}

.section {
  background: #161b22;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.section-title {
  color: #e6edf3;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.hint {
  color: #8b949e;
  font-size: 12px;
  margin-bottom: 20px;
}

.field {
  margin-bottom: 16px;
}

.label {
  color: #c9d1d9;
  font-size: 13px;
  margin-bottom: 8px;
}

.input {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 12px;
  color: #e6edf3;
  font-size: 14px;
  width: 100%;
  box-sizing: border-box;

  &::placeholder {
    color: #6e7681;
  }
}

.btn-ghost {
  background: transparent;
  color: #58a6ff;
  border: 1px solid #30363d;
  border-radius: 8px;
  font-size: 14px;
  margin-top: 8px;
  width: 100%;

  &:active {
    background: #21262d;
  }
}

.btn-primary {
  background: #238636;
  color: #fff;
  border-radius: 8px;
  font-size: 14px;

  &:active {
    background: #2ea043;
  }
}

.save-btn {
  width: 100%;
  margin-top: 20px;
}
</style>