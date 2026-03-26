import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { wxLogin as wxLoginApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(uni.getStorageSync('token') || null)
  const userId = ref<number | null>(null)

  const isLoggedIn = computed(() => !!token.value)

  function setToken(t: string) {
    token.value = t
    uni.setStorageSync('token', t)
  }

  function logout() {
    token.value = null
    userId.value = null
    uni.removeStorageSync('token')
  }

  // 微信登录 - 条件编译处理
  async function wxLogin(): Promise<string> {
    if (token.value) return token.value

    // #ifdef MP-WEIXIN
    const loginRes = await new Promise<UniApp.LoginRes>((resolve, reject) => {
      uni.login({
        success: resolve,
        fail: reject
      })
    })

    const res = await wxLoginApi(loginRes.code)
    if (res.code === 200 && res.data) {
      setToken(res.data.token)
      userId.value = res.data.user_id
      return res.data.token
    }
    throw new Error(res.msg || '登录失败')
    // #endif

    // #ifdef H5
    throw new Error('H5 环境请使用其他登录方式')
    // #endif
  }

  return { token, userId, isLoggedIn, setToken, logout, wxLogin }
})