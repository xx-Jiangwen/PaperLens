<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'

onLaunch(() => {
  console.log('App Launch')
  // 初始化用户状态
  const userStore = useUserStore()
  console.log('User logged in:', userStore.isLoggedIn)
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style lang="scss">
/* 全局样式已在 uni.scss 中定义 */
</style>