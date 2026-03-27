<template>
	<view class="container">
		<!-- 分类筛选 -->
		<scroll-view class="categories" scroll-x="true">
			<view
				v-for="(item, index) in categories"
				:key="index"
				:class="['cat-tag', activeCategory === item ? 'active' : '']"
				:data-cat="item"
				@tap="onCategoryTap"
			>
				{{ item }}
			</view>
		</scroll-view>

		<!-- 加载状态 -->
		<view v-if="loading" class="loading">
			<text>加载中...</text>
		</view>

		<!-- 论文列表 -->
		<view v-else class="papers">
			<view
				v-for="(paper, index) in papers"
				:key="paper.id"
				class="paper-card"
				:data-id="paper.id"
				@tap="onPaperTap"
			>
				<view class="tags">
					<text
						v-for="(cat, catIndex) in paper.categories.slice(0, 2)"
						:key="catIndex"
						class="tag"
					>{{ cat }}</text>
				</view>
				<view class="title">{{ paper.title }}</view>
				<view class="authors">{{ paper.authors[0] }}{{ paper.authors.length > 1 ? ' 等' : '' }}</view>
				<view :class="['summary-status', paper.summary_status]">
					{{ getStatusText(paper.summary_status) }}
				</view>
			</view>
		</view>

		<!-- 空状态 -->
		<view v-if="!loading && papers.length === 0" class="empty">
			<text>暂无论文</text>
		</view>
	</view>
</template>

<script>
import { getTodayPapers, getPapers } from '../../api/papers.js'

export default {
	data() {
		return {
			papers: [],
			loading: false,
			activeCategory: '全部',
			categories: ['全部', 'cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML']
		}
	},

	onLoad() {
		this.fetchPapers()
	},

	onPullDownRefresh() {
		this.fetchPapers().finally(() => {
			uni.stopPullDownRefresh()
		})
	},

	methods: {
		/**
		 * 获取状态文本
		 */
		getStatusText(status) {
			const statusMap = {
				'done': 'AI摘要已生成',
				'processing': 'AI摘要生成中',
				'pending': '待生成',
				'failed': '生成失败'
			}
			return statusMap[status] || '未知状态'
		},

		/**
		 * 获取论文列表
		 */
		async fetchPapers() {
			this.loading = true

			try {
				let res
				if (this.activeCategory && this.activeCategory !== '全部') {
					res = await getPapers({ category: this.activeCategory })
				} else {
					res = await getTodayPapers()
				}

				if (res.code === 200 && res.data) {
					this.papers = res.data
				} else {
					uni.showToast({ title: res.msg || '加载失败', icon: 'none' })
				}
			} catch (e) {
				uni.showToast({ title: '加载失败', icon: 'none' })
			} finally {
				this.loading = false
			}
		},

		/**
		 * 分类切换
		 */
		onCategoryTap(e) {
			const cat = e.currentTarget.dataset.cat
			this.activeCategory = cat
			this.fetchPapers()
		},

		/**
		 * 跳转详情
		 */
		onPaperTap(e) {
			const id = e.currentTarget.dataset.id
			uni.navigateTo({
				url: `/pages/detail/detail?id=${encodeURIComponent(id)}`
			})
		}
	}
}
</script>

<style lang="scss">
.container {
	min-height: 100vh;
	background-color: #0d1117;
	padding: 24rpx;
}

/* 分类筛选 */
.categories {
	white-space: nowrap;
	padding-bottom: 24rpx;
	margin-bottom: 24rpx;
	border-bottom: 1px solid #30363d;
}

.cat-tag {
	display: inline-block;
	padding: 12rpx 28rpx;
	background-color: #161b22;
	color: #8b949e;
	border-radius: 40rpx;
	margin-right: 16rpx;
	font-size: 24rpx;
}

.cat-tag.active {
	background-color: #1f4168;
	color: #58a6ff;
}

/* 论文卡片 */
.paper-card {
	background-color: #161b22;
	border-radius: 24rpx;
	padding: 32rpx;
	margin-bottom: 24rpx;
}

.tags {
	margin-bottom: 16rpx;
}

.tag {
	display: inline-block;
	padding: 4rpx 16rpx;
	background-color: #1f4168;
	color: #58a6ff;
	border-radius: 8rpx;
	font-size: 22rpx;
	margin-right: 8rpx;
}

.title {
	color: #e6edf3;
	font-size: 28rpx;
	font-weight: 500;
	margin-bottom: 12rpx;
	line-height: 1.4;
}

.authors {
	color: #8b949e;
	font-size: 24rpx;
	margin-bottom: 12rpx;
}

.summary-status {
	font-size: 22rpx;
	color: #8b949e;
}

.summary-status.done {
	color: #3fb950;
}

.summary-status.processing {
	color: #f0ad4e;
}

/* 加载状态 */
.loading {
	text-align: center;
	padding: 48rpx 0;
	color: #8b949e;
	font-size: 28rpx;
}

/* 空状态 */
.empty {
	text-align: center;
	padding: 96rpx 0;
	color: #8b949e;
	font-size: 28rpx;
}
</style>