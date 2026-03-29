<template>
	<view class="page">
		<!-- 搜索栏 -->
		<view class="search-section">
			<SearchBar
				placeholder="搜索论文"
				:readonly="true"
				@tap="goToSearch"
			/>
		</view>

		<!-- Tab 切换 -->
		<view class="tab-section">
			<SegmentedControl
				:options="tabOptions"
				:value="activeTab"
				@change="onTabChange"
			/>
		</view>

		<!-- 精选 Tab 内容 -->
		<view v-show="activeTab === 'featured'" class="content">
			<!-- 加载状态 -->
			<view v-if="featuredLoading && featuredPapers.length === 0" class="loading">
				<text>加载中...</text>
			</view>

			<!-- 论文列表 -->
			<view v-else class="paper-list">
				<PaperCard
					v-for="paper in featuredPapers"
					:key="paper.id"
					:paper="paper"
					:show-actions="true"
					:is-bookmarked="isBookmarked(paper.id)"
					@tap="goToDetail"
					@bookmark="onBookmark"
					@skip="onSkip"
				/>
			</view>

			<!-- 空状态 -->
			<view v-if="!featuredLoading && featuredPapers.length === 0" class="empty">
				<text class="empty-icon">📭</text>
				<text class="empty-text">暂无精选论文</text>
			</view>
		</view>

		<!-- 全部 Tab 内容 -->
		<view v-show="activeTab === 'all'" class="content">
			<!-- 数据源筛选 -->
			<scroll-view class="source-filter" scroll-x="true">
				<view
					v-for="source in sources"
					:key="source.value"
					:class="['source-tag', { active: selectedSource === source.value }]"
					:data-value="source.value"
					@tap="onSourceChange"
				>{{ source.label }}</view>
			</scroll-view>

			<!-- 加载状态 -->
			<view v-if="allLoading && allPapers.length === 0" class="loading">
				<text>加载中...</text>
			</view>

			<!-- 论文列表 -->
			<view v-else class="paper-list">
				<PaperCard
					v-for="paper in allPapers"
					:key="paper.id"
					:paper="paper"
					:show-actions="false"
					:is-bookmarked="isBookmarked(paper.id)"
					@tap="goToDetail"
				/>
			</view>

			<!-- 加载更多 -->
			<view v-if="allPapers.length > 0 && allHasMore" class="load-more">
				<text v-if="allLoading">加载中...</text>
				<text v-else>上拉加载更多</text>
			</view>
		</view>
	</view>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue'
import SegmentedControl from '@/components/SegmentedControl.vue'
import PaperCard from '@/components/PaperCard.vue'
import { usePapersStore } from '@/stores/papers.js'
import { useBookmarksStore } from '@/stores/bookmarks.js'

export default {
	components: {
		SearchBar,
		SegmentedControl,
		PaperCard
	},

	data() {
		return {
			activeTab: 'featured',
			tabOptions: [
				{ value: 'featured', label: '精选' },
				{ value: 'all', label: '全部' }
			],
			sources: [
				{ value: null, label: '全部' },
				{ value: 'arxiv', label: 'arXiv' }
			],
			selectedSource: null
		}
	},

	computed: {
		featuredPapers() {
			return this.papersStore.featuredPapers
		},
		featuredLoading() {
			return this.papersStore.featuredLoading
		},
		allPapers() {
			return this.papersStore.allPapers
		},
		allLoading() {
			return this.papersStore.allLoading
		},
		allHasMore() {
			return this.papersStore.allHasMore
		}
	},

	setup() {
		const papersStore = usePapersStore()
		const bookmarksStore = useBookmarksStore()
		return { papersStore, bookmarksStore }
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
		if (this.activeTab === 'all' && this.allHasMore && !this.allLoading) {
			this.papersStore.fetchAllPapers()
		}
	},

	methods: {
		/**
		 * 加载数据
		 */
		async loadData() {
			await this.papersStore.fetchFeaturedPapers()
			if (this.activeTab === 'all') {
				await this.papersStore.fetchAllPapers(true)
			}
		},

		/**
		 * Tab 切换
		 */
		onTabChange(value) {
			this.activeTab = value
			if (value === 'all' && this.allPapers.length === 0) {
				this.papersStore.fetchAllPapers(true)
			}
		},

		/**
		 * 数据源切换
		 */
		onSourceChange(e) {
			const value = e.currentTarget.dataset.value
			this.selectedSource = value
			this.papersStore.setSelectedSource(value)
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
		},

		/**
		 * 是否已收藏
		 */
		isBookmarked(paperId) {
			return this.bookmarksStore.isBookmarked(paperId)
		},

		/**
		 * 收藏操作
		 */
		async onBookmark(paper) {
			const res = await this.bookmarksStore.toggleBookmark(paper.id)
			if (res.code === 200) {
				uni.showToast({
					title: this.isBookmarked(paper.id) ? '已取消收藏' : '已收藏',
					icon: 'success'
				})
			} else {
				uni.showToast({ title: res.msg || '操作失败', icon: 'none' })
			}
		},

		/**
		 * 跳过操作
		 */
		onSkip(paper) {
			// 从列表中移除
			const index = this.papersStore.featuredPapers.findIndex(p => p.id === paper.id)
			if (index > -1) {
				this.papersStore.featuredPapers.splice(index, 1)
			}
			uni.showToast({ title: '已跳过', icon: 'none' })
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

.search-section {
	padding: $spacing-4;
	background-color: $color-bg;
}

.tab-section {
	padding: 0 $spacing-4 $spacing-4;
	background-color: $color-bg;
}

.content {
	padding: $spacing-4;
}

.source-filter {
	white-space: nowrap;
	margin-bottom: $spacing-4;
}

.source-tag {
	display: inline-flex;
	align-items: center;
	height: 56rpx;
	padding: 0 $spacing-4;
	background-color: $color-bg-card;
	color: $color-text-secondary;
	border-radius: $radius-full;
	font-size: $font-size-subheadline;
	margin-right: $spacing-2;
}

.source-tag.active {
	background-color: $color-primary-light;
	color: $color-primary;
}

.paper-list {
	// 论文卡片自带 margin-bottom
}

.loading {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: $spacing-6;
	color: $color-text-secondary;
	font-size: $font-size-body;
}

.load-more {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: $spacing-4;
	color: $color-text-tertiary;
	font-size: $font-size-footnote;
}

.empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: $spacing-6 * 2;
}

.empty-icon {
	font-size: 96rpx;
	margin-bottom: $spacing-4;
	opacity: 0.5;
}

.empty-text {
	font-size: $font-size-body;
	color: $color-text-secondary;
}
</style>