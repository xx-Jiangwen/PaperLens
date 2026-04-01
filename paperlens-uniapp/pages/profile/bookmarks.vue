<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header" :style="{ paddingTop: navBarTop + 'px' }">
			<view class="header-inner" :style="{ height: navBarHeight + 'px' }">
				<view class="header-left">
					<view class="icon-btn" @tap="goBack">
						<MdIcon name="arrow-back" size="48" color="#71717a" />
					</view>
				</view>
				<text class="brand-title">PaperLens</text>
				<view class="header-right">
					<view class="icon-btn">
						<MdIcon name="search" size="48" color="#71717a" />
					</view>
				</view>
			</view>
		</view>

		<!-- 主内容区 -->
		<scroll-view class="main-content" :style="{ paddingTop: contentTop + 'px' }" scroll-y="true">
			<!-- 标题区域 -->
			<view class="title-section">
				<text class="page-title">我的收藏</text>
				<view class="title-meta">
					<view class="count-badge">{{ bookmarks.length }} 篇文献</view>
					<text class="update-text">最后更新: {{ lastUpdateText }}</text>
				</view>
			</view>

			<!-- 加载状态 -->
			<view v-if="loading && bookmarks.length === 0" class="loading-state">
				<text class="loading-text">加载中...</text>
			</view>

			<!-- 收藏列表 -->
			<view v-else-if="bookmarks.length > 0" class="paper-list">
				<view
					v-for="bookmark in bookmarks"
					:key="bookmark.id"
					class="paper-card"
					@tap="goToDetail(bookmark.paper || bookmark)"
				>
					<view class="card-top">
						<text class="card-title">{{ (bookmark.paper || bookmark).title }}</text>
						<view class="bookmark-icon">
							<MdIcon name="bookmark" size="44" color="#0066cc" filled />
						</view>
					</view>
					<view class="card-meta">
						<view class="meta-source">
							<MdIcon name="description" size="28" color="#414753" />
							<text class="meta-text">{{ displaySource(bookmark.paper || bookmark) }}</text>
						</view>
						<view class="meta-dot"></view>
						<text class="meta-date">{{ formatDate(bookmark.created_at) }} 加入</text>
					</view>
				</view>

				<!-- 查看更多 -->
				<view v-if="hasMore" class="load-more" @tap="loadMore">
					<text class="load-more-text">查看更多收藏</text>
					<MdIcon name="keyboard-arrow-down" size="32" color="#0066cc" />
				</view>
			</view>

			<!-- 空状态 -->
			<view v-else class="empty-state">
				<MdIcon name="bookmark" size="128" color="#c1c6d5" />
				<text class="empty-title">暂无收藏</text>
				<text class="empty-hint">去首页发现感兴趣的论文吧</text>
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
import { useBookmarksStore } from '@/stores/bookmarks.js'
import MdIcon from '@/components/MdIcon.vue'

