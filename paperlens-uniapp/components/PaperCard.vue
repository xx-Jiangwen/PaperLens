<template>
	<view class="paper-card" @tap="onTap">
		<!-- 顶部：来源标签 + 收藏按钮 -->
		<view class="card-top">
			<view class="source-badge">{{ displaySource }}</view>
			<view class="bookmark-btn" @tap.stop="onBookmark">
				<text class="bookmark-icon" :class="{ bookmarked: isBookmarked }">bookmark</text>
			</view>
		</view>

		<!-- 标题 -->
		<view class="card-title">{{ paper.title }}</view>

		<!-- 作者 -->
		<view class="card-authors">{{ authorText }}</view>

		<!-- 摘要预览 -->
		<view class="card-abstract">{{ paper.abstract }}</view>
	</view>
</template>

<script>
export default {
	name: 'PaperCard',

	props: {
		paper: {
			type: Object,
			default: () => ({})
		},
		isBookmarked: {
			type: Boolean,
			default: false
		}
	},

	computed: {
		displaySource() {
			if (this.paper.arxiv_id) {
				return `ARXIV:${this.paper.arxiv_id}`
			}
			if (this.paper.categories && this.paper.categories.length > 0) {
				return this.paper.categories[0].toUpperCase()
			}
			return 'PAPER'
		},

		authorText() {
			if (!this.paper.authors || this.paper.authors.length === 0) return ''
			const first = this.paper.authors[0]
			const more = this.paper.authors.length > 1 ? ' 等' : ''
			return `${first}${more}`
		}
	},

	methods: {
		onTap() {
			this.$emit('select', this.paper)
		},

		onBookmark() {
			this.$emit('bookmark', this.paper)
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.paper-card {
	background-color: $color-surface-container-lowest;
	border-radius: 24rpx;
	padding: 48rpx;
	margin-bottom: 48rpx;
	box-shadow: 0 16rpx 60rpx rgba(0, 0, 0, 0.04);
	transition: all 0.3s ease;
}

.paper-card:active {
	box-shadow: 0 16rpx 80rpx rgba(0, 0, 0, 0.08);
	transform: scale(0.99);
}

/* ========== 顶部区域 ========== */

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

.bookmark-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 48rpx;
	color: $color-primary-container;
	opacity: 0.2;
	transition: opacity 0.2s ease;
}

.paper-card:active .bookmark-icon:not(.bookmarked) {
	opacity: 0.5;
}

.bookmark-icon.bookmarked {
	opacity: 1;
}

/* ========== 标题 ========== */

.card-title {
	font-family: 'Manrope', sans-serif;
	font-size: 40rpx;
	font-weight: 700;
	color: $color-on-surface;
	line-height: 1.25;
	margin-bottom: 16rpx;
	transition: color 0.2s ease;
}

.paper-card:active .card-title {
	color: $color-primary-container;
}

/* ========== 作者 ========== */

.card-authors {
	font-family: 'Inter', sans-serif;
	font-size: 28rpx;
	font-weight: 500;
	color: $color-on-secondary-container;
	margin-bottom: 24rpx;
}

/* ========== 摘要预览 ========== */

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
</style>