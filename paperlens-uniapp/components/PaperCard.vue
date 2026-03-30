<template>
	<view class="paper-card" @tap="onTap">
		<!-- 分类标签 -->
		<view class="tags">
			<view
				v-for="(cat, index) in displayCategories"
				:key="index"
				:class="['tag', cat.isHighlight ? 'tag-tertiary' : 'tag-surface']"
			>{{ cat.text }}</view>
		</view>

		<!-- 标题 -->
		<view class="title">{{ paper.title }}</view>

		<!-- 作者 -->
		<view class="authors">{{ authorText }}</view>

		<!-- 摘要预览 -->
		<view class="abstract">{{ paper.abstract }}</view>

		<!-- AI 摘要状态 -->
		<view v-if="paper.summary_status" class="summary-status">
			<text class="status-text">{{ statusText }}</text>
		</view>
	</view>
</template>

<script>
/**
 * PaperCard - 论文卡片组件
 * @description 编辑部风格的文章列表式展示
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
		 * 是否显示操作按钮（已废弃，保留兼容）
		 */
		showActions: {
			type: Boolean,
			default: false
		},
		/**
		 * 是否已收藏（已废弃，保留兼容）
		 */
		isBookmarked: {
			type: Boolean,
			default: false
		}
	},

	computed: {
		/**
		 * 显示的分类（最多2个，带高亮标记）
		 */
		displayCategories() {
			if (!this.paper.categories) return []
			const cats = this.paper.categories.slice(0, 2)
			return cats.map((text, index) => ({
				text,
				isHighlight: index === 0 // 第一个标签用绿色高亮
			}))
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
		 * 状态文本（轻量版）
		 */
		statusText() {
			const statusMap = {
				'done': 'AI摘要',
				'processing': '生成中',
				'pending': '待生成',
				'failed': '生成失败'
			}
			return statusMap[this.paper.summary_status] || ''
		}
	},

	methods: {
		onTap() {
			this.$emit('select', this.paper)
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.paper-card {
	padding-bottom: $spacing-12;
	border-bottom: 1rpx solid $color-separator;
	opacity: 0.2;
}

.paper-card:last-child {
	border-bottom: none;
}

.tags {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	gap: $spacing-2;
	margin-bottom: $spacing-3;
}

.tag {
	display: inline-flex;
	align-items: center;
	height: 36rpx;
	padding: 0 $spacing-2;
	border-radius: 8rpx;
	font-size: $font-size-label-xs;
	font-weight: $font-weight-extrabold;
	letter-spacing: $letter-spacing-widest;
	text-transform: uppercase;
}

.tag-tertiary {
	background-color: $color-tertiary-fixed;
	color: $color-on-tertiary-container;
}

.tag-surface {
	background-color: $color-surface-variant;
	color: $color-on-surface-variant;
}

.title {
	font-family: $font-family-headline;
	font-size: $font-size-headline-lg;
	font-weight: $font-weight-bold;
	color: $color-primary;
	line-height: $line-height-normal;
	margin-bottom: $spacing-2;
}

.authors {
	font-family: $font-family-body;
	font-size: $font-size-footnote;
	font-weight: $font-weight-semibold;
	color: $color-text-secondary;
	margin-bottom: $spacing-3;
}

.abstract {
	font-family: $font-family-headline;
	font-style: italic;
	font-size: $font-size-subheadline;
	color: $color-text-secondary;
	line-height: $line-height-relaxed;
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 3;
	-webkit-box-orient: vertical;
}

.summary-status {
	margin-top: $spacing-2;
}

.status-text {
	font-family: $font-family-label;
	font-size: $font-size-label-xs;
	font-weight: $font-weight-bold;
	color: $color-tertiary-fixed-dim;
	letter-spacing: $letter-spacing-wide;
}
</style>