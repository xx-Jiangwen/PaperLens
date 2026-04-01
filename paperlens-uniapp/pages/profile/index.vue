<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header">
			<view class="header-inner">
				<view class="icon-btn">
					<text class="material-icon menu-icon">menu</text>
				</view>
				<text class="brand-title">PaperLens</text>
				<view class="icon-btn" @tap="goToSearch">
					<text class="material-icon search-icon">search</text>
				</view>
			</view>
		</view>

		<!-- 主内容区 -->
		<view class="main-content">
			<!-- 头像区域 -->
			<view class="profile-section">
				<view class="avatar-wrapper">
					<image
						v-if="isLoggedIn && userInfo.avatar"
						class="avatar"
						:src="userInfo.avatar"
						mode="aspectFill"
					/>
					<view v-else class="avatar-placeholder">
						<text class="avatar-icon">person</text>
					</view>
				</view>
				<text class="username">{{ displayName }}</text>
			</view>

			<!-- 菜单卡片 -->
			<view class="menu-card">
				<view class="menu-item" @tap="goToBookmarks">
					<view class="menu-left">
						<text class="menu-icon">bookmark</text>
						<text class="menu-label">我的收藏</text>
					</view>
					<text class="menu-arrow">chevron_right</text>
				</view>
				<view class="menu-divider"></view>
				<view class="menu-item" @tap="goToSettings">
					<view class="menu-left">
						<text class="menu-icon">settings</text>
						<text class="menu-label">偏好设置</text>
					</view>
					<text class="menu-arrow">chevron_right</text>
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
		</view>

		<!-- 底部导航 -->
		<view class="bottom-nav">
			<view class="nav-item" @tap="switchTab('/pages/home/index')">
				<text class="nav-icon">home</text>
				<text class="nav-label">首页</text>
			</view>
			<view class="nav-item active">
				<text class="nav-icon filled">person</text>
				<text class="nav-label">个人</text>
			</view>
		</view>
	</view>
</template>

<script>
import userStore from '@/stores/user.js'
import { getUserInfo } from '@/api/user.js'

export default {
	data() {
		return {
			isLoggedIn: false,
			userInfo: {}
		}
	},

	computed: {
		displayName() {
			if (!this.isLoggedIn) return '未登录'
			return this.userInfo.nickname || 'PaperLens Reader'
		}
	},

	onLoad() {
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
@import '@/styles/variables.scss';

.page {
	min-height: 100vh;
	background-color: $color-bg;
	padding-bottom: 140rpx;
}

/* ========== 顶部导航栏 ========== */

.header {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	z-index: 100;
	background-color: rgba(255, 255, 255, 0.7);
	backdrop-filter: blur(40px);
	-webkit-backdrop-filter: blur(40px);
}

.header-inner {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	height: 128rpx;
	padding: 0 48rpx;
	max-width: 768rpx;
	margin: 0 auto;
}

.icon-btn {
	padding: 16rpx;
}

.material-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 44rpx;
}

.menu-icon,
.search-icon {
	color: #3b82f6;
}

.brand-title {
	font-family: 'Manrope', sans-serif;
	font-size: 40rpx;
	font-weight: 700;
	color: #18181b;
}

/* ========== 主内容区 ========== */

.main-content {
	padding: 192rpx 48rpx 0;
	max-width: 768rpx;
	margin: 0 auto;
}

/* ========== 头像区域 ========== */

.profile-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-bottom: 96rpx;
}

.avatar-wrapper {
	width: 256rpx;
	height: 256rpx;
	border-radius: 50%;
	overflow: hidden;
	margin-bottom: 48rpx;
	background-color: $color-surface-container-high;
	box-shadow: 0 0 0 32rpx $color-surface-container-lowest,
	            0 8rpx 32rpx rgba(0, 0, 0, 0.08);
}

.avatar {
	width: 100%;
	height: 100%;
}

.avatar-placeholder {
	width: 100%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	background-color: $color-surface-container-high;
}

.avatar-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 128rpx;
	color: $color-outline-variant;
}

.username {
	font-family: 'Manrope', sans-serif;
	font-size: 48rpx;
	font-weight: 700;
	color: $color-on-surface;
	letter-spacing: -0.02em;
}

/* ========== 菜单卡片 ========== */

.menu-card {
	background-color: $color-surface-container-lowest;
	border-radius: 24rpx;
	overflow: hidden;
}

.menu-item {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding: 40rpx 48rpx;
}

.menu-item:active {
	background-color: $color-surface-container-low;
	transform: scale(0.99);
}

.menu-left {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 32rpx;
}

.menu-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 44rpx;
	color: $color-on-surface-variant;
}

.menu-label {
	font-family: 'Inter', sans-serif;
	font-size: 34rpx;
	font-weight: 500;
	color: $color-on-surface;
}

.menu-arrow {
	font-family: 'Material Symbols Outlined';
	font-size: 40rpx;
	color: $color-outline-variant;
}

.menu-divider {
	height: 2rpx;
	margin: 0 48rpx;
	background-color: $color-surface-container;
}

/* ========== 退出登录 ========== */

.logout-section {
	margin-top: 64rpx;
}

.logout-btn {
	background-color: $color-surface-container-lowest;
	border-radius: 24rpx;
	padding: 32rpx;
	text-align: center;
}

.logout-btn:active {
	transform: scale(0.95);
	background-color: rgba($color-error, 0.05);
}

.logout-text {
	font-family: 'Inter', sans-serif;
	font-size: 34rpx;
	font-weight: 600;
	color: $color-error;
}

/* ========== 登录按钮 ========== */

.login-section {
	margin-top: 64rpx;
}

.login-btn {
	background-color: $color-primary-container;
	border-radius: 24rpx;
	padding: 32rpx;
	text-align: center;
}

.login-btn:active {
	transform: scale(0.95);
}

.login-text {
	font-family: 'Inter', sans-serif;
	font-size: 34rpx;
	font-weight: 600;
	color: $color-on-primary;
}

/* ========== 底部导航 ========== */

.bottom-nav {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	gap: 32rpx;
	padding: 32rpx 64rpx 64rpx;
	background-color: rgba(255, 255, 255, 0.7);
	backdrop-filter: blur(40px);
	-webkit-backdrop-filter: blur(40px);
	border-top-left-radius: 48rpx;
	border-top-right-radius: 48rpx;
	box-shadow: 0 -8rpx 80rpx rgba(26, 28, 29, 0.04);
}

.nav-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 12rpx 48rpx;
	border-radius: 32rpx;
}

.nav-item:active {
	transform: scale(0.9);
}

.nav-item.active {
	background-color: rgba(59, 130, 246, 0.1);
}

.nav-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 40rpx;
	color: #71717a;
}

.nav-icon.filled {
	font-variation-settings: 'FILL' 1;
}

.nav-item.active .nav-icon {
	color: #3b82f6;
}

.nav-label {
	font-family: 'Inter', sans-serif;
	font-size: 22rpx;
	font-weight: 500;
	color: #71717a;
	margin-top: 8rpx;
}

.nav-item.active .nav-label {
	color: #3b82f6;
}
</style>