<template>
	<view class="page">
		<!-- 自定义顶部导航栏 -->
		<view class="header">
			<view class="header-content">
				<view class="header-left">
					<text class="header-icon">📖</text>
					<text class="header-title">The Editorial Scholar</text>
				</view>
				<view class="header-right">
					<text class="brand-name">PaperLens</text>
				</view>
			</view>
			<view class="header-divider"></view>
		</view>

		<!-- Hero 区域 -->
		<view class="hero-section">
			<text class="hero-label">READER PROFILE</text>
			<view class="hero-title">
				<text class="hero-title-main" v-if="isLoggedIn">{{ userInfo.nickname || 'PaperLens Reader' }}</text>
				<text class="hero-title-main" v-else>Welcome</text>
			</view>
			<text class="hero-subtitle" v-if="isLoggedIn">探索学术前沿，发现精选论文</text>
			<text class="hero-subtitle" v-else @tap="handleLogin">点击登录，开启个性化推荐</text>
			<view class="hero-divider"></view>
		</view>

		<!-- 统计 Bento 卡片 -->
		<view class="stats-section" v-if="isLoggedIn">
			<view class="bento-card">
				<view class="bento-accent"></view>
				<view class="bento-header">
					<text class="bento-icon">◆</text>
					<text class="bento-label">WEEKLY STATS</text>
				</view>
				<view class="bento-list">
					<view class="bento-item">
						<text class="bento-num">01</text>
						<text class="bento-text">本周阅读</text>
						<text class="bento-value">{{ stats.weekRead || 0 }}</text>
					</view>
					<view class="bento-item">
						<text class="bento-num">02</text>
						<text class="bento-text">收藏</text>
						<text class="bento-value">{{ stats.weekBookmarked || 0 }}</text>
					</view>
					<view class="bento-item">
						<text class="bento-num">03</text>
						<text class="bento-text">跳过</text>
						<text class="bento-value">{{ stats.weekSkipped || 0 }}</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 菜单区域 -->
		<view class="menu-section">
			<view class="menu-card">
				<view class="menu-item" @tap="goToBookmarks">
					<text class="menu-label">我的收藏</text>
					<text class="menu-arrow">→</text>
				</view>
				<view class="menu-divider"></view>
				<view class="menu-item" @tap="goToSettings">
					<text class="menu-label">偏好设置</text>
					<text class="menu-arrow">→</text>
				</view>
			</view>
		</view>

		<!-- 底部信息 -->
		<view class="footer">
			<text class="footer-text">PaperLens v2.0</text>
			<text class="footer-sub">让论文阅读更高效</text>
		</view>

		<!-- 自定义底部导航 -->
		<TabBar current-path="/pages/profile/index" />
	</view>
</template>

<script>
import TabBar from '@/components/TabBar.vue'
import userStore from '@/stores/user.js'
import { getUserInfo, getUserStats } from '@/api/user.js'

