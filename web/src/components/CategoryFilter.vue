<template>
  <div class="category-filter">
    <button
      :class="['tag', modelValue === '' && 'active']"
      @click="$emit('update:modelValue', '')"
    >全部</button>
    <button
      v-for="cat in categories"
      :key="cat"
      :class="['tag', modelValue === cat && 'active']"
      @click="$emit('update:modelValue', cat)"
    >{{ cat }}</button>
  </div>
</template>

<script setup lang="ts">
defineProps<{ categories: string[]; modelValue: string }>()
defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<style scoped>
.category-filter { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.tag { background: #161b22; color: #8b949e; border: 1px solid #30363d; padding: 6px 14px; border-radius: 20px; cursor: pointer; transition: all 0.2s; }
.tag.active, .tag:hover { background: #1f4168; color: #58a6ff; border-color: #58a6ff; }
</style>
