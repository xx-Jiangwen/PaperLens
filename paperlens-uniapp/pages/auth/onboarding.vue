<template>
	<view class="page">
		<!-- 标题 -->
		<view class="header">
			<view class="title">欢迎使用 PaperLens</view>
			<view class="subtitle">设置你的昵称和感兴趣的方向</view>
		</view>

		<!-- 昵称输入 -->
		<view class="nickname-section">
			<view class="section-label">你的昵称</view>
			<input
				class="nickname-input"
				v-model="nickname"
				placeholder="输入昵称（1-20个字符）"
				maxlength="20"
			/>
		</view>

		<!-- 分类选择 -->
		<view class="category-section">
			<view class="section-label">感兴趣的方向</view>
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
import { updateUserInfo } from '@/api/user.js'

export default {
	setup() {
		const settingsStore = useSettingsStore()
		return { settingsStore }
	},

	data() {
		return {
			nickname: '',
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

			// 保存昵称
			const trimmed = this.nickname.trim()
			if (trimmed) {
				await updateUserInfo({ nickname: trimmed })
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
.page {
	min-height: 100vh;
	background-color: #F5F5F7;
	display: flex;
	flex-direction: column;
}

.header {
	padding: 24px 16px 16px;
}

.title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 28px;
	font-weight: 700;
	color: #1a1c1d;
	margin-bottom: 8px;
}

.subtitle {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	color: #414753;
}

.category-section {
	flex: 1;
	padding: 0 16px;
}

.section-label {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	font-weight: 600;
	color: #1a1c1d;
	margin-bottom: 12px;
}

.nickname-section {
	padding: 0 16px 16px;
}

.nickname-input {
	height: 44px;
	background-color: #ffffff;
	border-radius: 8px;
	padding: 0 16px;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	color: #1a1c1d;
	border: 1px solid #e8e8ea;
}

.category-grid {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	margin: 0 -4px;
}

.category-card {
	width: calc(50% - 8px);
	margin: 4px;
	padding: 16px;
	background-color: #ffffff;
	border-radius: 12px;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 80px;
	border: 2px solid transparent;
	transition: all 0.15s ease;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.category-card.active {
	background-color: #d7e3ff;
	border-color: #0066cc;
}

.category-icon {
	font-size: 24px;
	margin-bottom: 8px;
}

.category-name {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 500;
	color: #1a1c1d;
}

.hint {
	text-align: center;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 13px;
	color: #727784;
	padding: 16px;
}

.action-section {
	padding: 16px;
	padding-bottom: calc(16px + env(safe-area-inset-bottom));
}

.btn-start {
	height: 48px;
	background-color: #0066cc;
	border-radius: 12px;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	font-weight: 600;
	color: #FFFFFF;
}

.btn-start[disabled] {
	background-color: #e8e8ea;
	color: #727784;
}
</style>