<template>
	<view class="page">
		<!-- 加载状态 -->
		<view v-if="loading" class="loading">
			<text>加载中...</text>
		</view>

		<!-- 论文详情 -->
		<view v-else-if="paper" class="content">
			<!-- 标题 -->
			<view class="title">{{ paper.title }}</view>

			<!-- 作者 -->
			<view class="authors">{{ authorText }}</view>

			<!-- 分类标签 -->
			<view class="tags">
				<view
					v-for="(cat, index) in paper.categories"
					:key="index"
					class="tag"
				>{{ cat }}</view>
			</view>

			<!-- AI 摘要 -->
			<view class="section">
				<view class="section-header" @tap="toggleSummary">
					<text class="section-title">AI 结构化摘要</text>
					<text class="section-toggle">{{ summaryExpanded ? '收起' : '展开' }}</text>
				</view>

				<view v-show="summaryExpanded">
					<view v-if="paper.summary_status === 'done'" class="summary-content">
						<view class="summary-item">
							<view class="summary-label">What（问题与方案）</view>
							<view class="summary-text">{{ paper.summary_what }}</view>
						</view>
						<view class="summary-item">
							<view class="summary-label">How（技术路径）</view>
							<view class="summary-text">{{ paper.summary_how }}</view>
						</view>
						<view class="summary-item">
							<view class="summary-label">Why（贡献与意义）</view>
							<view class="summary-text">{{ paper.summary_why }}</view>
						</view>
						<view class="disclaimer">内容由 AI 生成，请以原文为准</view>
					</view>

					<view v-else-if="paper.summary_status === 'processing'" class="summary-status">
						<text>AI 摘要生成中...</text>
					</view>

					<view v-else class="summary-status">
						<text>暂无 AI 摘要</text>
					</view>
				</view>
			</view>

			<!-- 原文摘要 -->
			<view class="section">
				<view class="section-header" @tap="toggleAbstract">
					<text class="section-title">原文摘要</text>
					<text class="section-toggle">{{ abstractExpanded ? '收起' : '展开' }}</text>
				</view>
				<view v-show="abstractExpanded" class="abstract-text">
					{{ paper.abstract }}
				</view>
			</view>
		</view>

		<!-- 底部操作栏 -->
		<view v-if="paper" class="bottom-bar">
			<view class="action-btn" @tap="onBookmark">
				<text class="icon">{{ isBookmarked ? '★' : '☆' }}</text>
				<text class="label">{{ isBookmarked ? '已收藏' : '收藏' }}</text>
			</view>
			<view class="action-btn" @tap="onShare">
				<text class="icon">↗</text>
				<text class="label">分享</text>
			</view>
			<view class="action-btn primary" @tap="openPdf">
				<text class="label">打开原文</text>
			</view>
		</view>
	</view>
</template>

<script>
import { usePapersStore } from '@/stores/papers.js'
import { useBookmarksStore } from '@/stores/bookmarks.js'

export default {
	setup() {
		const papersStore = usePapersStore()
		const bookmarksStore = useBookmarksStore()
		return { papersStore, bookmarksStore }
	},

	data() {
		return {
			summaryExpanded: true,
			abstractExpanded: false
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
		toggleSummary() {
			this.summaryExpanded = !this.summaryExpanded
		},

		toggleAbstract() {
			this.abstractExpanded = !this.abstractExpanded
		},

		async onBookmark() {
			if (!this.paper) return
			const res = await this.bookmarksStore.toggleBookmark(this.paper.id)
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

		openPdf() {
			if (!this.paper || !this.paper.pdf_url) return
			uni.setClipboardData({
				data: this.paper.pdf_url,
				success: () => {
					uni.showToast({ title: 'PDF 链接已复制', icon: 'success' })
				}
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
	padding-bottom: 120rpx;
}

.content {
	padding: $spacing-4;
}

.loading {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 60vh;
	color: $color-text-secondary;
	font-size: $font-size-body;
}

.title {
	font-size: $font-size-title2;
	font-weight: $font-weight-bold;
	color: $color-text-primary;
	line-height: $line-height-normal;
	margin-bottom: $spacing-3;
}

.authors {
	font-size: $font-size-subheadline;
	color: $color-text-secondary;
	margin-bottom: $spacing-3;
}

.tags {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	margin-bottom: $spacing-4;
}

.tag {
	display: inline-flex;
	align-items: center;
	height: 48rpx;
	padding: 0 $spacing-3;
	background-color: $color-primary-light;
	color: $color-primary;
	border-radius: 12rpx;
	font-size: $font-size-footnote;
	font-weight: $font-weight-medium;
	margin-right: $spacing-2;
}

.section {
	background-color: $color-bg-card;
	border-radius: $radius-md;
	padding: $spacing-4;
	margin-bottom: $spacing-4;
}

.section-header {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
}

.section-title {
	font-size: $font-size-headline;
	font-weight: $font-weight-semibold;
	color: $color-text-primary;
}

.section-toggle {
	font-size: $font-size-subheadline;
	color: $color-primary;
}

.summary-content {
	margin-top: $spacing-4;
}

.summary-item {
	margin-bottom: $spacing-4;
}

.summary-item:last-child {
	margin-bottom: 0;
}

.summary-label {
	font-size: $font-size-footnote;
	font-weight: $font-weight-semibold;
	color: $color-primary;
	margin-bottom: $spacing-2;
}

.summary-text {
	font-size: $font-size-body;
	color: $color-text-secondary;
	line-height: $line-height-relaxed;
}

.disclaimer {
	font-size: $font-size-caption;
	color: $color-text-tertiary;
	margin-top: $spacing-4;
	padding-top: $spacing-3;
	border-top: 1rpx solid $color-separator;
}

.summary-status {
	margin-top: $spacing-4;
	color: $color-text-tertiary;
	font-size: $font-size-body;
	text-align: center;
	padding: $spacing-4;
}

.abstract-text {
	margin-top: $spacing-4;
	font-size: $font-size-body;
	color: $color-text-secondary;
	line-height: $line-height-relaxed;
}

.bottom-bar {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	flex-direction: row;
	align-items: center;
	height: 112rpx;
	background-color: $color-bg;
	border-top: 1rpx solid $color-separator;
	padding: 0 $spacing-4;
	padding-bottom: env(safe-area-inset-bottom);
}

.action-btn {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 0 $spacing-4;
}

.action-btn .icon {
	font-size: 40rpx;
	margin-bottom: 4rpx;
}

.action-btn .label {
	font-size: $font-size-caption;
	color: $color-text-secondary;
}

.action-btn.primary {
	flex: 1;
	margin-left: auto;
	background-color: $color-primary;
	border-radius: $radius-sm;
	height: 72rpx;
}

.action-btn.primary .label {
	color: #FFFFFF;
	font-size: $font-size-body;
	font-weight: $font-weight-semibold;
}
</style>