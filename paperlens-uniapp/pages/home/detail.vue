<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header" :style="{ paddingTop: navBarTop + 'px' }">
			<view class="header-inner" :style="{ height: navBarHeight + 'px' }">
				<view class="header-left">
					<view class="icon-btn" @tap="goBack">
						<MdIcon name="arrow-back" size="48" color="#1a1c1d" />
					</view>
				</view>
				<text class="brand-title">PaperLens</text>
				<view class="header-right">
					<view class="icon-btn" @tap="onBookmark">
						<MdIcon
							name="bookmark"
							size="48"
							:color="isBookmarked ? '#0066cc' : '#1a1c1d'"
							:filled="isBookmarked"
						/>
					</view>
					<view class="icon-btn" @tap="onShare">
						<MdIcon name="share" size="48" color="#1a1c1d" />
					</view>
				</view>
			</view>
		</view>

		<!-- 加载状态 -->
		<view v-if="loading" class="loading-state">
			<text class="loading-text">加载中...</text>
		</view>

		<!-- 论文详情 -->
		<scroll-view v-else-if="paper" class="main-content" :style="{ paddingTop: contentTop + 'px' }" scroll-y="true">
			<!-- 标题 -->
			<view class="paper-title">{{ paper.title }}</view>

			<!-- 作者 + 年份 -->
			<view class="meta-row">
				<text class="authors-text">{{ authorText }}</text>
				<view class="dot-sep"></view>
				<view class="year-badge">{{ displayYear }}</view>
			</view>

			<!-- 关键词 -->
			<view class="keywords-section">
				<text class="section-label">关键词</text>
				<view class="keywords-list">
					<view
						v-for="(kw, index) in keywords"
						:key="index"
						class="keyword-tag"
					>{{ kw }}</view>
				</view>
			</view>

			<!-- AI 摘要 -->
			<view class="ai-section">
				<view class="ai-header">
					<MdIcon name="auto-awesome" size="36" color="#0066cc" filled />
					<text class="ai-title">AI 摘要</text>
				</view>
				<view v-if="paper.summary_status === 'done'" class="ai-content">
					<text class="ai-paragraph">{{ paper.summary_what }}</text>
					<view class="ai-list">
						<view class="ai-list-item">
							<text class="bullet">•</text>
							<text class="list-text">{{ paper.summary_how }}</text>
						</view>
						<view class="ai-list-item">
							<text class="bullet">•</text>
							<text class="list-text">{{ paper.summary_why }}</text>
						</view>
					</view>
				</view>
				<view v-else-if="paper.summary_status === 'processing'" class="ai-status">
					<text>AI 摘要生成中...</text>
				</view>
				<view v-else class="ai-status">
					<text>暂无 AI 摘要</text>
				</view>
			</view>

			<!-- 原文摘要 -->
			<view class="abstract-section">
				<text class="section-label">原文摘要</text>
				<view class="abstract-card">
					<text class="abstract-text">{{ paper.abstract }}</text>
				</view>
			</view>
		</scroll-view>

		<!-- 底部导航 - 仅图标 -->
		<view class="bottom-nav">
			<view class="nav-item active" @tap="switchTab('/pages/home/index')">
				<MdIcon name="home" size="52" color="#3b82f6" filled />
			</view>
			<view class="nav-item" @tap="switchTab('/pages/profile/index')">
				<MdIcon name="person" size="52" color="#a1a1aa" />
			</view>
		</view>
	</view>
</template>

<script>
import { usePapersStore } from '@/stores/papers.js'
import { useBookmarksStore } from '@/stores/bookmarks.js'
import MdIcon from '@/components/MdIcon.vue'

