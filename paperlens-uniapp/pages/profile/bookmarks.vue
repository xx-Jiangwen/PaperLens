<template>
	<view class="page">
		<!-- 加载状态 -->
		<view v-if="loading && bookmarks.length === 0" class="loading">
			<text>加载中...</text>
		</view>

		<!-- 收藏列表 -->
		<view v-else-if="bookmarks.length > 0" class="bookmark-list">
			<PaperCard
				v-for="bookmark in bookmarks"
				:key="bookmark.id"
				:paper="bookmark.paper || bookmark"
				:show-actions="false"
				:is-bookmarked="true"
				@tap="goToDetail"
			/>
		</view>

		<!-- 空状态 -->
		<view v-else class="empty">
			<text class="empty-icon">📚</text>
			<text class="empty-text">暂无收藏</text>
			<text class="empty-hint">去首页发现感兴趣的论文吧</text>
		</view>
	</view>
</template>

<script>
import PaperCard from '@/components/PaperCard.vue'
import { useBookmarksStore } from '@/stores/bookmarks.js'

export default {
	components: {
		PaperCard
	},

	setup() {
		const bookmarksStore = useBookmarksStore()
		return { bookmarksStore }
	},

	computed: {
		bookmarks() {
			return this.bookmarksStore.bookmarks
		},
		loading() {
			return this.bookmarksStore.loading
		}
	},

	onLoad() {
		this.bookmarksStore.fetchBookmarks(true)
	},

	onPullDownRefresh() {
		this.bookmarksStore.fetchBookmarks(true).finally(() => {
			uni.stopPullDownRefresh()
		})
	},

	onReachBottom() {
		if (this.bookmarksStore.hasMore && !this.loading) {
			this.bookmarksStore.fetchBookmarks()
		}
	},

	methods: {
		goToDetail(paper) {
			const paperId = paper.id || paper.paper_id
			uni.navigateTo({
				url: `/pages/home/detail?id=${encodeURIComponent(paperId)}`
			})
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

.loading {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 60vh;
	color: $color-text-secondary;
	font-size: $font-size-body;
}

.bookmark-list {
	padding: $spacing-4;
}

.empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 60vh;
}

.empty-icon {
	font-size: 96rpx;
	margin-bottom: $spacing-4;
	opacity: 0.5;
}

.empty-text {
	font-size: $font-size-title3;
	font-weight: $font-weight-semibold;
	color: $color-text-primary;
	margin-bottom: $spacing-2;
}

.empty-hint {
	font-size: $font-size-subheadline;
	color: $color-text-secondary;
}
</style>