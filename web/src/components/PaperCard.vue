<template>
  <div class="paper-card">
    <div class="categories">
      <span v-for="c in paper.categories?.slice(0, 2)" :key="c" class="tag">{{ c }}</span>
    </div>
    <h3>{{ paper.title }}</h3>
    <div class="authors">{{ paper.authors?.slice(0, 3).join(', ') }}{{ (paper.authors?.length ?? 0) > 3 ? ' 等' : '' }}</div>
    <p class="abstract">{{ paper.abstract?.slice(0, 150) }}...</p>
    <div class="footer">
      <span class="date">{{ formatDate(paper.published_at) }}</span>
      <span class="summary-badge" :class="paper.summary_status">
        {{ statusText[paper.summary_status] }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Paper } from '../types/paper'

defineProps<{ paper: Paper }>()

const statusText: Record<string, string> = {
  pending: '待生成', processing: '生成中', done: 'AI摘要', failed: '生成失败',
}

function formatDate(d: string | null) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.paper-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.2s;
}
.paper-card:hover { border-color: #58a6ff; transform: translateY(-2px); }
h3 { color: #e6edf3; font-size: 1rem; margin: 8px 0; line-height: 1.5; }
.authors { color: #8b949e; font-size: 0.85rem; margin-bottom: 8px; }
.abstract { color: #8b949e; font-size: 0.85rem; line-height: 1.5; }
.tag { background: #1f4168; color: #58a6ff; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; margin-right: 4px; }
.footer { display: flex; justify-content: space-between; margin-top: 12px; }
.summary-badge.done { color: #3fb950; }
.summary-badge.pending { color: #8b949e; }
.summary-badge.processing { color: #d29922; }
</style>
