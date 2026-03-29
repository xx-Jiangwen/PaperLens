<template>
	<view class="paper-card" @tap="onTap">
		<!-- 分类标签 -->
		<view class="tags">
			<view
				v-for="(cat, index) in displayCategories"
				:key="index"
				class="tag"
			>{{ cat }}</view>
		</view>

		<!-- 标题 -->
		<view class="title">{{ paper.title }}</view>

		<!-- 作者 -->
		<view class="authors">{{ authorText }}</view>

		<!-- 摘要预览 -->
		<view class="abstract">{{ paper.abstract }}</view>

		<!-- AI 摘要状态 -->
		<view :class="['summary-status', paper.summary_status]">
			<text class="status-dot"></text>
			{{ statusText }}
		</view>

		<!-- 操作按钮 -->
		<view v-if="showActions" class="actions">
			<view class="action-btn bookmark" @tap.stop="onBookmark">
				<text class="icon">{{ isBookmarked ? '★' : '☆' }}</text>
				<text class="label">{{ isBookmarked ? '已收藏' : '收藏' }}</text>
			</view>
			<view class="action-btn skip" @tap.stop="onSkip">
				<text class="icon">✕</text>
				<text class="label">跳过</text>
			</view>
		</view>
	</view>
</template>

<script>
/**
 * PaperCard - 论文卡片组件
 * @description 展示论文信息的卡片，支持收藏和跳过操作
 */

export default {
	name: 'PaperCard',

	props: {
		/**
		 * 论文数据
		 */
		paper: {
			type: Object,
			default: () => ({})
		},
		/**
		 * 是否显示操作按钮
		 */
		showActions: {
			type: Boolean,
			default: false
		},
		/**
		 * 是否已收藏
		 */
		isBookmarked: {
			type: Boolean,
			default: false
		}
	},

	computed: {
		/**
		 * 显示的分类（最多2个）
		 */
		displayCategories() {
			if (!this.paper.categories) return []
			return this.paper.categories.slice(0, 2)
		},

		/**
		 * 作者文本
		 */
		authorText() {
			if (!this.paper.authors || this.paper.authors.length === 0) return ''
			const first = this.paper.authors[0]
			const more = this.paper.authors.length > 1 ? ' 等' : ''
			return `${first}${more}`
		},

		/**
		 * 状态文本
		 */
		statusText() {
			const statusMap = {
				'done': 'AI摘要已生成',
				'processing': 'AI摘要生成中',
				'pending': '待生成摘要',
				'failed': '生成失败'
			}
			return statusMap[this.paper.summary_status] || ''
		}
	},

	methods: {
		onTap() {
			this.$emit('tap', this.paper)
		},

		onBookmark() {
			this.$emit('bookmark', this.paper)
		},

		onSkip() {
			this.$emit('skip', this.paper)
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.paper-card {
	background-color: $color-bg-card;
	border-radius: $radius-md;
	padding: $spacing-4;
	margin-bottom: $spacing-4;
}

.tags {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	margin-bottom: $spacing-2;
}

.tag {
	display: inline-flex;
	align-items: center;
	height: 40rpx;
	padding: 0 $spacing-2;
	background-color: $color-primary-light;
	color: $color-primary;
	border-radius: 8rpx;
	font-size: $font-size-caption;
	font-weight: $font-weight-medium;
	margin-right: $spacing-1;
}

.title {
	font-size: $font-size-headline;
	font-weight: $font-weight-semibold;
	color: $color-text-primary;
	line-height: $line-height-normal;
	margin-bottom: $spacing-2;
}

.authors {
	font-size: $font-size-footnote;
	color: $color-text-secondary;
	margin-bottom: $spacing-2;
}

.abstract {
	font-size: $font-size-subheadline;
	color: $color-text-secondary;
	line-height: $line-height-relaxed;
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	margin-bottom: $spacing-3;
}

.summary-status {
	display: flex;
	flex-direction: row;
	align-items: center;
	font-size: $font-size-caption;
	color: $color-text-tertiary;
}

.status-dot {
	width: 12rpx;
	height: 12rpx;
	border-radius: 50%;
	background-color: $color-text-tertiary;
	margin-right: $spacing-1;
}

.summary-status.done .status-dot {
	background-color: $color-success;
}

.summary-status.done {
	color: $color-success;
}

.summary-status.processing .status-dot {
	background-color: $color-warning;
}

.summary-status.processing {
	color: $color-warning;
}

.summary-status.failed .status-dot {
	background-color: $color-error;
}

.summary-status.failed {
	color: $color-error;
}

.actions {
	display: flex;
	flex-direction: row;
	margin-top: $spacing-4;
	padding-top: $spacing-3;
	border-top: 1rpx solid $color-separator;
}

.action-btn {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
	flex: 1;
	height: 64rpx;
	border-radius: $radius-sm;
	font-size: $font-size-footnote;
	font-weight: $font-weight-medium;
	transition: opacity $duration-fast;
}

.action-btn:active {
	opacity: 0.7;
}

.action-btn .icon {
	margin-right: $spacing-1;
	font-size: $font-size-body;
}

.action-btn.bookmark {
	background-color: $color-primary-light;
	color: $color-primary;
}

.action-btn.skip {
	background-color: $color-bg-grouped;
	color: $color-text-secondary;
	margin-left: $spacing-2;
}
</style>