<template>
  <div class="paper-detail">
    <template v-if="paper">
      <h1>{{ paper.title }}</h1>
      <div class="authors">{{ paper.authors.join(', ') }}</div>
      <div class="categories">
        <span v-for="c in paper.categories" :key="c" class="tag">{{ c }}</span>
      </div>

      <div class="links">
        <a :href="paper.url" target="_blank">arXiv 页面</a>
        <a :href="paper.pdf_url" target="_blank">PDF</a>
      </div>

      <!-- AI 摘要 -->
      <div class="summary-section">
        <div class="summary-header">
          <h2>AI 摘要</h2>
          <button v-if="paper.summary_status !== 'done'" @click="generateSummary" :disabled="generating">
            {{ generating ? '生成中...' : '生成摘要' }}
          </button>
        </div>
        <SummaryPanel :summary="summary" :loading="generating" />
        <p class="disclaimer">内容由 AI 生成，请以原文为准</p>
      </div>

      <div class="abstract">
        <h3>原文摘要</h3>
        <p>{{ paper.abstract }}</p>
      </div>
    </template>
    <div v-else>加载中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import SummaryPanel from '../components/SummaryPanel.vue'
import { getPaper } from '../api/papers'
import { streamSummary } from '../api/ai'
import { useUserStore } from '../stores/user'
import type { Paper } from '../types/paper'

const route = useRoute()
const userStore = useUserStore()
const paper = ref<Paper | null>(null)
const generating = ref(false)
const summary = ref('')

onMounted(async () => {
  const { data } = await getPaper(route.params.id as string)
  paper.value = data.data
  if (paper.value?.summary_status === 'done') {
    summary.value = paper.value.summary_what || ''
  }
})

async function generateSummary() {
  if (!paper.value) return
  generating.value = true
  summary.value = ''
  await streamSummary(
    paper.value.id,
    userStore.token,
    (_section, delta) => { summary.value += delta },
    () => { generating.value = false },
    (err) => { console.error(err); generating.value = false },
  )
}
</script>
