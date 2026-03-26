<template>
  <div class="home">
    <div class="filters">
      <CategoryFilter :categories="CATEGORIES" v-model="activeCategory" />
      <input v-model="searchQuery" placeholder="搜索论文..." @keyup.enter="fetchPapers" />
    </div>
    <div class="papers-grid">
      <PaperCard
        v-for="paper in papers"
        :key="paper.id"
        :paper="paper"
        @click="$router.push(`/paper/${paper.id}`)"
      />
    </div>
    <div v-if="loading" class="loading">加载中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PaperCard from '../components/PaperCard.vue'
import CategoryFilter from '../components/CategoryFilter.vue'
import { getTodayPapers, getPapers } from '../api/papers'
import type { Paper } from '../types/paper'

const CATEGORIES = ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML']
const papers = ref<Paper[]>([])
const loading = ref(false)
const activeCategory = ref('')
const searchQuery = ref('')

async function fetchPapers() {
  loading.value = true
  try {
    const { data } = await getPapers({ category: activeCategory.value || undefined, q: searchQuery.value || undefined })
    papers.value = data.data
  } finally {
    loading.value = false
  }
}

onMounted(fetchPapers)
</script>
