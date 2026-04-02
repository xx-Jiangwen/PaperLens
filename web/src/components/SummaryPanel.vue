<template>
  <div class="summary-panel">
    <div v-if="loading" class="loading-indicator">AI 正在生成摘要...</div>
    <template v-else-if="summary">
      <p class="summary-content">{{ summary }}</p>
    </template>
    <div v-else class="empty">点击「生成摘要」按钮获取 AI 摘要</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  summary: string
  loading: boolean
}>()
</script>

<style scoped>
.summary-panel {
  background: #0d1117;
  border-radius: 8px;
  padding: 20px;
}
.summary-content {
  color: #c9d1d9;
  line-height: 1.7;
  font-size: 14px;
}
.empty, .loading-indicator {
  color: #8b949e;
  text-align: center;
  padding: 20px;
}
</style>