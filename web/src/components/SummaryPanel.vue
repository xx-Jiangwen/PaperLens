<template>
  <div class="summary-panel">
    <div v-if="loading" class="loading-indicator">AI 正在生成摘要...</div>
    <template v-else-if="summary.what || summary.how || summary.why">
      <div class="section">
        <h4>问题与方案</h4>
        <p>{{ summary.what }}</p>
      </div>
      <div class="section">
        <h4>技术路径</h4>
        <p>{{ summary.how }}</p>
      </div>
      <div class="section">
        <h4>贡献与意义</h4>
        <p>{{ summary.why }}</p>
      </div>
    </template>
    <div v-else class="empty">点击「生成摘要」按钮获取 AI 三段式摘要</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  summary: { what: string; how: string; why: string }
  loading: boolean
}>()
</script>

<style scoped>
.summary-panel { background: #0d1117; border-radius: 8px; padding: 20px; }
.section { margin-bottom: 16px; }
h4 { color: #58a6ff; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
p { color: #c9d1d9; line-height: 1.7; }
.empty, .loading-indicator { color: #8b949e; text-align: center; padding: 20px; }
</style>
