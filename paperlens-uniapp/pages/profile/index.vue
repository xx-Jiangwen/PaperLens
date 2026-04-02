<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header" :style="{ paddingTop: navBarTop + 'px' }">
			<view class="header-inner" :style="{ height: navBarHeight + 'px' }">
				<view class="header-left">
					<view class="icon-btn">
						<MdIcon name="menu" size="48" color="#3b82f6" />
					</view>
				</view>
				<text class="brand-title">PaperLens</text>
				<view class="header-right">
					<view class="icon-btn" @tap="goToSearch">
						<MdIcon name="search" size="48" color="#3b82f6" />
					</view>
				</view>
			</view>
		</view>

		<!-- 主内容区 -->
		<scroll-view class="main-content" :style="{ paddingTop: headerHeight + 'px' }" scroll-y="true">
			<!-- 头像区域 -->
			<view class="profile-section">
				<!-- 微信头像选择按钮 -->
				<button
					v-if="isLoggedIn"
					class="avatar-btn"
					open-type="chooseAvatar"
					@chooseavatar="onChooseAvatar"
				>
					<image
						v-if="userInfo.avatar"
						class="avatar"
						:src="userInfo.avatar"
						mode="aspectFill"
					/>
					<view v-else class="avatar-placeholder">
						<MdIcon name="person" size="64" color="#c1c6d5" filled />
					</view>
					<view class="avatar-edit-hint">
						<MdIcon name="edit" size="28" color="#ffffff" />
					</view>
				</button>
				<!-- 未登录时点击登录 -->
				<view v-else class="avatar-wrapper" @tap="handleLogin">
					<view class="avatar-placeholder">
						<MdIcon name="person" size="64" color="#c1c6d5" filled />
					</view>
				</view>
				<text class="username">{{ displayName }}</text>
			</view>

			<!-- 菜单卡片 -->
			<view class="menu-card">
				<view class="menu-item" @tap="goToBookmarks">
					<view class="menu-left">
						<MdIcon name="bookmark" size="48" color="#414753" />
						<text class="menu-label">我的收藏</text>
					</view>
					<MdIcon name="chevron-right" size="44" color="#c1c6d5" />
				</view>
				<view class="menu-divider"></view>
				<view class="menu-item" @tap="goToSettings">
					<view class="menu-left">
						<MdIcon name="settings" size="48" color="#414753" />
						<text class="menu-label">偏好设置</text>
					</view>
					<MdIcon name="chevron-right" size="44" color="#c1c6d5" />
				</view>
			</view>

			<!-- 退出登录 -->
			<view v-if="isLoggedIn" class="logout-section">
				<view class="logout-btn" @tap="logout">
					<text class="logout-text">退出登录</text>
				</view>
			</view>

			<!-- 未登录 -->
			<view v-else class="login-section">
				<view class="login-btn" @tap="handleLogin">
					<text class="login-text">登录 / 注册</text>
				</view>
			</view>
		</scroll-view>

		<!-- 底部导航 - 仅图标 -->
		<view class="bottom-nav">
			<view class="nav-item" @tap="switchTab('/pages/home/index')">
				<MdIcon name="home" size="52" color="#a1a1aa" />
			</view>
			<view class="nav-item active">
				<MdIcon name="person" size="52" color="#3b82f6" filled />
			</view>
		</view>
	</view>
</template>

<script>
import userStore from '@/stores/user.js'
import { getUserInfo, updateUserInfo } from '@/api/user.js'
import MdIcon from '@/components/MdIcon.vue'

