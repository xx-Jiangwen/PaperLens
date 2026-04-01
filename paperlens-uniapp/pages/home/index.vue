<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header">
			<view class="header-inner">
				<view class="header-left">
					<view class="icon-btn">
						<MdIcon name="menu" :size="44" color="#71717a" />
					</view>
					<text class="brand-title">PaperLens</text>
				</view>
				<view class="icon-btn" @tap="goToSearch">
					<MdIcon name="search" :size="44" color="#71717a" />
				</view>
			</view>
		</view>

		<!-- 主内容区 -->
		<view class="main-content">
			<!-- 标题 -->
			<view class="page-title">学术动态</view>

			<!-- 论文列表 -->
			<view class="paper-list">
				<!-- 加载状态 -->
				<view v-if="loading && papers.length === 0" class="loading-state">
					<text class="loading-text">加载中...</text>
				</view>

				<!-- 论文卡片 -->
				<view
					v-for="paper in papers"
					:key="paper.id"
					class="paper-card"
					@tap="goToDetail(paper)"
				>
					<view class="card-top">
						<view class="source-badge">{{ formatSource(paper) }}</view>
						<view class="bookmark-btn" @tap.stop="onBookmark(paper)">
							<MdIcon
								name="bookmark"
								:size="48"
								:color="isBookmarked(paper.id) ? '#0066cc' : '#0066cc'"
								:filled="isBookmarked(paper.id)"
								:class="{ 'icon-dim': !isBookmarked(paper.id) }"
							/>
						</view>
					</view>
					<view class="card-title">{{ paper.title }}</view>
					<view class="card-authors">{{ formatAuthors(paper.authors) }}</view>
					<view class="card-abstract">{{ paper.abstract }}</view>
				</view>

				<!-- 空状态 -->
				<view v-if="!loading && papers.length === 0" class="empty-state">
					<MdIcon name="description" :size="128" color="#c1c6d5" />
					<text class="empty-text">暂无论文</text>
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
		papers() {
			return this.papersStore.featuredPapers
		},
		loading() {
			return this.papersStore.featuredLoading
		}
	},

	onLoad() {
		this.papersStore.fetchFeaturedPapers()
	},

	onPullDownRefresh() {
		this.papersStore.fetchFeaturedPapers().finally(() => {
			uni.stopPullDownRefresh()
		})
	},

	methods: {
		formatSource(paper) {
			if (paper.arxiv_id) return `ARXIV:${paper.arxiv_id}`
			if (paper.categories && paper.categories.length > 0) {
				return paper.categories[0].toUpperCase()
			}
			return 'PAPER'
		},

		formatAuthors(authors) {
			if (!authors || authors.length === 0) return ''
			const first = authors[0]
			const more = authors.length > 1 ? ' 等' : ''
			return `${first}${more}`
		},

		isBookmarked(paperId) {
			return this.bookmarksStore.isBookmarked(paperId)
		},

		goToSearch() {
			uni.navigateTo({ url: '/pages/home/search' })
		},

		goToDetail(paper) {
			uni.navigateTo({
				url: `/pages/home/detail?id=${encodeURIComponent(paper.id)}`
			})
		},

		async onBookmark(paper) {
			await this.bookmarksStore.toggleBookmark(paper.id)
			uni.showToast({
				title: this.isBookmarked(paper.id) ? '已取消收藏' : '已收藏',
				icon: 'success'
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
	max-width: 1120rpx;
	margin: 0 auto;
}

.header-left {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 32rpx;
}

.icon-btn {
	padding: 16rpx;
}

.brand-title {
	font-family: 'Manrope', sans-serif;
	font-size: 40rpx;
	font-weight: 700;
	color: #18181b;
	letter-spacing: -0.02em;
}

/* ========== 主内容区 ========== */

.main-content {
	padding: 192rpx 48rpx 0;
	max-width: 896rpx;
	margin: 0 auto;
}

.page-title {
	font-family: 'Manrope', sans-serif;
	font-size: 60rpx;
	font-weight: 800;
	color: $color-on-surface;
	letter-spacing: -0.02em;
	margin-bottom: 48rpx;
}

/* ========== 论文卡片 ========== */

.paper-list {
	display: flex;
	flex-direction: column;
	gap: 48rpx;
}

.paper-card {
	background-color: $color-surface-container-lowest;
	border-radius: 24rpx;
	padding: 48rpx;
	box-shadow: 0 16rpx 60rpx rgba(0, 0, 0, 0.04);
	transition: all 0.3s ease;
}

.paper-card:active {
	box-shadow: 0 16rpx 80rpx rgba(0, 0, 0, 0.08);
	transform: scale(0.99);
}

.card-top {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: flex-start;
	margin-bottom: 24rpx;
}

.source-badge {
	background-color: $color-surface-container-high;
	color: $color-on-surface-variant;
	font-family: 'Inter', sans-serif;
	font-size: 20rpx;
	font-weight: 700;
	letter-spacing: 0.1em;
	padding: 8rpx 20rpx;
	border-radius: 999rpx;
}

.bookmark-btn {
	padding: 12rpx;
	margin-top: -12rpx;
	margin-right: -12rpx;
}

.icon-dim {
	opacity: 0.2;
}

.paper-card:active .icon-dim {
	opacity: 0.5;
}

.card-title {
	font-family: 'Manrope', sans-serif;
	font-size: 40rpx;
	font-weight: 700;
	color: $color-on-surface;
	line-height: 1.25;
	margin-bottom: 16rpx;
}

.card-authors {
	font-family: 'Inter', sans-serif;
	font-size: 28rpx;
	font-weight: 500;
	color: $color-on-secondary-container;
	margin-bottom: 24rpx;
}

.card-abstract {
	font-family: 'Inter', sans-serif;
	font-size: 28rpx;
	color: $color-on-surface-variant;
	line-height: 1.6;
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 3;
	-webkit-box-orient: vertical;
}

/* ========== 加载状态 ========== */

.loading-state {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 128rpx;
}

.loading-text {
	font-family: 'Inter', sans-serif;
	font-size: 34rpx;
	color: $color-on-surface-variant;
}

/* ========== 空状态 ========== */

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 128rpx;
}

.empty-text {
	font-family: 'Inter', sans-serif;
	font-size: 34rpx;
	color: $color-on-surface-variant;
	margin-top: 32rpx;
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
	padding: 24rpx 32rpx 48rpx;
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

.nav-item:active {
	transform: scale(0.9);
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