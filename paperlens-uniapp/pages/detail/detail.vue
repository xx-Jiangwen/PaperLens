<template>
	<view class="container" v-if="paper">
		<!-- 标题 -->
		<view class="title">{{ paper.title }}</view>

		<!-- 作者 -->
		<view class="authors">{{ authorText }}</view>

		<!-- 分类标签 -->
		<view class="tags">
			<text
				v-for="(cat, index) in paper.categories"
				:key="index"
				class="tag"
			>{{ cat }}</text>
		</view>

		<!-- 操作按钮 -->
		<view class="action-btns">
			<button class="btn-secondary" @tap="openArxiv">复制链接</button>
			<button class="btn-primary" @tap="openPdf">查看 PDF</button>
		</view>

		<!-- AI 摘要 -->
		<view class="summary-section">
			<view class="section-title">AI 结构化摘要</view>

			<view v-if="paper.summary_status === 'done'">
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

				<button class="btn-ghost" @tap="copySummary">复制摘要文本</button>
			</view>

			<view v-else-if="paper.summary_status === 'processing'" class="empty">
				AI 摘要生成中...
			</view>

			<view v-else class="empty">
				暂无 AI 摘要，将在后台自动生成
			</view>
		</view>

		<!-- 原文摘要 -->
		<view class="abstract-section">
			<view class="section-title">原文摘要（英文）</view>
			<view class="abstract-text">{{ paper.abstract }}</view>
		</view>
	</view>
</template>

<script>
import { getPaper } from '../../api/papers.js'

export default {
	data() {
		return {
			paper: null
		}
	},

	computed: {
		authorText() {
			if (!this.paper || !this.paper.authors) return ''
			return this.paper.authors.join(', ')
		}
	},

	onLoad(options) {
		const id = decodeURIComponent(options.id || '')
		if (id) {
			this.loadPaper(id)
		}
	},

	methods: {
		/**
		 * 加载论文详情
		 */
		async loadPaper(id) {
			try {
				const res = await getPaper(id)
				if (res.code === 200 && res.data) {
					this.paper = res.data
				} else {
					uni.showToast({ title: res.msg || '加载失败', icon: 'none' })
				}
			} catch (e) {
				uni.showToast({ title: '加载失败', icon: 'none' })
			}
		},

		/**
		 * 打开 arXiv 链接
		 */
		openArxiv() {
			if (!this.paper || !this.paper.url) return
			uni.setClipboardData({
				data: this.paper.url,
				success: () => {
					uni.showToast({ title: '链接已复制', icon: 'success' })
				}
			})
		},

		/**
		 * 打开 PDF
		 */
		openPdf() {
			if (!this.paper || !this.paper.pdf_url) return
			uni.setClipboardData({
				data: this.paper.pdf_url,
				success: () => {
					uni.showToast({ title: 'PDF 链接已复制', icon: 'none' })
				}
			})
		},

		/**
		 * 复制摘要
		 */
		copySummary() {
			if (!this.paper) return
			const text = `What: ${this.paper.summary_what}\n\nHow: ${this.paper.summary_how}\n\nWhy: ${this.paper.summary_why}`
			uni.setClipboardData({
				data: text,
				success: () => {
					uni.showToast({ title: '摘要已复制', icon: 'success' })
				}
			})
		}
	}
}
</script>

<style lang="scss">
.container {
	min-height: 100vh;
	background-color: #0d1117;
	padding: 32rpx;
}

/* 标题 */
.title {
	color: #e6edf3;
	font-size: 32rpx;
	font-weight: 600;
	line-height: 1.4;
	margin-bottom: 16rpx;
}

/* 作者 */
.authors {
	color: #8b949e;
	font-size: 24rpx;
	margin-bottom: 24rpx;
}

/* 分类标签 */
.tags {
	margin-bottom: 32rpx;
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

/* 操作按钮 */
.action-btns {
	display: flex;
	gap: 24rpx;
	margin-bottom: 48rpx;
}

.btn-primary {
	flex: 1;
	background-color: #58a6ff;
	color: #0d1117;
	font-weight: 600;
	border-radius: 16rpx;
	font-size: 28rpx;
}

.btn-secondary {
	flex: 1;
	background-color: #21262d;
	color: #e6edf3;
	border-radius: 16rpx;
	font-size: 28rpx;
}

.btn-ghost {
	background-color: transparent;
	color: #8b949e;
	border: 1px solid #30363d;
	border-radius: 16rpx;
	font-size: 28rpx;
	margin-top: 24rpx;
}

/* 摘要区域 */
.summary-section {
	background-color: #161b22;
	border-radius: 24rpx;
	padding: 32rpx;
	margin-bottom: 32rpx;
}

.section-title {
	color: #e6edf3;
	font-size: 28rpx;
	font-weight: 600;
	margin-bottom: 24rpx;
}

.summary-item {
	margin-bottom: 24rpx;
}

.summary-label {
	color: #58a6ff;
	font-size: 24rpx;
	font-weight: 500;
	margin-bottom: 12rpx;
}

.summary-text {
	color: #c9d1d9;
	font-size: 28rpx;
	line-height: 1.6;
}

.disclaimer {
	color: #8b949e;
	font-size: 22rpx;
	margin-top: 24rpx;
	padding-top: 24rpx;
	border-top: 1px solid #30363d;
}

/* 原文摘要 */
.abstract-section {
	background-color: #161b22;
	border-radius: 24rpx;
	padding: 32rpx;
}

.abstract-text {
	color: #c9d1d9;
	font-size: 28rpx;
	line-height: 1.6;
}

/* 空状态 */
.empty {
	color: #8b949e;
	font-size: 28rpx;
	text-align: center;
	padding: 48rpx 0;
}
</style>