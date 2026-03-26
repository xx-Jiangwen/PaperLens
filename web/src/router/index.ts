import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('../views/HomeView.vue') },
    { path: '/paper/:id', component: () => import('../views/PaperDetailView.vue') },
    { path: '/settings', component: () => import('../views/SettingsView.vue') },
    { path: '/bookmarks', component: () => import('../views/BookmarksView.vue') },
  ],
})

export default router
