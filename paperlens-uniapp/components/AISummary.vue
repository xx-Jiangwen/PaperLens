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
@import '@/styles/variables.scss';

.ai-summary {
	background-color: $color-bg-card;
	border-radius: $radius-md;
	overflow: hidden;
}

.summary-header {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding: $spacing-4;
}

.header-left {
	display: flex;
	flex-direction: row;
	align-items: center;
}

.header-icon {
	font-size: 32rpx;
	margin-right: $spacing-2;
}

.header-title {
	font-size: $font-size-headline;
	font-weight: $font-weight-semibold;
	color: $color-text-primary;
}

.header-toggle {
	font-size: $font-size-subheadline;
	color: $color-primary;
}

.summary-content {
	padding: 0 $spacing-4 $spacing-4;
}

.processing {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: $spacing-6;
}

.processing-animation {
	display: flex;
	flex-direction: row;
	margin-bottom: $spacing-3;
}

.dot {
	width: 16rpx;
	height: 16rpx;
	border-radius: 50%;
	background-color: $color-primary;
	margin: 0 $spacing-1;
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
	font-size: $font-size-subheadline;
	color: $color-text-secondary;
}

.failed,
.pending {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: $spacing-4;
}

.failed-text,
.pending-text {
	font-size: $font-size-subheadline;
	color: $color-text-tertiary;
	margin-bottom: $spacing-3;
}

.retry-btn,
.generate-btn {
	padding: $spacing-2 $spacing-4;
	background-color: $color-primary-light;
	color: $color-primary;
	border-radius: $radius-sm;
	font-size: $font-size-footnote;
	font-weight: $font-weight-medium;
}

.section {
	margin-bottom: $spacing-4;
}

.section:last-of-type {
	margin-bottom: 0;
}

.section-label {
	font-size: $font-size-footnote;
	font-weight: $font-weight-semibold;
	color: $color-primary;
	margin-bottom: $spacing-2;
}

.section-text {
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
</style>