export default {
	components: {
		TabBar
	},

	data() {
		return {
			isLoggedIn: false,
			userInfo: {},
			stats: {}
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
				this.loadStats()
			} else {
				this.userInfo = {}
				this.stats = {}
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

		async loadStats() {
			try {
				const res = await getUserStats()
				if (res.code === 200 && res.data) {
					this.stats = res.data
				}
			} catch (e) {
				console.error('加载统计失败', e)
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

		goToBookmarks() {
			if (!this.isLoggedIn) {
				this.handleLogin()
				return
			}
			uni.navigateTo({
				url: '/pages/profile/bookmarks'
			})
		},

		goToSettings() {
			uni.navigateTo({
				url: '/pages/profile/settings'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.page {
	min-height: 100vh;
	background-color: $color-bg;
	padding-bottom: 160rpx;
}

/* ========== 自定义顶部导航栏 ========== */

.header {
	position: sticky;
	top: 0;
	z-index: 100;
	background-color: $color-bg;
}

.header-content {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding: $spacing-4 $spacing-6;
}

.header-left {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: $spacing-2;
}

.header-icon {
	font-size: 40rpx;
	color: $color-primary;
}

.header-title {
	font-family: $font-family-headline;
	font-size: $font-size-headline-lg;
	font-weight: $font-weight-bold;
	color: $color-primary;
}

.header-right {
	display: flex;
	flex-direction: row;
	align-items: center;
}

.brand-name {
	font-family: $font-family-headline;
	font-size: $font-size-footnote;
	font-weight: $font-weight-bold;
	font-style: italic;
	color: $color-primary;
}

.header-divider {
	height: 1rpx;
	background-color: $color-surface-container-low;
}

/* ========== Hero 区域 ========== */

.hero-section {
	padding: $spacing-8 $spacing-6 $spacing-6;
}

.hero-label {
	font-family: $font-family-label;
	font-size: $font-size-label-xs;
	font-weight: $font-weight-extrabold;
	letter-spacing: $letter-spacing-widest;
	text-transform: uppercase;
	color: $color-text-secondary;
	margin-bottom: $spacing-4;
}

.hero-title {
	display: flex;
	flex-direction: column;
	margin-bottom: $spacing-2;
}

.hero-title-main {
	font-family: $font-family-headline;
	font-size: $font-size-headline-xl;
	font-weight: $font-weight-bold;
	color: $color-primary;
	line-height: $line-height-tight;
}

.hero-subtitle {
	font-family: $font-family-body;
	font-size: $font-size-subheadline;
	color: $color-text-secondary;
}

.hero-divider {
	width: 96rpx;
	height: 4rpx;
	background-color: $color-primary-container;
	border-radius: $radius-full;
	margin-top: $spacing-6;
}

/* ========== 统计 Bento 卡片 ========== */

.stats-section {
	padding: $spacing-6;
}

.bento-card {
	background-color: $color-primary-container;
	border-radius: $radius-xl;
	padding: $spacing-6;
	position: relative;
	overflow: hidden;
}

.bento-accent {
	position: absolute;
	top: 0;
	right: 0;
	width: 128rpx;
	height: 128rpx;
	background-color: rgba(255, 255, 255, 0.05);
	border-radius: 50%;
	transform: translate(64rpx, -64rpx);
}

.bento-header {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: $spacing-2;
	margin-bottom: $spacing-4;
}

.bento-icon {
	color: $color-tertiary-fixed;
	font-size: 28rpx;
}

.bento-label {
	font-family: $font-family-label;
	font-size: $font-size-label-xs;
	font-weight: $font-weight-extrabold;
	letter-spacing: $letter-spacing-widest;
	text-transform: uppercase;
	color: $color-on-primary;
}

.bento-list {
	display: flex;
	flex-direction: column;
	gap: $spacing-3;
}

.bento-item {
	display: flex;
	flex-direction: row;
	align-items: center;
}

.bento-num {
	font-family: $font-family-body;
	font-size: $font-size-footnote;
	font-weight: $font-weight-bold;
	color: $color-tertiary-fixed;
	margin-right: $spacing-3;
}

.bento-text {
	font-family: $font-family-body;
	font-size: $font-size-subheadline;
	color: $color-on-primary;
	opacity: 0.9;
}

.bento-value {
	font-family: $font-family-body;
	font-size: $font-size-headline-lg;
	font-weight: $font-weight-bold;
	color: $color-on-primary;
	margin-left: auto;
}

/* ========== 菜单区域 ========== */

.menu-section {
	padding: $spacing-6;
}

.menu-card {
	background-color: $color-surface-container-low;
	border-radius: $radius-md;
}

.menu-item {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding: $spacing-4 $spacing-4;
}

.menu-label {
	font-family: $font-family-body;
	font-size: $font-size-body;
	font-weight: $font-weight-medium;
	color: $color-text-primary;
}

.menu-arrow {
	font-size: 32rpx;
	color: $color-text-tertiary;
}

.menu-divider {
	height: 1rpx;
	background-color: $color-separator;
	opacity: 0.2;
	margin: 0 $spacing-4;
}

/* ========== 底部信息 ========== */

.footer {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: $spacing-8;
}

.footer-text {
	font-family: $font-family-headline;
	font-size: $font-size-footnote;
	font-weight: $font-weight-bold;
	font-style: italic;
	color: $color-primary;
}

.footer-sub {
	font-family: $font-family-body;
	font-size: $font-size-caption;
	color: $color-text-tertiary;
	margin-top: $spacing-1;
}
</style>