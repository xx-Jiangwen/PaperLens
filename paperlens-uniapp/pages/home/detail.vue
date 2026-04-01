<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header">
			<view class="header-inner">
				<view class="header-left">
					<view class="icon-btn" @tap="goBack">
						<MdIcon name="arrow-back" :size="44" color="#1a1c1d" />
					</view>
					<text class="brand-title">PaperLens</text>
				</view>
				<view class="header-right">
					<view class="icon-btn" @tap="onBookmark">
						<MdIcon
							name="bookmark"
							:size="44"
							:color="isBookmarked ? '#0066cc' : '#1a1c1d'"
							:filled="isBookmarked"
						/>
					</view>
					<view class="icon-btn" @tap="onShare">
						<MdIcon name="share" :size="44" color="#1a1c1d" />
					</view>
				</view>
			</view>
		</view>

		<!-- 加载状态 -->
		<view v-if="loading" class="loading-state">
			<text class="loading-text">加载中...</text>
		</view>

		<!-- 论文详情 -->
		<view v-else-if="paper" class="main-content">
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
					<MdIcon name="auto-awesome" :size="36" color="#0066cc" filled />
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
		</view>

		<!-- 底部导航 -->
		<view class="bottom-nav">
			<view class="nav-item active">
				<MdIcon name="home" :size="40" color="#3b82f6" filled />
				<text class="nav-label">首页</text>
			</view>
			<view class="nav-item" @tap="switchTab('/pages/profile/index')">
				<MdIcon name="person" :size="40" color="#71717a" />
				<text class="nav-label">个人</text>
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
@import '@/styles/variables.scss';

.page {
	min-height: 100vh;
	background-color: $color-bg;
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
	max-width: 1280rpx;
	margin: 0 auto;
}

.header-left,
.header-right {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 16rpx;
}

.icon-btn {
	padding: 16rpx;
}

.brand-title {
	font-family: 'Manrope', sans-serif;
	font-size: 40rpx;
	font-weight: 700;
	color: #18181b;
}

/* ========== 主内容区 ========== */

.main-content {
	padding: 192rpx 48rpx 200rpx;
	max-width: 1280rpx;
	margin: 0 auto;
}

.loading-state {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 80vh;
}

.loading-text {
	font-family: 'Inter', sans-serif;
	font-size: 34rpx;
	color: $color-on-surface-variant;
}

/* ========== 标题 - 4xl/5xl ========== */

.paper-title {
	font-family: 'Manrope', sans-serif;
	font-size: 80rpx;
	font-weight: 800;
	color: $color-on-surface;
	line-height: 1.1;
	letter-spacing: -0.02em;
	margin-bottom: 32rpx;
}

/* ========== 作者 + 年份 ========== */

.meta-row {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 24rpx;
	margin-bottom: 64rpx;
}

.authors-text {
	font-family: 'Inter', sans-serif;
	font-size: 36rpx;
	font-weight: 500;
	color: $color-on-surface-variant;
}

.dot-sep {
	width: 16rpx;
	height: 16rpx;
	border-radius: 50%;
	background-color: $color-surface-variant;
}

.year-badge {
	background-color: $color-surface-container-high;
	color: $color-on-surface-variant;
	font-family: 'Inter', sans-serif;
	font-size: 26rpx;
	font-weight: 600;
	letter-spacing: 0.05em;
	padding: 12rpx 24rpx;
	border-radius: 999rpx;
}

/* ========== 关键词 ========== */

.keywords-section {
	margin-bottom: 64rpx;
}

.section-label {
	font-family: 'Manrope', sans-serif;
	font-size: 26rpx;
	font-weight: 700;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: rgba($color-on-surface-variant, 0.7);
	margin-bottom: 24rpx;
	display: block;
}

.keywords-list {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	gap: 16rpx;
}

.keyword-tag {
	background-color: $color-surface-container-lowest;
	color: $color-on-surface;
	font-family: 'Inter', sans-serif;
	font-size: 28rpx;
	font-weight: 500;
	padding: 20rpx 32rpx;
	border-radius: 999rpx;
	box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}

/* ========== AI 摘要 ========== */

.ai-section {
	background-color: rgba($color-primary-container, 0.05);
	border: 2rpx solid rgba($color-primary-container, 0.1);
	border-radius: 48rpx;
	padding: 64rpx;
	margin-bottom: 64rpx;
}

.ai-header {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 16rpx;
	margin-bottom: 32rpx;
}

.ai-title {
	font-family: 'Manrope', sans-serif;
	font-size: 36rpx;
	font-weight: 700;
	color: $color-primary-container;
}

.ai-content {
	// 内容
}

.ai-paragraph {
	font-family: 'Inter', sans-serif;
	font-size: 36rpx;
	font-weight: 500;
	color: $color-on-surface;
	line-height: 1.6;
	margin-bottom: 32rpx;
}

.ai-list {
	display: flex;
	flex-direction: column;
	gap: 24rpx;
}

.ai-list-item {
	display: flex;
	flex-direction: row;
	gap: 24rpx;
}

.bullet {
	font-size: 32rpx;
	color: $color-primary-container;
}

.list-text {
	font-family: 'Inter', sans-serif;
	font-size: 36rpx;
	font-weight: 500;
	color: $color-on-surface;
	line-height: 1.6;
}

.ai-status {
	font-family: 'Inter', sans-serif;
	font-size: 34rpx;
	color: $color-on-surface-variant;
	text-align: center;
	padding: 32rpx;
}

/* ========== 原文摘要 ========== */

.abstract-section {
	margin-bottom: 64rpx;
}

.abstract-card {
	background-color: $color-surface-container-lowest;
	border-radius: 48rpx;
	padding: 64rpx;
}

.abstract-text {
	font-family: 'Inter', sans-serif;
	font-size: 36rpx;
	color: $color-on-surface;
	line-height: 1.6;
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
	padding: 24rpx 32rpx 64rpx;
	background-color: rgba(255, 255, 255, 0.7);
	backdrop-filter: blur(40px);
	-webkit-backdrop-filter: blur(40px);
	border-top-left-radius: 32rpx;
	border-top-right-radius: 32rpx;
	box-shadow: 0 -8rpx 80rpx rgba(26, 28, 29, 0.06);
}

.nav-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 12rpx 48rpx;
	border-radius: 24rpx;
	transition: all 0.2s ease;
}

.nav-item.active {
	background-color: rgba(59, 130, 246, 0.1);
}

.nav-label {
	font-family: 'Inter', sans-serif;
	font-size: 24rpx;
	font-weight: 500;
	color: #71717a;
	margin-top: 8rpx;
}

.nav-item.active .nav-label {
	color: #3b82f6;
}
</style>