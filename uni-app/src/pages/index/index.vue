<template>
  <view class="container">
    <!-- 分类筛选 -->
    <scroll-view class="categories" scroll-x>
      <view
        v-for="cat in categories"
        :key="cat"
        :class="['cat-tag', { active: activeCategory === cat }]"
        @click="onCategoryTap(cat)"
      >{{ cat }}</view>
    </scroll-view>

    <!-- 论文列表 -->
    <view class="papers">
      <view
        v-for="paper in papers"
        :key="paper.id"
        class="paper-card"
        @click="onPaperTap(paper.id)"
      >
        <view class="tags">
          <text
            v-for="(c, idx) in paper.categories?.slice(0, 2)"
            :key="idx"
            class="tag"
          >{{ c }}</text>
        </view>
        <view class="title">{{ paper.title }}</view>
        <view class="authors">{{ paper.authors[0] }}{{ paper.authors.length > 1 ? ' 等' : '' }}</view>
        <view :class="['summary-status', paper.summary_status]">
          {{ statusText[paper.summary_status] }}
        </view>
      </view>
    </view>

    <view v-if="loading" class="loading">加载中...</view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onPullDownRefresh } from '@dcloudio/uni-app'
import { getTodayPapers, getPapers } from '@/api/papers'
import type { Paper } from '@/types'

const CATEGORIES = ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML']
const statusText: Record<string, string> = {
  pending: '待生成',
  processing: '生成中',
  done: 'AI摘要',
  failed: '生成失败'
}

const papers = ref<Paper[]>([])
const loading = ref(false)
const activeCategory = ref('')
const categories = ref(CATEGORIES)

async function fetchPapers() {
  loading.value = true
  try {
    const res = activeCategory.value
      ? await getPapers({ category: activeCategory.value })
      : await getTodayPapers()
    papers.value = res.data || []
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'error' })
  } finally {
    loading.value = false
  }
}

function onCategoryTap(cat: string) {
  activeCategory.value = activeCategory.value === cat ? '' : cat
  fetchPapers()
}

function onPaperTap(id: string) {
  uni.navigateTo({ url: `/pages/detail/detail?id=${encodeURIComponent(id)}` })
}

// 初始化加载
fetchPapers()

// 下拉刷新
onPullDownRefresh(() => {
  fetchPapers().finally(() => uni.stopPullDownRefresh())
})
</script>

<style lang="scss" scoped>
.container {
  padding: 12px;
}

.categories {
  white-space: nowrap;
  margin-bottom: 16px;
}

.cat-tag {
  display: inline-block;
  padding: 6px 14px;
  background: #161b22;
  color: #8b949e;
  border-radius: 20px;
  margin-right: 8px;
  font-size: 12px;

  &.active {
    background: #1f4168;
    color: #58a6ff;
  }
}

.paper-card {
  background: #161b22;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}

.title {
  color: #e6edf3;
  font-size: 14px;
  line-height: 1.5;
  margin: 8px 0;
}

.authors {
  color: #8b949e;
  font-size: 12px;
  margin-bottom: 8px;
}

.tag {
  background: #1f4168;
  color: #58a6ff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  margin-right: 4px;
}

.summary-status {
  font-size: 11px;
  color: #8b949e;

  &.done {
    color: #3fb950;
  }

  &.processing {
    color: #58a6ff;
  }

  &.failed {
    color: #f85149;
  }
}

.loading {
  text-align: center;
  color: #8b949e;
  padding: 20px;
}
</style>