export default {
	components: {
		MdIcon
	},

	setup() {
		const papersStore = usePapersStore()
		const bookmarksStore = useBookmarksStore()
		return { papersStore, bookmarksStore }
	},

		data() {
			return {
				navBarTop: 20,
				navBarHeight: 56,
				contentTop: 120
			}
		},

	computed: {
		paper() {
			return this.papersStore.currentPaper
		},
		loading() {
			return this.papersStore.detailLoading
		},
		authorText() {
			if (!this.paper || !this.paper.authors) return ''
			return this.paper.authors.join(', ')
		},
		displayYear() {
			if (!this.paper || !this.paper.published_at) return ''
			return new Date(this.paper.published_at).getFullYear()
		},
		keywords() {
			if (!this.paper || !this.paper.categories) return []
			return this.paper.categories.slice(0, 5)
		},
		isBookmarked() {
			if (!this.paper) return false
			return this.bookmarksStore.isBookmarked(this.paper.id)
		}
	},

	onLoad(options) {
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

		const id = decodeURIComponent(options.id || '')
		if (id) {
			this.papersStore.fetchPaperDetail(id)
		}
	},

	onUnload() {
		this.papersStore.clearCurrentPaper()
	},

	methods: {
		goBack() {
			uni.navigateBack()
		},

		async onBookmark() {
			if (!this.paper) return
			await this.bookmarksStore.toggleBookmark(this.paper.id)
			uni.showToast({
				title: this.isBookmarked ? '已取消收藏' : '已收藏',
				icon: 'success'
			})
		},

		onShare() {
			if (!this.paper) return
			uni.setClipboardData({
				data: this.paper.url,
				success: () => {
					uni.showToast({ title: '链接已复制', icon: 'success' })
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
}

.header-left {
	width: 48px;
	display: flex;
	align-items: center;
}

.header-right {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 4px;
	width: 96px;
	justify-content: flex-end;
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
}

.loading-state {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 60vh;
}

.loading-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	color: #414753;
}

/* ========== 标题 ========== */

.paper-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 28px;
	font-weight: 800;
	color: #1a1c1d;
	line-height: 1.2;
	letter-spacing: -0.02em;
	margin-bottom: 16px;
}

/* ========== 作者 + 年份 ========== */

	.meta-row {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 8px;
		margin-bottom: 32px;
		flex-wrap: wrap;
	}
.authors-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 500;
	color: #414753;
}

.dot-sep {
	width: 6px;
	height: 6px;
	border-radius: 50%;
	background-color: #e2e2e4;
}

.year-badge {
	background-color: #e8e8ea;
	color: #414753;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 12px;
	font-weight: 600;
	letter-spacing: 0.05em;
	padding: 6px 12px;
	border-radius: 999px;
}

/* ========== 关键词 ========== */

.keywords-section {
	margin-bottom: 32px;
}

.section-label {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 12px;
	font-weight: 700;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: rgba(65, 71, 83, 0.7);
	margin-bottom: 12px;
	display: block;
}

.keywords-list {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	gap: 8px;
}

.keyword-tag {
	background-color: #ffffff;
	color: #1a1c1d;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 500;
	padding: 10px 16px;
	border-radius: 999px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* ========== AI 摘要 ========== */

.ai-section {
	background-color: rgba(0, 102, 204, 0.05);
	border: 1px solid rgba(0, 102, 204, 0.1);
	border-radius: 16px;
	padding: 24px;
	margin-bottom: 32px;
}

.ai-header {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 8px;
	margin-bottom: 16px;
}

.ai-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 18px;
	font-weight: 700;
	color: #0066cc;
}

.ai-paragraph {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 15px;
	font-weight: 500;
	color: #1a1c1d;
	line-height: 1.6;
	margin-bottom: 16px;
}

.ai-list {
	display: flex;
	flex-direction: column;
	gap: 12px;
}

.ai-list-item {
	display: flex;
	flex-direction: row;
	gap: 12px;
}

.bullet {
	font-size: 14px;
	color: #0066cc;
}

.list-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 15px;
	font-weight: 500;
	color: #1a1c1d;
	line-height: 1.6;
}

.ai-status {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	color: #414753;
	text-align: center;
	padding: 16px;
}

/* ========== 原文摘要 ========== */

.abstract-section {
	margin-bottom: 32px;
}

.abstract-card {
	background-color: #ffffff;
	border-radius: 16px;
	padding: 24px;
}

.abstract-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 15px;
	color: #1a1c1d;
	line-height: 1.6;
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