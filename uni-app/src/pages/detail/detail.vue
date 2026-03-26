<template>
  <view class="container" v-if="paper">
    <view class="title">{{ paper.title }}</view>
    <view class="authors">{{ paper.authors.join(', ') }}</view>

    <view class="tags">
      <text v-for="(c, idx) in paper.categories" :key="idx" class="tag">{{ c }}</text>
    </view>

    <view class="action-btns">
      <button class="btn-secondary" @click="openArxiv">复制链接</button>
      <button class="btn-primary" @click="openPdf">查看 PDF</button>
    </view>

    <!-- AI 三段式摘要 -->
    <view class="summary-section">
      <view class="section-header">
        <text class="section-title">AI 结构化摘要</text>
      </view>
      <view v-if="summary.what">
        <view class="summary-item">
          <view class="summary-label">问题与方案</view>
          <view class="summary-text">{{ summary.what }}</view>
        </view>
        <view class="summary-item">
          <view class="summary-label">技术路径</view>
          <view class="summary-text">{{ summary.how }}</view>
        </view>
        <view class="summary-item">
          <view class="summary-label">贡献与意义</view>
          <view class="summary-text">{{ summary.why }}</view>
        </view>
        <view class="disclaimer">内容由 AI 生成，请以原文为准</view>
        <button class="btn-ghost" @click="copySummary">复制摘要文本</button>
      </view>
      <view v-else class="empty">暂无 AI 摘要，将在后台自动生成</view>
    </view>

    <!-- 原文摘要 -->
    <view class="abstract-section">
      <view class="section-title">原文摘要</view>
      <view class="abstract-text">{{ paper.abstract }}</view>
    </view>
  </view>

  <view v-else class="loading-container">
    <text>加载中...</text>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getPaper } from '@/api/papers'
import type { Paper } from '@/types'

const paper = ref<Paper | null>(null)
const summary = ref({ what: '', how: '', why: '' })

function loadPaper(id: string) {
  getPaper(id).then((res) => {
    paper.value = res.data
    if (res.data?.summary_status === 'done') {
      summary.value = {
        what: res.data.summary_what || '',
        how: res.data.summary_how || '',
        why: res.data.summary_why || ''
      }
    }
  }).catch(() => {
    uni.showToast({ title: '加载失败', icon: 'error' })
  })
}

function openPdf() {
  if (paper.value?.pdf_url) {
    // #ifdef MP-WEIXIN
    uni.setClipboardData({
      data: paper.value.pdf_url,
      success: () => uni.showToast({ title: 'PDF链接已复制', icon: 'success' })
    })
    // #endif
    // #ifdef H5
    window.open(paper.value.pdf_url, '_blank')
    // #endif
  } else {
    uni.showToast({ title: '暂无PDF链接', icon: 'none' })
  }
}

function openArxiv() {
  if (paper.value?.url) {
    uni.setClipboardData({
      data: paper.value.url,
      success: () => uni.showToast({ title: '链接已复制', icon: 'success' })
    })
  }
}

function copySummary() {
  const text = `问题与方案：${summary.value.what}。技术路径：${summary.value.how}。贡献与意义：${summary.value.why}`
  uni.setClipboardData({
    data: text,
    success: () => uni.showToast({ title: '摘要已复制', icon: 'success' })
  })
}

onLoad((options) => {
  const id = decodeURIComponent(options?.id || '')
  if (id) loadPaper(id)
})
</script>

<style lang="scss" scoped>
.container {
  padding: 16px;
}

.title {
  color: #e6edf3;
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 12px;
}

.authors {
  color: #8b949e;
  font-size: 13px;
  margin-bottom: 12px;
}

.tags {
  margin-bottom: 16px;
}

.tag {
  display: inline-block;
  background: #1f4168;
  color: #58a6ff;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 6px;
  margin-bottom: 4px;
}

.action-btns {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.btn-secondary {
  flex: 1;
  background: #21262d;
  color: #c9d1d9;
  border: 1px solid #30363d;
  border-radius: 8px;
  font-size: 14px;

  &:active {
    background: #30363d;
  }
}

.btn-primary {
  flex: 1;
  background: #238636;
  color: #fff;
  border-radius: 8px;
  font-size: 14px;

  &:active {
    background: #2ea043;
  }
}

.btn-ghost {
  background: transparent;
  color: #58a6ff;
  border: 1px solid #30363d;
  border-radius: 8px;
  font-size: 14px;
  margin-top: 12px;
}

.summary-section {
  background: #161b22;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.section-title {
  color: #e6edf3;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.summary-item {
  margin-bottom: 16px;
}

.summary-label {
  color: #58a6ff;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 6px;
}

.summary-text {
  color: #c9d1d9;
  font-size: 14px;
  line-height: 1.6;
}

.disclaimer {
  color: #8b949e;
  font-size: 12px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #30363d;
}

.empty {
  color: #8b949e;
  font-size: 14px;
  text-align: center;
  padding: 20px;
}

.abstract-section {
  background: #161b22;
  border-radius: 12px;
  padding: 16px;
}

.abstract-text {
  color: #8b949e;
  font-size: 13px;
  line-height: 1.6;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: #8b949e;
}
</style>