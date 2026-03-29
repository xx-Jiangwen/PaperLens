<template>
	<view class="page">
		<!-- 标题 -->
		<view class="header">
			<view class="title">选择你感兴趣的方向</view>
			<view class="subtitle">我们将为你推荐相关领域的论文</view>
		</view>

		<!-- 分类选择 -->
		<view class="category-section">
			<view class="category-grid">
				<view
					v-for="cat in categories"
					:key="cat.value"
					:class="['category-card', { active: selected.includes(cat.value) }]"
					:data-value="cat.value"
					@tap="toggleCategory"
				>
					<text class="category-icon">{{ cat.icon }}</text>
					<text class="category-name">{{ cat.label }}</text>
				</view>
			</view>
		</view>

		<!-- 提示 -->
		<view class="hint">
			已选择 {{ selected.length }}/5 个方向
		</view>

		<!-- 开始按钮 -->
		<view class="action-section">
			<button
				class="btn-start"
				:disabled="selected.length === 0"
				@tap="onStart"
			>开始使用</button>
		</view>
	</view>
</template>

<script>
import { useSettingsStore } from '@/stores/settings.js'

export default {
	setup() {
		const settingsStore = useSettingsStore()
		return { settingsStore }
	},

	data() {
		return {
			selected: [],
			categories: [
				{ value: 'cs.AI', label: '人工智能', icon: '🤖' },
				{ value: 'cs.CL', label: '自然语言', icon: '💬' },
				{ value: 'cs.CV', label: '计算机视觉', icon: '👁️' },
				{ value: 'cs.LG', label: '机器学习', icon: '📊' },
				{ value: 'stat.ML', label: '统计学习', icon: '📈' },
				{ value: 'cs.RO', label: '机器人', icon: '🦾' },
				{ value: 'cs.NE', label: '神经网络', icon: '🧠' },
				{ value: 'cs.SE', label: '软件工程', icon: '💻' }
			]
		}
	},

	methods: {
		toggleCategory(e) {
			const value = e.currentTarget.dataset.value
			const index = this.selected.indexOf(value)
			if (index > -1) {
				this.selected.splice(index, 1)
			} else if (this.selected.length < 5) {
				this.selected.push(value)
			} else {
				uni.showToast({ title: '最多选择 5 个', icon: 'none' })
			}
		},

		async onStart() {
			if (this.selected.length === 0) {
				uni.showToast({ title: '请至少选择一个方向', icon: 'none' })
				return
			}

			// 保存兴趣设置
			await this.settingsStore.saveSettings({
				preferred_categories: this.selected
			})

			// 标记不是新用户了
			uni.removeStorageSync('is_new_user')

			// 跳转首页
			uni.switchTab({
				url: '/pages/home/index'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.page {
	min-height: 100vh;
	background-color: $color-bg;
	display: flex;
	flex-direction: column;
}

.header {
	padding: $spacing-6 $spacing-4 $spacing-4;
}

.title {
	font-size: $font-size-title1;
	font-weight: $font-weight-bold;
	color: $color-text-primary;
	margin-bottom: $spacing-2;
}

.subtitle {
	font-size: $font-size-body;
	color: $color-text-secondary;
}

.category-section {
	flex: 1;
	padding: 0 $spacing-4;
}

.category-grid {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	margin: 0 -$spacing-2;
}

.category-card {
	width: calc(50% - $spacing-4);
	margin: $spacing-2;
	padding: $spacing-4;
	background-color: $color-bg-grouped;
	border-radius: $radius-md;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 160rpx;
	border: 4rpx solid transparent;
	transition: all $duration-fast;
}

.category-card.active {
	background-color: $color-primary-light;
	border-color: $color-primary;
}

.category-icon {
	font-size: 48rpx;
	margin-bottom: $spacing-2;
}

.category-name {
	font-size: $font-size-subheadline;
	font-weight: $font-weight-medium;
	color: $color-text-primary;
}

.hint {
	text-align: center;
	font-size: $font-size-footnote;
	color: $color-text-tertiary;
	padding: $spacing-4;
}

.action-section {
	padding: $spacing-4;
	padding-bottom: calc($spacing-4 + env(safe-area-inset-bottom));
}

.btn-start {
	height: 96rpx;
	background-color: $color-primary;
	border-radius: $radius-md;
	font-size: $font-size-body;
	font-weight: $font-weight-semibold;
	color: #FFFFFF;
}

.btn-start[disabled] {
	background-color: $color-bg-grouped;
	color: $color-text-tertiary;
}
</style>