export default {
	components: {
		MdIcon
	},

	data() {
		return {
			isLoggedIn: false,
			userInfo: {},
			statusBarHeight: 20,
				navBarTop: 20,
				navBarHeight: 56
		}
	},

	computed: {
		displayName() {
			if (!this.isLoggedIn) return '未登录'
			return this.userInfo.nickname || 'PaperLens Reader'
		},
		headerHeight() {
			return this.navBarTop + this.navBarHeight + 32
		}
	},

	onLoad() {
		// 获取状态栏高度
		const systemInfo = uni.getSystemInfoSync()
		this.statusBarHeight = systemInfo.statusBarHeight || 20

			// 获取微信胶囊按钮位置，确保导航栏不被遮挡
			try {
				const menuRect = uni.getMenuButtonBoundingClientRect()
				if (menuRect) {
					// 导航栏顶部位置 = 胶囊底部 + 间距
					this.navBarTop = menuRect.bottom + 8
					// 导航栏高度与胶囊对齐
					this.navBarHeight = menuRect.height
				}
			} catch (e) {
				// 非微信环境使用默认值
				this.navBarTop = this.statusBarHeight + 44
			}

		userStore.init()
		this.refreshState()
	},

	onShow() {
		this.refreshState()
	},

	methods: {
		refreshState() {
			this.isLoggedIn = userStore.isLoggedIn()
			if (this.isLoggedIn) {
				this.loadUserInfo()
			} else {
				this.userInfo = {}
			}
		},

		async loadUserInfo() {
			try {
				const res = await getUserInfo()
				if (res.code === 200 && res.data) {
					this.userInfo = res.data
				}
			} catch (e) {
				console.error('加载用户信息失败', e)
			}
		},

		// 微信头像选择回调
		async onChooseAvatar(e) {
			const tempAvatarPath = e.detail.avatarUrl
			if (!tempAvatarPath) return

			uni.showLoading({ title: '上传中...' })

			try {
				// 上传头像到服务器
				const uploadRes = await new Promise((resolve, reject) => {
					uni.uploadFile({
						url: this.$config.baseUrl + '/api/v1/users/avatar',
						filePath: tempAvatarPath,
						name: 'avatar',
						header: {
							'Authorization': 'Bearer ' + userStore.getToken()
						},
						success: (res) => {
							if (res.statusCode === 200) {
								resolve(JSON.parse(res.data))
							} else {
								reject(new Error('上传失败'))
							}
						},
						fail: reject
					})
				})

				if (uploadRes.code === 200) {
					this.userInfo.avatar = uploadRes.data.avatar
					uni.showToast({ title: '头像已更新', icon: 'success' })
				} else {
					throw new Error(uploadRes.msg || '上传失败')
				}
			} catch (e) {
				console.error('上传头像失败', e)
				uni.showToast({ title: '上传失败', icon: 'none' })
			} finally {
				uni.hideLoading()
			}
		},

		async handleLogin() {
			uni.showLoading({ title: '登录中...' })
			const success = await userStore.performWxLogin()
			uni.hideLoading()
			if (success) {
				const isNew = uni.getStorageSync('is_new_user')
				if (isNew) {
					uni.navigateTo({ url: '/pages/auth/onboarding' })
				} else {
					uni.showToast({ title: '登录成功', icon: 'success' })
					this.refreshState()
				}
			} else {
				uni.showToast({ title: '登录失败', icon: 'none' })
			}
		},

		goToSearch() {
			uni.navigateTo({ url: '/pages/home/search' })
		},

		goToBookmarks() {
			if (!this.isLoggedIn) {
				this.handleLogin()
				return
			}
			uni.navigateTo({ url: '/pages/profile/bookmarks' })
		},

		goToSettings() {
			uni.navigateTo({ url: '/pages/profile/settings' })
		},

		logout() {
			uni.showModal({
				title: '确认退出',
				content: '退出登录后需要重新登录才能使用完整功能',
				confirmText: '退出',
				confirmColor: '#ba1a1a',
				success: (res) => {
					if (res.confirm) {
						userStore.clear()
						this.isLoggedIn = false
						this.userInfo = {}
						uni.reLaunch({ url: '/pages/home/index' })
					}
				}
			})
		},

		switchTab(url) {
			uni.switchTab({ url })
		}
	}
}
</script>

<style lang="scss" scoped>
/* ========== 页面基础 ========== */

.page {
	min-height: 100vh;
	background-color: #F5F5F7;
	display: flex;
	flex-direction: column;
	overflow-x: hidden;
	width: 100%;
}

/* ========== 顶部导航栏 ========== */

.header {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	z-index: 100;
	background-color: rgba(255, 255, 255, 0.85);
	border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.header-inner {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	height: 56px;
	padding: 12px 16px 8px;
	max-width: 600px;
	margin: 0 auto;
	width: 100%;
	box-sizing: border-box;
}

.header-left,
.header-right {
	width: 48px;
	display: flex;
	align-items: center;
}

.icon-btn {
	padding: 8px;
}

.brand-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 20px;
	font-weight: 700;
	color: #18181b;
	letter-spacing: -0.02em;
	text-align: center;
	flex: 1;
}

