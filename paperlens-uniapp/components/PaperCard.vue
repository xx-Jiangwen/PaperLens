<template>
	<view class="paper-card" @tap="onTap">
		<!-- 顶部：来源标签 + 收藏按钮 -->
		<view class="card-top">
			<view class="source-badge">{{ displaySource }}</view>
			<view class="bookmark-btn" @tap.stop="onBookmark">
				<MdIcon
					name="bookmark"
					size="48"
					:color="isBookmarked ? '#0066cc' : '#0066cc'"
					:filled="isBookmarked"
					:class="{ 'icon-dim': !isBookmarked }"
				/>
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
import MdIcon from '@/components/MdIcon.vue'

export default {
	name: 'PaperCard',
	components: {
		MdIcon
	},

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
.paper-card {
	background-color: #ffffff;
	border-radius: 12px;
	padding: 20px;
	margin-bottom: 20px;
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
	transition: all 0.3s ease;
	width: 100%;
	box-sizing: border-box;
	overflow: hidden;
}

.paper-card:active {
	box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
	transform: scale(0.98);
}

/* ========== 顶部区域 ========== */

.card-top {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: flex-start;
	margin-bottom: 12px;
	width: 100%;
}

.source-badge {
	background-color: #e8e8ea;
	color: #414753;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 10px;
	font-weight: 700;
	letter-spacing: 0.1em;
	padding: 4px 10px;
	border-radius: 999px;
	flex-shrink: 0;
}

.bookmark-btn {
	padding: 6px;
	margin-top: -6px;
	margin-right: -6px;
	flex-shrink: 0;
}

.icon-dim {
	opacity: 0.2;
}

.paper-card:active .icon-dim {
	opacity: 0.5;
}

/* ========== 标题 ========== */

.card-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 18px;
	font-weight: 700;
	color: #1a1c1d;
	line-height: 1.3;
	margin-bottom: 8px;
	transition: color 0.2s ease;
	word-break: break-word;
	overflow-wrap: break-word;
}

.paper-card:active .card-title {
	color: #0066cc;
}

/* ========== 作者 ========== */

.card-authors {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 500;
	color: #626267;
	margin-bottom: 12px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

/* ========== 摘要预览 ========== */

.card-abstract {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	color: #414753;
	line-height: 1.6;
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 3;
	-webkit-box-orient: vertical;
	word-break: break-word;
}
</style>