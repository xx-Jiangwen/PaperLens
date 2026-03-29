<template>
	<view class="page">
		<!-- 用户信息 -->
		<view class="profile-header">
			<image class="avatar" :src="userInfo.avatar_url || defaultAvatar" mode="aspectFill" />
			<view class="user-info">
				<view class="nickname">{{ userInfo.nickname || '未登录' }}</view>
				<view class="hint" v-if="!isLoggedIn">点击登录，开启个性化推荐</view>
			</view>
		</view>

		<!-- 本周统计 -->
		<view class="section">
			<view class="section-title">本周阅读</view>
			<view class="stats-grid">
				<view class="stat-item">
					<view class="stat-value">{{ stats.weekRead || 0 }}</view>
					<view class="stat-label">阅读</view>
				</view>
				<view class="stat-item">
					<view class="stat-value">{{ stats.weekBookmarked || 0 }}</view>
					<view class="stat-label">收藏</view>
				</view>
				<view class="stat-item">
					<view class="stat-value">{{ stats.weekSkipped || 0 }}</view>
					<view class="stat-label">跳过</view>
				</view>
			</view>
		</view>

		<!-- 功能入口 -->
		<view class="menu-section">
			<view class="menu-item" @tap="goToBookmarks">
				<text class="menu-icon">📚</text>
				<text class="menu-label">我的收藏</text>
				<text class="menu-arrow">›</text>
			</view>
			<view class="menu-item" @tap="goToSettings">
				<text class="menu-icon">⚙️</text>
				<text class="menu-label">设置</text>
				<text class="menu-arrow">›</text>
			</view>
		</view>

		<!-- 关于 -->
		<view class="about-section">
			<view class="about-item">PaperLens v2.0</view>
			<view class="about-item">让论文阅读更高效</view>
		</view>
	</view>
</template>

<script>
import userStore from '@/stores/user.js'
import { getUserStats } from '@/api/user.js'

export default {
	data() {
		return {
			userInfo: {},
			stats: {},
			defaultAvatar: '/static/logo.png'
		}
	},

	computed: {
		isLoggedIn() {
			return userStore.isLoggedIn()
		}
	},

	onLoad() {
		userStore.init()
		this.loadUserInfo()
	},

	onShow() {
		if (this.isLoggedIn) {
			this.loadStats()
		}
	},

	methods: {
		async loadUserInfo() {
			if (this.isLoggedIn) {
				this.userInfo = {
					nickname: 'PaperLens 用户',
					avatar_url: ''
				}
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

		goToBookmarks() {
			if (!this.isLoggedIn) {
				this.promptLogin()
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
		},

		async promptLogin() {
			const success = await userStore.performWxLogin()
			if (success) {
				this.loadUserInfo()
				this.loadStats()
			} else {
				uni.showToast({ title: '登录失败', icon: 'none' })
			}
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.page {
	min-height: 100vh;
	background-color: $color-bg-grouped;
}

.profile-header {
	display: flex;
	flex-direction: row;
	align-items: center;
	padding: $spacing-6 $spacing-4;
	background-color: $color-bg;
}

.avatar {
	width: 128rpx;
	height: 128rpx;
	border-radius: 50%;
	background-color: $color-bg-grouped;
}

.user-info {
	margin-left: $spacing-4;
}

.nickname {
	font-size: $font-size-title2;
	font-weight: $font-weight-bold;
	color: $color-text-primary;
}

.hint {
	font-size: $font-size-subheadline;
	color: $color-text-secondary;
	margin-top: $spacing-1;
}

.section {
	background-color: $color-bg-card;
	margin: $spacing-4;
	border-radius: $radius-md;
	padding: $spacing-4;
}

.section-title {
	font-size: $font-size-headline;
	font-weight: $font-weight-semibold;
	color: $color-text-primary;
	margin-bottom: $spacing-4;
}

.stats-grid {
	display: flex;
	flex-direction: row;
}

.stat-item {
	flex: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.stat-value {
	font-size: $font-size-title1;
	font-weight: $font-weight-bold;
	color: $color-primary;
}

.stat-label {
	font-size: $font-size-footnote;
	color: $color-text-secondary;
	margin-top: $spacing-1;
}

.menu-section {
	background-color: $color-bg-card;
	margin: $spacing-4;
	border-radius: $radius-md;
	overflow: hidden;
}

.menu-item {
	display: flex;
	flex-direction: row;
	align-items: center;
	padding: $spacing-4;
	border-bottom: 1rpx solid $color-separator;
}

.menu-item:last-child {
	border-bottom: none;
}

.menu-icon {
	font-size: 40rpx;
	margin-right: $spacing-3;
}

.menu-label {
	flex: 1;
	font-size: $font-size-body;
	color: $color-text-primary;
}

.menu-arrow {
	font-size: $font-size-title2;
	color: $color-text-tertiary;
}

.about-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: $spacing-6;
}

.about-item {
	font-size: $font-size-caption;
	color: $color-text-tertiary;
	margin-bottom: $spacing-1;
}
</style>