/* ========== 主内容区 ========== */

.main-content {
	flex: 1;
	padding: 0 16px 100px;
	max-width: 600px;
	margin: 0 auto;
	width: 100%;
	box-sizing: border-box;
	overflow-x: hidden;
}

/* ========== 头像区域 ========== */

.profile-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-bottom: 40px;
		padding-top: 20px;
	width: 100%;
	box-sizing: border-box;
}

.avatar-btn {
	position: relative;
	width: 120px;
	height: 120px;
	padding: 0;
	margin: 0;
	background: transparent;
	border: none;
	border-radius: 50%;
	overflow: visible;
}

.avatar-btn::after {
	display: none;
}

.avatar-wrapper {
	width: 120px;
	height: 120px;
	border-radius: 50%;
	overflow: hidden;
	background-color: #e8e8ea;
	box-shadow: 0 0 0 8px #ffffff, 0 4px 16px rgba(0, 0, 0, 0.08);
	display: flex;
	align-items: center;
	justify-content: center;
}

.avatar {
	width: 120px;
	height: 120px;
	border-radius: 50%;
	box-shadow: 0 0 0 8px #ffffff, 0 4px 16px rgba(0, 0, 0, 0.08);
}

.avatar-placeholder {
	width: 120px;
	height: 120px;
	border-radius: 50%;
	background-color: #e8e8ea;
	display: flex;
	align-items: center;
	justify-content: center;
	box-shadow: 0 0 0 8px #ffffff, 0 4px 16px rgba(0, 0, 0, 0.08);
}

.avatar-edit-hint {
	position: absolute;
	right: 0;
	bottom: 0;
	width: 36px;
	height: 36px;
	background-color: #0066cc;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
}

.username {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 24px;
	font-weight: 700;
	color: #1a1c1d;
	letter-spacing: -0.02em;
	margin-top: 16px;
	word-break: break-word;
	overflow-wrap: break-word;
	text-align: center;
}

/* ========== 菜单卡片 ========== */

.menu-card {
	background-color: #ffffff;
	border-radius: 12px;
	overflow: hidden;
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
	width: 100%;
	box-sizing: border-box;
}

.menu-item {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding: 20px;
	width: 100%;
	box-sizing: border-box;
}

.menu-item:active {
	background-color: #f3f3f5;
	transform: scale(0.99);
}

.menu-left {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 16px;
	flex: 1;
	min-width: 0;
}

.menu-label {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	font-weight: 500;
	color: #1a1c1d;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.menu-divider {
	height: 1px;
	margin: 0 20px;
	background-color: #eeeef0;
}

/* ========== 退出登录 ========== */

.logout-section {
	margin-top: 24px;
	width: 100%;
	box-sizing: border-box;
}

.logout-btn {
	background-color: #ffffff;
	border-radius: 12px;
	padding: 20px;
	text-align: center;
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
	width: 100%;
	box-sizing: border-box;
}

.logout-btn:active {
	transform: scale(0.95);
	background-color: rgba(186, 26, 26, 0.05);
}

.logout-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	font-weight: 600;
	color: #ba1a1a;
}

/* ========== 登录按钮 ========== */

.login-section {
	margin-top: 24px;
	width: 100%;
	box-sizing: border-box;
}

.login-btn {
	background-color: #0066cc;
	border-radius: 12px;
	padding: 20px;
	text-align: center;
	box-shadow: 0 4px 24px rgba(0, 102, 204, 0.16);
	width: 100%;
	box-sizing: border-box;
}

.login-btn:active {
	transform: scale(0.95);
}

.login-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	font-weight: 600;
	color: #ffffff;
}

/* ========== 底部导航 - 仅图标 ========== */

.bottom-nav {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	gap: 64px;
	padding: 16px 16px 32px;
	background-color: rgba(255, 255, 255, 0.85);
	border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.nav-item {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 56px;
	height: 56px;
	border-radius: 50%;
	transition: all 0.2s ease;
}

.nav-item:active {
	transform: scale(0.9);
}

.nav-item.active {
	background-color: rgba(59, 130, 246, 0.1);
}
</style>