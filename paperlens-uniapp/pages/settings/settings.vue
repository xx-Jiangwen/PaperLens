<template>
	<view class="container">
		<view class="section">
			<view class="section-title">大模型配置（BYOK）</view>
			<view class="hint">支持 OpenAI、DeepSeek、本地 Ollama 等兼容 OpenAI 协议的模型</view>

			<!-- API Base URL -->
			<view class="field">
				<view class="label">API Base URL</view>
				<input
					class="input"
					v-model="form.llm_base_url"
					placeholder="https://api.openai.com/v1"
				/>
			</view>

			<!-- Model Name -->
			<view class="field">
				<view class="label">模型名称</view>
				<input
					class="input"
					v-model="form.llm_model_name"
					placeholder="gpt-4o-mini"
				/>
			</view>

			<!-- API Key -->
			<view class="field">
				<view class="label">API Key</view>
				<input
					class="input"
					type="password"
					v-model="form.llm_api_key"
					:placeholder="apiKeySet ? '已设置（留空不修改）' : '输入 API Key'"
				/>
			</view>

			<button
				class="btn-ghost"
				:loading="testing"
				@tap="testLLM"
			>测试连通性</button>
		</view>

		<button class="btn-primary save-btn" @tap="save">保存设置</button>
	</view>
</template>

<script>
import { getSettings, updateSettings, testLLM as testLLMApi } from '../../api/settings.js'
import userStore from '../../stores/user.js'

export default {
	data() {
		return {
			form: {
				llm_base_url: '',
				llm_model_name: '',
				llm_api_key: '',
				language: 'zh'
			},
			apiKeySet: false,
			testing: false
		}
	},

	onLoad() {
		userStore.init()
		this.loadSettings()
	},

	methods: {
		/**
		 * 加载设置
		 */
		async loadSettings() {
			try {
				const res = await getSettings()
				if (res.code === 200 && res.data) {
					this.form.llm_base_url = res.data.llm_base_url || ''
					this.form.llm_model_name = res.data.llm_model_name || ''
					this.form.language = res.data.language || 'zh'
					this.apiKeySet = res.data.llm_api_key_set || false
				}
			} catch (e) {
				// 未登录时静默处理
			}
		},

		/**
		 * 测试 LLM 连通性
		 */
		async testLLM() {
			// 确保已登录
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
					title: res.msg || (res.code === 200 ? '连接成功' : '连接失败'),
					icon: res.code === 200 ? 'success' : 'none'
				})
			} catch (e) {
				uni.showToast({ title: '测试失败', icon: 'none' })
			} finally {
				this.testing = false
			}
		},

		/**
		 * 保存设置
		 */
		async save() {
			// 确保已登录
			if (!userStore.isLoggedIn()) {
				const success = await userStore.performWxLogin()
				if (!success) {
					uni.showToast({ title: '登录失败', icon: 'none' })
					return
				}
			}

			const payload = {
				llm_base_url: this.form.llm_base_url,
				llm_model_name: this.form.llm_model_name,
				language: this.form.language
			}

			// 只有填写了 API Key 才发送
			if (this.form.llm_api_key) {
				payload.llm_api_key = this.form.llm_api_key
			}

			try {
				const res = await updateSettings(payload)
				if (res.code === 200) {
					uni.showToast({ title: '保存成功', icon: 'success' })
					if (this.form.llm_api_key) {
						this.apiKeySet = true
					}
				} else {
					uni.showToast({ title: res.msg || '保存失败', icon: 'none' })
				}
			} catch (e) {
				uni.showToast({ title: '保存失败', icon: 'none' })
			}
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

.section {
	background-color: #161b22;
	border-radius: 24rpx;
	padding: 32rpx;
	margin-bottom: 32rpx;
}

.section-title {
	color: #e6edf3;
	font-size: 28rpx;
	font-weight: 600;
	margin-bottom: 16rpx;
}

.hint {
	color: #8b949e;
	font-size: 24rpx;
	margin-bottom: 32rpx;
}

.field {
	margin-bottom: 28rpx;
}

.label {
	color: #8b949e;
	font-size: 24rpx;
	margin-bottom: 12rpx;
}

.input {
	background-color: #0d1117;
	color: #e6edf3;
	border: 1px solid #30363d;
	border-radius: 16rpx;
	padding: 20rpx 24rpx;
	font-size: 28rpx;
}

.btn-ghost {
	background-color: transparent;
	color: #8b949e;
	border: 1px solid #30363d;
	border-radius: 16rpx;
	font-size: 28rpx;
	margin-top: 16rpx;
}

.save-btn {
	background-color: #58a6ff;
	color: #0d1117;
	font-weight: 600;
	border-radius: 16rpx;
	font-size: 28rpx;
}
</style>