export default {
	components: {
		MdIcon
	},

	setup() {
		const bookmarksStore = useBookmarksStore()
		return { bookmarksStore }
	},

		data() {
			return {
				navBarTop: 20,
				navBarHeight: 56,
				contentTop: 120
			}
		},

	computed: {
		bookmarks() {
			return this.bookmarksStore.bookmarks
		},
		loading() {
			return this.bookmarksStore.loading
		},
		hasMore() {
			return this.bookmarksStore.hasMore
		},
		lastUpdateText() {
			if (this.bookmarks.length === 0) return '-'
			return this.formatDate(this.bookmarks[0].created_at)
		}
	},

	onLoad() {
		// 获取胶囊按钮位置
		try {
			const menuRect = uni.getMenuButtonBoundingClientRect()
			if (menuRect) {
				this.navBarTop = menuRect.bottom + 8
				this.navBarHeight = menuRect.height
				this.contentTop = menuRect.bottom + 8 + this.navBarHeight + 16
			}
		} catch (e) {
			const systemInfo = uni.getSystemInfoSync()
			this.navBarTop = (systemInfo.statusBarHeight || 20) + 44
			this.contentTop = this.navBarTop + 56 + 16
		}

		this.bookmarksStore.fetchBookmarks(true)
	},

	onPullDownRefresh() {
		this.bookmarksStore.fetchBookmarks(true).finally(() => {
			uni.stopPullDownRefresh()
		})
	},

	onReachBottom() {
		if (this.hasMore && !this.loading) {
			this.loadMore()
		}
	},

	methods: {
		displaySource(paper) {
			if (paper.categories && paper.categories.length > 0) {
				return paper.categories[0]
			}
			return 'ArXiv'
		},

		formatDate(dateStr) {
			if (!dateStr) return '-'
			const date = new Date(dateStr)
			const year = date.getFullYear()
			const month = String(date.getMonth() + 1).padStart(2, '0')
			const day = String(date.getDate()).padStart(2, '0')
			return `${year}-${month}-${day}`
		},

		goBack() {
			uni.navigateBack()
		},

		goToDetail(paper) {
			const paperId = paper.id || paper.paper_id
			uni.navigateTo({
				url: `/pages/home/detail?id=${encodeURIComponent(paperId)}`
			})
		},

		switchTab(url) {
			uni.switchTab({ url })
		},

		loadMore() {
			if (!this.loading && this.hasMore) {
				this.bookmarksStore.fetchBookmarks()
			}
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
	/* 安全区域适配 */
	padding-top: constant(safe-area-inset-top);
	padding-top: env(safe-area-inset-top);
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
	text-align: center;
	flex: 1;
}

/* ========== 主内容区 ========== */

.main-content {
	flex: 1;
	padding: 120px 16px 100px;
	max-width: 600px;
	margin: 0 auto;
	width: 100%;
	box-sizing: border-box;
	overflow-x: hidden;
}

/* ========== 标题区域 ========== */

.title-section {
	margin-bottom: 32px;
}

.page-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 30px;
	font-weight: 800;
	color: #1a1c1d;
	letter-spacing: -0.02em;
	margin-bottom: 8px;
}

.title-meta {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 8px;
}

.count-badge {
	background-color: #e2e2e4;
	color: #414753;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 12px;
	font-weight: 500;
	padding: 4px 12px;
	border-radius: 999px;
	flex-shrink: 0;
}

.update-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 12px;
	color: #414753;
}

/* ========== 加载状态 ========== */

.loading-state {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 60px;
}

.loading-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	color: #414753;
}

/* ========== 论文卡片 ========== */

.paper-list {
	display: flex;
	flex-direction: column;
	gap: 16px;
	width: 100%;
	box-sizing: border-box;
	overflow-x: hidden;
}

.paper-card {
	background-color: #ffffff;
	border-radius: 12px;
	padding: 16px;
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
	transition: all 0.3s ease;
	width: 100%;
	box-sizing: border-box;
	overflow: hidden;
}

.paper-card:active {
	background-color: #f3f3f5;
	transform: scale(0.98);
}

.card-top {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: flex-start;
	gap: 12px;
	margin-bottom: 12px;
	width: 100%;
}

.card-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 18px;
	font-weight: 700;
	color: #1a1c1d;
	line-height: 1.3;
	flex: 1;
	word-break: break-word;
	overflow-wrap: break-word;
}

.paper-card:active .card-title {
	color: #0066cc;
}

.bookmark-icon {
	padding: 4px;
	flex-shrink: 0;
}

.card-meta {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 8px;
}

.meta-source {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 4px;
}

.meta-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 13px;
	color: #414753;
}

.meta-dot {
	width: 6px;
	height: 6px;
	border-radius: 50%;
	background-color: #c1c6d5;
	flex-shrink: 0;
}

.meta-date {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 13px;
	color: #414753;
}

/* ========== 查看更多 ========== */

.load-more {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
	gap: 8px;
	padding: 32px 0;
}

.load-more-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	font-weight: 600;
	color: #0066cc;
}

/* ========== 空状态 ========== */

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px;
}

.empty-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 20px;
	font-weight: 600;
	color: #1a1c1d;
	margin: 16px 0 8px;
}

.empty-hint {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	color: #414753;
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
	padding-bottom: calc(16px + constant(safe-area-inset-bottom));
	padding-bottom: calc(16px + env(safe-area-inset-bottom));
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