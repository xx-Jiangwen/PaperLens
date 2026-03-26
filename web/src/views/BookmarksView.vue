<template>
  <div class="bookmarks">
    <h1>我的收藏</h1>
    <div class="papers-grid">
      <PaperCard v-for="item in bookmarks" :key="item.paper.id" :paper="item.paper"
                 @click="$router.push(`/paper/${item.paper.id}`)" />
    </div>
    <div v-if="bookmarks.length === 0">还没有收藏</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PaperCard from '../components/PaperCard.vue'
import client from '../api/client'

const bookmarks = ref<any[]>([])

onMounted(async () => {
  const { data } = await client.get('/bookmarks')
  bookmarks.value = data.data || []
})
</script>
