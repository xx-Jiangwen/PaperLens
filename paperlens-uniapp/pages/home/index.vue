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
					<text class="search-icon" @tap="goToSearch">🔍</text>
					<text class="brand-name">PaperLens</text>
				</view>
			</view>
			<view class="header-divider"></view>
		</view>

		<!-- Hero 区域 -->
		<view class="hero-section">
			<text class="hero-label">CURATED INSIGHTS</text>
			<view class="hero-title">
				<text class="hero-title-main">Discovery Through</text>
				<text class="hero-title-accent">Intellectual Rigor</text>
			</view>
			<view class="hero-divider"></view>
		</view>

		<!-- 分类筛选器 -->
		<scroll-view class="filter-section" scroll-x="true">
			<view
				v-for="filter in filterOptions"
				:key="filter.value"
				:class="['filter-tag', { active: activeFilter === filter.value }]"
				:data-value="filter.value"
				@tap="onFilterChange"
			>{{ filter.label }}</view>
		</scroll-view>

		<!-- 论文列表 -->
		<view class="content">
			<!-- 加载状态 -->
			<view v-if="loading && papers.length === 0" class="loading">
				<text>加载中...</text>
			</view>

			<!-- 论文列表 -->
			<view v-else class="paper-list">
				<PaperCard
					v-for="paper in papers"
					:key="paper.id"
					:paper="paper"
					@select="goToDetail"
				/>
			</view>

			<!-- 空状态 -->
			<view v-if="!loading && papers.length === 0" class="empty">
				<text class="empty-icon">📭</text>
				<text class="empty-text">暂无论文</text>
			</view>

			<!-- 加载更多 -->
			<view v-if="papers.length > 0 && hasMore" class="load-more">
				<text v-if="loading">加载中...</text>
				<text v-else>上拉加载更多</text>
			</view>
		</view>

		<!-- 自定义底部导航 -->
		<TabBar current-path="/pages/home/index" />
	</view>
</template>

<script>
import PaperCard from '@/components/PaperCard.vue'
import TabBar from '@/components/TabBar.vue'
import { usePapersStore } from '@/stores/papers.js'

export default {
	components: {
		PaperCard,
		TabBar
	},

	data() {
		return {
			activeFilter: 'recent',
			filterOptions: [
				{ value: 'recent', label: 'RECENT' },
				{ value: 'featured', label: 'FEATURED' },
				{ value: 'cv', label: 'CV' },
				{ value: 'nlp', label: 'NLP' },
				{ value: 'ml', label: 'ML' }
			]
		}
	},

	computed: {
		papers() {
			// 根据筛选条件返回不同列表
			if (this.activeFilter === 'recent' || this.activeFilter === 'featured') {
				return this.papersStore.featuredPapers
			}
			return this.papersStore.allPapers.filter(paper => {
				if (!paper.categories) return false
				return paper.categories.some(cat => {
					const catLower = cat.toLowerCase()
					if (this.activeFilter === 'cv') return catLower.includes('cv')
					if (this.activeFilter === 'nlp') return catLower.includes('cl') || catLower.includes('nlp')
					if (this.activeFilter === 'ml') return catLower.includes('lg') || catLower.includes('ml')
					return false
				})
			})
		},
		loading() {
			return this.papersStore.featuredLoading || this.papersStore.allLoading
		},
		hasMore() {
			return this.papersStore.allHasMore
		}
	},

	setup() {
		const papersStore = usePapersStore()
		return { papersStore }
	},

	onLoad() {
		this.loadData()
	},

	onPullDownRefresh() {
		this.loadData().finally(() => {
			uni.stopPullDownRefresh()
		})
	},

	onReachBottom() {
		if (this.activeFilter !== 'recent' && this.hasMore && !this.loading) {
			this.papersStore.fetchAllPapers()
		}
	},

	methods: {
		/**
		 * 加载数据
		 */
		async loadData() {
			await this.papersStore.fetchFeaturedPapers()
		},

		/**
		 * 筛选器切换
		 */
		onFilterChange(e) {
			const value = e.currentTarget.dataset.value
			this.activeFilter = value
			if (value !== 'recent' && value !== 'featured' && this.papersStore.allPapers.length === 0) {
				this.papersStore.fetchAllPapers(true)
			}
		},

		/**
		 * 跳转搜索页
		 */
		goToSearch() {
			uni.navigateTo({
				url: '/pages/home/search'
			})
		},

		/**
		 * 跳转详情页
		 */
		goToDetail(paper) {
			uni.navigateTo({
				url: `/pages/home/detail?id=${encodeURIComponent(paper.id)}`
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
	padding-bottom: 160rpx; // 为底部导航留空间
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
	gap: $spacing-4;
}

.search-icon {
	font-size: 36rpx;
	color: $color-text-secondary;
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
}

.hero-title-main {
	font-family: $font-family-headline;
	font-size: $font-size-headline-xl;
	font-weight: $font-weight-bold;
	color: $color-primary;
	line-height: $line-height-tight;
}

.hero-title-accent {
	font-family: $font-family-headline;
	font-size: $font-size-headline-xl;
	font-weight: $font-weight-bold;
	font-style: italic;
	color: $color-primary;
	line-height: $line-height-tight;
}

.hero-divider {
	width: 96rpx;
	height: 4rpx;
	background-color: $color-primary-container;
	border-radius: $radius-full;
	margin-top: $spacing-6;
}

/* ========== 分类筛选器 ========== */

.filter-section {
	white-space: nowrap;
	padding: 0 $spacing-6 $spacing-4;
}

.filter-tag {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	height: 44rpx;
	padding: 0 $spacing-4;
	background-color: $color-surface-variant;
	color: $color-on-surface-variant;
	border-radius: $radius-full;
	font-family: $font-family-label;
	font-size: $font-size-label-xs;
	font-weight: $font-weight-bold;
	letter-spacing: $letter-spacing-widest;
	text-transform: uppercase;
	margin-right: $spacing-2;
	transition: all $duration-fast;
}

.filter-tag.active {
	background-color: $color-primary-container;
	color: $color-on-primary;
}

/* ========== 内容区域 ========== */

.content {
	padding: $spacing-6;
}

.paper-list {
	// 论文卡片自带 padding-bottom
}

.loading {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: $spacing-8;
	color: $color-text-secondary;
	font-family: $font-family-body;
	font-size: $font-size-body;
}

.load-more {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: $spacing-4;
	color: $color-text-tertiary;
	font-family: $font-family-body;
	font-size: $font-size-footnote;
}

.empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: $spacing-16;
}

.empty-icon {
	font-size: 96rpx;
	margin-bottom: $spacing-4;
	opacity: 0.5;
}

.empty-text {
	font-family: $font-family-body;
	font-size: $font-size-body;
	color: $color-text-secondary;
}
</style>