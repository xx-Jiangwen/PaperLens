<template>
	<view class="page">
		<!-- 兴趣方向 -->
		<view class="section">
			<view class="section-title">兴趣方向</view>
			<view class="section-hint">选择 1-5 个感兴趣的领域</view>
			<view class="category-grid">
				<view
					v-for="cat in allCategories"
					:key="cat"
					:class="['category-item', { active: selectedCategories.includes(cat) }]"
					:data-cat="cat"
					@tap="toggleCategory"
				>{{ cat }}</view>
			</view>
		</view>

		<!-- 每日推送数量 -->
		<view class="section">
			<view class="section-title">每日推送数量</view>
			<view class="count-selector">
				<view
					v-for="n in 10"
					:key="n"
					:class="['count-item', { active: dailyCount === n }]"
					:data-count="n"
					@tap="setDailyCount"
				>{{ n }}</view>
			</view>
		</view>

		<!-- BYOK 配置 -->
		<view class="section">
			<view class="section-title">大模型配置（BYOK）</view>
			<view class="section-hint">支持 OpenAI、DeepSeek、本地 Ollama 等</view>

			<view class="field">
				<view class="label">API Base URL</view>
				<input
					class="input"
					v-model="form.llm_base_url"
					placeholder="https://api.openai.com/v1"
				/>
			</view>

			<view class="field">
				<view class="label">模型名称</view>
				<input
					class="input"
					v-model="form.llm_model_name"
					placeholder="gpt-4o-mini"
				/>
			</view>

			<view class="field">
				<view class="label">API Key</view>
				<input
					class="input"
					type="password"
					v-model="form.llm_api_key"
					:placeholder="form.llm_api_key_set ? '已设置（留空不修改）' : '输入 API Key'"
				/>
			</view>

			<button class="btn-test" @tap="testLLM">测试连通性</button>
		</view>

		<!-- 保存按钮 -->
		<view class="save-section">
			<button class="btn-save" @tap="save">保存设置</button>
		</view>
	</view>
</template>

<script>
import userStore from '@/stores/user.js'
import { useSettingsStore } from '@/stores/settings.js'
import { testLLM as testLLMApi } from '@/api/settings.js'

export default {
	setup() {
		const settingsStore = useSettingsStore()
		return { settingsStore }
	},

	data() {
		return {
			allCategories: ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML', 'cs.RO', 'cs.NE', 'cs.SE'],
			selectedCategories: [],
			dailyCount: 5,
			form: {
				llm_base_url: '',
				llm_model_name: '',
				llm_api_key: '',
				llm_api_key_set: false
			},
			testing: false
		}
	},

	onLoad() {
		this.loadSettings()
	},

	methods: {
		async loadSettings() {
			if (!userStore.isLoggedIn()) return
			await this.settingsStore.fetchSettings()
			this.selectedCategories = [...this.settingsStore.categories]
			this.dailyCount = this.settingsStore.dailyCount
			this.form.llm_base_url = this.settingsStore.llmBaseUrl
			this.form.llm_model_name = this.settingsStore.llmModelName
			this.form.llm_api_key_set = this.settingsStore.llmApiKeySet
		},

		toggleCategory(e) {
			const cat = e.currentTarget.dataset.cat
			const index = this.selectedCategories.indexOf(cat)
			if (index > -1) {
				this.selectedCategories.splice(index, 1)
			} else if (this.selectedCategories.length < 5) {
				this.selectedCategories.push(cat)
			} else {
				uni.showToast({ title: '最多选择 5 个', icon: 'none' })
			}
		},

		setDailyCount(e) {
			this.dailyCount = e.currentTarget.dataset.count
		},

		async testLLM() {
			if (!userStore.isLoggedIn()) {
				const success = await userStore.performWxLogin()
				if (!success) {
					uni.showToast({ title: '登录失败', icon: 'none' })
					return
				}
			}

			this.testing = true
			try {
				const res = await testLLMApi()
				uni.showToast({
					title: res.code === 200 ? '连接成功' : '连接失败',
					icon: res.code === 200 ? 'success' : 'none'
				})
			} catch (e) {
				uni.showToast({ title: '测试失败', icon: 'none' })
			} finally {
				this.testing = false
			}
		},

		async save() {
			if (!userStore.isLoggedIn()) {
				const success = await userStore.performWxLogin()
				if (!success) {
					uni.showToast({ title: '登录失败', icon: 'none' })
					return
				}
			}

			const payload = {
				preferred_categories: this.selectedCategories,
				daily_count: this.dailyCount,
				llm_base_url: this.form.llm_base_url,
				llm_model_name: this.form.llm_model_name
			}

			if (this.form.llm_api_key) {
				payload.llm_api_key = this.form.llm_api_key
			}

			const res = await this.settingsStore.saveSettings(payload)
			if (res.code === 200) {
				uni.showToast({ title: '保存成功', icon: 'success' })
				if (this.form.llm_api_key) {
					this.form.llm_api_key_set = true
					this.form.llm_api_key = ''
				}
			} else {
				uni.showToast({ title: res.msg || '保存失败', icon: 'none' })
			}
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.page {
	min-height: 100vh;
	background-color: $color-bg-grouped;
	padding-bottom: 160rpx;
}

.section {
	background-color: $color-bg-card;
	margin: $spacing-4;
	border-radius: $radius-md;
	padding: $spacing-4;
}

.section-title {
	font-size: $font-size-headline;
	font-weight: $font-weight-semibold;
	color: $color-text-primary;
}

.section-hint {
	font-size: $font-size-footnote;
	color: $color-text-secondary;
	margin-top: $spacing-1;
	margin-bottom: $spacing-4;
}

.category-grid {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
}

.category-item {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 64rpx;
	padding: 0 $spacing-4;
	background-color: $color-bg-grouped;
	color: $color-text-secondary;
	border-radius: $radius-sm;
	font-size: $font-size-subheadline;
	margin-right: $spacing-2;
	margin-bottom: $spacing-2;
}

.category-item.active {
	background-color: $color-primary-light;
	color: $color-primary;
}

.count-selector {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
}

.count-item {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 56rpx;
	height: 56rpx;
	background-color: $color-bg-grouped;
	color: $color-text-secondary;
	border-radius: $radius-sm;
	font-size: $font-size-body;
	margin-right: $spacing-2;
	margin-bottom: $spacing-2;
}

.count-item.active {
	background-color: $color-primary;
	color: #FFFFFF;
}

.field {
	margin-bottom: $spacing-4;
}

.label {
	font-size: $font-size-footnote;
	color: $color-text-secondary;
	margin-bottom: $spacing-2;
}

.input {
	background-color: $color-bg-grouped;
	color: $color-text-primary;
	border-radius: $radius-sm;
	padding: $spacing-3 $spacing-4;
	font-size: $font-size-body;
}

.btn-test {
	background-color: transparent;
	color: $color-primary;
	border: 2rpx solid $color-separator;
	border-radius: $radius-sm;
	font-size: $font-size-body;
	margin-top: $spacing-2;
}

.save-section {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	padding: $spacing-4;
	background-color: $color-bg;
	padding-bottom: calc($spacing-4 + env(safe-area-inset-bottom));
}

.btn-save {
	background-color: $color-primary;
	color: #FFFFFF;
	font-weight: $font-weight-semibold;
	border-radius: $radius-sm;
	font-size: $font-size-body;
}
</style>