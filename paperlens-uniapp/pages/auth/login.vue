<template>
	<view class="page">
		<!-- Logo -->
		<view class="logo-section">
			<image class="logo" src="/static/logo.png" mode="aspectFit" />
			<view class="app-name">PaperLens</view>
			<view class="slogan">让论文阅读更高效</view>
		</view>

		<!-- 登录按钮 -->
		<view class="login-section">
			<button class="btn-login" :loading="loading" @tap="onLogin">
				<text class="btn-icon">💬</text>
				<text class="btn-text">微信一键登录</text>
			</button>

			<view class="terms">
				登录即表示同意
				<text class="link">《用户协议》</text>
				和
				<text class="link">《隐私政策》</text>
			</view>
		</view>
	</view>
</template>

<script>
import userStore from '@/stores/user.js'

export default {
	data() {
		return {
			loading: false
		}
	},

	methods: {
		async onLogin() {
			this.loading = true
			try {
				const success = await userStore.performWxLogin()
				if (success) {
					// 检查是否是新用户，需要引导
					const isNew = uni.getStorageSync('is_new_user')
					if (isNew) {
						uni.redirectTo({
							url: '/pages/auth/onboarding'
						})
					} else {
						uni.switchTab({
							url: '/pages/home/index'
						})
					}
				} else {
					uni.showToast({ title: '登录失败', icon: 'none' })
				}
			} catch (e) {
				uni.showToast({ title: '登录失败', icon: 'none' })
			} finally {
				this.loading = false
			}
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

.logo-section {
	flex: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
}

.logo {
	width: 160rpx;
	height: 160rpx;
	margin-bottom: $spacing-4;
}

.app-name {
	font-size: $font-size-title1;
	font-weight: $font-weight-bold;
	color: $color-text-primary;
	margin-bottom: $spacing-2;
}

.slogan {
	font-size: $font-size-subheadline;
	color: $color-text-secondary;
}

.login-section {
	padding: $spacing-6 $spacing-4;
	padding-bottom: calc($spacing-6 + env(safe-area-inset-bottom));
}

.btn-login {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
	height: 96rpx;
	background-color: #07C160;
	border-radius: $radius-md;
}

.btn-icon {
	font-size: 40rpx;
	margin-right: $spacing-2;
}

.btn-text {
	font-size: $font-size-body;
	font-weight: $font-weight-semibold;
	color: #FFFFFF;
}

.terms {
	text-align: center;
	font-size: $font-size-caption;
	color: $color-text-tertiary;
	margin-top: $spacing-4;
}

.link {
	color: $color-primary;
}
</style>