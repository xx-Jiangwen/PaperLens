<template>
	<view class="ai-summary">
		<!-- 标题栏 -->
		<view class="summary-header" @tap="toggleExpand">
			<view class="header-left">
				<text class="header-icon">✨</text>
				<text class="header-title">AI 结构化摘要</text>
			</view>
			<text class="header-toggle">{{ expanded ? '收起' : '展开' }}</text>
		</view>

		<!-- 内容区 -->
		<view v-show="expanded" class="summary-content">
			<!-- 处理中状态 -->
			<view v-if="status === 'processing'" class="processing">
				<view class="processing-animation">
					<view class="dot"></view>
					<view class="dot"></view>
					<view class="dot"></view>
				</view>
				<text class="processing-text">AI 正在生成摘要...</text>
			</view>

			<!-- 失败状态 -->
			<view v-else-if="status === 'failed'" class="failed">
				<text class="failed-text">摘要生成失败</text>
				<view class="retry-btn" @tap="onRetry">重试</view>
			</view>

			<!-- 待处理状态 -->
			<view v-else-if="status === 'pending'" class="pending">
				<text class="pending-text">暂无摘要，点击生成</text>
				<view class="generate-btn" @tap="onRetry">生成摘要</view>
			</view>

			<!-- 完成状态 -->
			<view v-else-if="status === 'done' && summary" class="sections">
				<view class="section">
					<view class="section-label">What · 问题与方案</view>
					<view class="section-text">{{ summary.what }}</view>
				</view>
				<view class="section">
					<view class="section-label">How · 技术路径</view>
					<view class="section-text">{{ summary.how }}</view>
				</view>
				<view class="section">
					<view class="section-label">Why · 贡献与意义</view>
					<view class="section-text">{{ summary.why }}</view>
				</view>
				<view class="disclaimer">内容由 AI 生成，请以原文为准</view>
			</view>
		</view>
	</view>
</template>

<script>
/**
 * AISummary - AI 摘要面板组件
 * @description 可折叠的 AI 结构化摘要展示面板
 */

export default {
	name: 'AISummary',

	props: {
		/**
		 * 摘要内容
		 */
		summary: {
			type: Object,
			default: null
		},
		/**
		 * 状态：pending | processing | done | failed
		 */
		status: {
			type: String,
			default: 'pending'
		},
		/**
		 * 是否展开
		 */
		expanded: {
			type: Boolean,
			default: true
		}
	},

	methods: {
		toggleExpand() {
			this.$emit('toggle', !this.expanded)
		},

		onRetry() {
			this.$emit('retry')
		}
	}
}
</script>

<style lang="scss" scoped>
.ai-summary {
	background-color: #ffffff;
	border-radius: 12px;
	overflow: hidden;
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
}

.summary-header {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding: 16px;
}

.header-left {
	display: flex;
	flex-direction: row;
	align-items: center;
}

.header-icon {
	font-size: 16px;
	margin-right: 8px;
}

.header-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	font-weight: 600;
	color: #1a1c1d;
}

.header-toggle {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	color: #0066cc;
}

.summary-content {
	padding: 0 16px 16px;
}

.processing {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 24px;
}

.processing-animation {
	display: flex;
	flex-direction: row;
	margin-bottom: 12px;
}

.dot {
	width: 8px;
	height: 8px;
	border-radius: 50%;
	background-color: #0066cc;
	margin: 0 4px;
	animation: bounce 1.4s infinite ease-in-out;
}

.dot:nth-child(1) {
	animation-delay: 0s;
}

.dot:nth-child(2) {
	animation-delay: 0.2s;
}

.dot:nth-child(3) {
	animation-delay: 0.4s;
}

@keyframes bounce {
	0%, 80%, 100% {
		transform: scale(0.6);
		opacity: 0.5;
	}
	40% {
		transform: scale(1);
		opacity: 1;
	}
}

.processing-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	color: #414753;
}

.failed,
.pending {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 16px;
}

.failed-text,
.pending-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	color: #727784;
	margin-bottom: 12px;
}

.retry-btn,
.generate-btn {
	padding: 8px 16px;
	background-color: #d7e3ff;
	color: #0066cc;
	border-radius: 8px;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 13px;
	font-weight: 500;
}

.section {
	margin-bottom: 16px;
}

.section:last-of-type {
	margin-bottom: 0;
}

.section-label {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 13px;
	font-weight: 600;
	color: #0066cc;
	margin-bottom: 8px;
}

.section-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 15px;
	color: #414753;
	line-height: 1.6;
}

.disclaimer {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 11px;
	color: #727784;
	margin-top: 16px;
	padding-top: 12px;
	border-top: 1px solid rgba(193, 198, 213, 0.15);
}
</style>