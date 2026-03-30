<template>
	<view class="page">
		<!-- 搜索框 -->
		<view class="search-header">
			<view class="search-bar">
				<text class="search-icon">🔍</text>
				<input
					class="search-input"
					v-model="query"
					placeholder="搜索论文标题、作者、摘要..."
					:focus="true"
					@confirm="onSearch"
					@input="onInput"
				/>
				<text v-if="query" class="clear-btn" @tap="clearQuery">✕</text>
			</view>
			<text class="cancel-btn" @tap="goBack">取消</text>
		</view>

		<!-- 搜索历史 -->
		<view v-if="!query && recentSearches.length > 0" class="history-section">
			<view class="section-header">
				<text class="section-title">搜索历史</text>
				<text class="clear-history" @tap="clearHistory">清空</text>
			</view>
			<view class="history-list">
				<view
					v-for="(item, index) in recentSearches"
					:key="index"
					class="history-item"
					:data-query="item"
					@tap="useHistory"
				>{{ item }}</view>
			</view>
		</view>

		<!-- 加载状态 -->
		<view v-if="loading" class="loading">
			<text>搜索中...</text>
		</view>

		<!-- 搜索结果 -->
		<view v-else-if="results.length > 0" class="results">
			<PaperCard
				v-for="paper in results"
				:key="paper.id"
				:paper="paper"
				:show-actions="false"
				@select="goToDetail"
			/>
		</view>

		<!-- 空状态 -->
		<view v-else-if="query && searched" class="empty">
			<text class="empty-icon">🔍</text>
			<text class="empty-text">未找到相关论文</text>
		</view>
	</view>
</template>

<script>
import PaperCard from '@/components/PaperCard.vue'
import { searchPapers } from '@/api/papers.js'

export default {
	components: {
		PaperCard
	},

	data() {
		return {
			query: '',
			results: [],
			loading: false,
			searched: false,
			recentSearches: []
		}
	},

	onLoad() {
		this.loadHistory()
	},

	methods: {
		loadHistory() {
			const history = uni.getStorageSync('search_history') || []
			this.recentSearches = history.slice(0, 10)
		},

		saveHistory(query) {
			if (!query) return
			let history = uni.getStorageSync('search_history') || []
			history = history.filter(h => h !== query)
			history.unshift(query)
			history = history.slice(0, 10)
			uni.setStorageSync('search_history', history)
			this.recentSearches = history
		},

		clearHistory() {
			uni.removeStorageSync('search_history')
			this.recentSearches = []
		},

		onInput(e) {
			this.query = e.detail.value
		},

		clearQuery() {
			this.query = ''
			this.results = []
			this.searched = false
		},

		async onSearch() {
			if (!this.query.trim()) return

			this.loading = true
			this.searched = true

			try {
				const res = await searchPapers(this.query.trim())
				if (res.code === 200 && res.data) {
					this.results = res.data
					this.saveHistory(this.query.trim())
				} else {
					uni.showToast({ title: res.msg || '搜索失败', icon: 'none' })
				}
			} catch (e) {
				uni.showToast({ title: '搜索失败', icon: 'none' })
			} finally {
				this.loading = false
			}
		},

		useHistory(e) {
			this.query = e.currentTarget.dataset.query
			this.onSearch()
		},

		goBack() {
			uni.navigateBack()
		},

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
	background-color: $color-bg-grouped;
}

.search-header {
	display: flex;
	flex-direction: row;
	align-items: center;
	padding: $spacing-2 $spacing-4;
	background-color: $color-bg;
}

.search-bar {
	flex: 1;
	display: flex;
	flex-direction: row;
	align-items: center;
	height: 72rpx;
	background-color: $color-bg-grouped;
	border-radius: $radius-sm;
	padding: 0 $spacing-3;
}

.search-icon {
	font-size: $font-size-body;
	opacity: 0.5;
	margin-right: $spacing-2;
}

.search-input {
	flex: 1;
	height: 72rpx;
	font-size: $font-size-body;
	color: $color-text-primary;
}

.clear-btn {
	font-size: $font-size-body;
	color: $color-text-tertiary;
	padding: $spacing-2;
}

.cancel-btn {
	margin-left: $spacing-3;
	font-size: $font-size-body;
	color: $color-primary;
}

.history-section {
	padding: $spacing-4;
}

.section-header {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	margin-bottom: $spacing-3;
}

.section-title {
	font-size: $font-size-headline;
	font-weight: $font-weight-semibold;
	color: $color-text-primary;
}

.clear-history {
	font-size: $font-size-subheadline;
	color: $color-text-tertiary;
}

.history-list {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
}

.history-item {
	padding: $spacing-2 $spacing-4;
	background-color: $color-bg-card;
	color: $color-text-secondary;
	border-radius: $radius-full;
	font-size: $font-size-subheadline;
	margin-right: $spacing-2;
	margin-bottom: $spacing-2;
}

.results {
	padding: $spacing-4;
}

.loading {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 40vh;
	color: $color-text-secondary;
	font-size: $font-size-body;
}

.empty {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 40vh;
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