<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header" :style="{ paddingTop: navBarTop + 'px' }">
			<view class="header-inner" :style="{ height: navBarHeight + 'px' }">
				<view class="header-left">
					<view class="icon-btn" @tap="goBack">
						<MdIcon name="arrow-back" size="48" color="#71717a" />
					</view>
				</view>
				<text class="page-title">偏好设置</text>
				<view class="header-right"></view>
			</view>
		</view>

		<!-- 主内容区 -->
		<scroll-view class="main-content" :style="{ paddingTop: contentTop + 'px' }" scroll-y="true">
			<!-- Hero 区域 -->
			<view class="hero-section">
				<text class="hero-title">定制您的阅读体验</text>
				<text class="hero-desc">调整研究算法，让我们为您筛选最相关的学术动态。</text>
			</view>

			<!-- 研究方向 -->
			<view class="section">
				<text class="section-label">研究方向</text>
				<view class="category-card">
					<view class="category-list">
						<view
							v-for="cat in allCategories"
							:key="cat.value"
							:class="['category-chip', { active: selectedCategories.includes(cat.value) }]"
							:data-value="cat.value"
							@tap="toggleCategory"
						>{{ cat.label }}</view>
						<!-- 添加按钮 -->
						<view class="add-chip">
							<MdIcon name="add" size="28" color="#c1c6d5" />
						</view>
					</view>
					<text class="section-hint">选择您的核心研究领域，PaperLens 将优先为您推荐相关领域的顶级期刊论文。</text>
				</view>
			</view>

			<!-- 每日推送数量 -->
			<view class="section">
				<text class="section-label">每日推送数量</text>
				<view class="count-card">
					<view class="count-header">
						<view class="count-info">
							<text class="count-value">{{ dailyCount }} 篇/日</text>
							<text class="count-desc">{{ countModeText }}</text>
						</view>
						<MdIcon name="auto-awesome" size="48" color="#c1c6d5" />
					</view>
					<!-- 滑块 -->
					<view class="slider-container">
						<view class="slider-track">
							<view class="slider-fill" :style="{ width: sliderPercent + '%' }"></view>
							<view class="slider-thumb" :style="{ left: sliderPercent + '%' }"></view>
						</view>
						<view class="slider-labels">
							<text class="slider-label">1 篇</text>
							<text class="slider-label">10 篇</text>
						</view>
					</view>
					<!-- 隐藏的原生滑块 -->
					<slider
						class="hidden-slider"
						:min="1"
						:max="10"
						:value="dailyCount"
						:block-size="1"
						backgroundColor="transparent"
						activeColor="transparent"
						@changing="onSliderChange"
						@change="onSliderChange"
					/>
				</view>
			</view>

			<!-- 保存按钮 -->
			<view class="save-section">
				<view class="save-btn" @tap="save">
					<text class="save-text">保存我的偏好</text>
				</view>
				<text class="save-hint">您的更改将立即同步至所有已登录设备。</text>
			</view>
		</scroll-view>

		<!-- 底部导航 - 仅图标 -->
		<view class="bottom-nav">
			<view class="nav-item" @tap="switchTab('/pages/home/index')">
				<MdIcon name="home" size="52" color="#a1a1aa" />
			</view>
			<view class="nav-item active">
				<MdIcon name="person" size="52" color="#3b82f6" filled />
			</view>
		</view>
	</view>
</template>

<script>
import userStore from '@/stores/user.js'
import { useSettingsStore } from '@/stores/settings.js'
import { getUserInfo, updateUserInfo } from '@/api/user.js'
import MdIcon from '@/components/MdIcon.vue'

export default {
	components: {
		MdIcon
	},

	setup() {
		const settingsStore = useSettingsStore()
		return { settingsStore }
	},

	data() {
		return {
			navBarTop: 20,
			navBarHeight: 56,
			contentTop: 120,
			allCategories: [
				{ value: 'cs.CL', label: 'NLP' },
				{ value: 'cs.CV', label: 'CV' },
				{ value: 'cs.LG', label: 'ML' },
				{ value: 'cs.AI', label: 'AI' },
				{ value: 'stat.ML', label: 'Stat' },
				{ value: 'cs.RO', label: 'Robotics' },
				{ value: 'cs.NE', label: 'Neural' },
				{ value: 'cs.SE', label: 'SE' }
			],
			selectedCategories: [],
			dailyCount: 5,
			nickname: '',
			isLoggedIn: false
		}
	},

	computed: {
		countModeText() {
			if (this.dailyCount <= 3) return '推荐频率：精选模式'
			if (this.dailyCount <= 6) return '推荐频率：深度阅读模式'
			return '推荐频率：广泛浏览模式'
		},
		sliderPercent() {
			return ((this.dailyCount - 1) / 9) * 100
		}
	},

	onLoad() {
		// 获取胶囊按钮位置
		try {
			const menuRect = uni.getMenuButtonBoundingClientRect()
			if (menuRect) {
				this.navBarTop = menuRect.bottom + 8
				this.navBarHeight = menuRect.height
				this.contentTop = menuRect.bottom + 8 + this.navBarHeight + 16
			}
		} catch (e) {
			const systemInfo = uni.getSystemInfoSync()
			this.navBarTop = (systemInfo.statusBarHeight || 20) + 44
			this.contentTop = this.navBarTop + 56 + 16
		}

		this.isLoggedIn = userStore.isLoggedIn()
		this.loadSettings()
	},

	methods: {
		async loadSettings() {
			if (!userStore.isLoggedIn()) return
			await this.settingsStore.fetchSettings()
			this.selectedCategories = [...this.settingsStore.categories]
			this.dailyCount = this.settingsStore.dailyCount || 5
			try {
				const res = await getUserInfo()
				if (res.code === 200 && res.data) {
					this.nickname = res.data.nickname || ''
				}
			} catch (e) {
				console.error('加载用户信息失败', e)
			}
		},

		toggleCategory(e) {
			const value = e.currentTarget.dataset.value
			const index = this.selectedCategories.indexOf(value)
			if (index > -1) {
				this.selectedCategories.splice(index, 1)
			} else if (this.selectedCategories.length < 5) {
				this.selectedCategories.push(value)
			} else {
				uni.showToast({ title: '最多选择 5 个', icon: 'none' })
			}
		},

		onSliderChange(e) {
			this.dailyCount = e.detail.value
		},

		goBack() {
			uni.navigateBack()
		},

		switchTab(url) {
			uni.switchTab({ url })
		},

		async save() {
			if (!userStore.isLoggedIn()) {
				const success = await userStore.performWxLogin()
				if (!success) {
					uni.showToast({ title: '登录失败', icon: 'none' })
					return
				}
			}

			const trimmed = this.nickname.trim()
			if (trimmed) {
				await updateUserInfo({ nickname: trimmed })
			}

			const payload = {
				preferred_categories: this.selectedCategories,
				daily_count: this.dailyCount
			}

			const res = await this.settingsStore.saveSettings(payload)
			if (res.code === 200) {
				uni.showToast({ title: '保存成功', icon: 'success' })
			} else {
				uni.showToast({ title: res.msg || '保存失败', icon: 'none' })
			}
		}
	}
}
</script>

<style lang="scss" scoped>
/* ========== 页面基础 ========== */

.page {
	min-height: 100vh;
	background-color: #F5F5F7;
	display: flex;
	flex-direction: column;
}

/* ========== 顶部导航栏 ========== */

.header {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	z-index: 100;
	background-color: rgba(255, 255, 255, 0.85);
	border-bottom: 1px solid rgba(0, 0, 0, 0.04);
	/* 安全区域适配 */
	padding-top: constant(safe-area-inset-top);
	padding-top: env(safe-area-inset-top);
}

.header-inner {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	height: 56px;
	padding: 12px 16px 8px;
	max-width: 600px;
	margin: 0 auto;
}

.header-left,
.header-right {
	width: 48px;
	display: flex;
	align-items: center;
}

.icon-btn {
	padding: 8px;
}

.page-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 18px;
	font-weight: 700;
	color: #18181b;
	text-align: center;
	flex: 1;
}

/* ========== 主内容区 ========== */

.main-content {
	flex: 1;
	padding: 120px 16px 100px;
	max-width: 600px;
	margin: 0 auto;
	width: 100%;
	box-sizing: border-box;
}

/* ========== Hero 区域 ========== */

.hero-section {
	margin-bottom: 32px;
}

.hero-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 28px;
	font-weight: 800;
	color: #1a1c1d;
	letter-spacing: -0.02em;
	margin-bottom: 8px;
}

.hero-desc {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	color: #414753;
	line-height: 1.5;
}

/* ========== Section ========== */

.section {
	margin-bottom: 32px;
	width: 100%;
	box-sizing: border-box;
}

.section-label {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 12px;
	font-weight: 700;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: #414753;
	margin-bottom: 16px;
	padding-left: 4px;
}

.section-hint {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 11px;
	font-style: italic;
	color: #414753;
	margin-top: 16px;
}

/* ========== 研究方向卡片 ========== */

.category-card {
	background-color: #ffffff;
	border-radius: 12px;
	padding: 20px;
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
	width: 100%;
	box-sizing: border-box;
}

.category-list {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	gap: 8px;
}

.category-chip {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 32px;
	padding: 0 16px;
	background-color: #e8e8ea;
	color: #414753;
	border-radius: 999px;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 500;
	transition: all 0.2s ease;
}

.category-chip.active {
	background-color: #0066cc;
	color: #ffffff;
}

.category-chip:active {
	transform: scale(0.95);
}

.add-chip {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 36px;
	height: 36px;
	border: 2px dashed #c1c6d5;
	border-radius: 999px;
}

/* ========== 每日推送数量卡片 ========== */

.count-card {
	background-color: #ffffff;
	border-radius: 12px;
	padding: 20px;
	position: relative;
	box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
	width: 100%;
	box-sizing: border-box;
}

.count-header {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: flex-end;
	margin-bottom: 24px;
}

.count-info {
	display: flex;
	flex-direction: column;
	gap: 4px;
}

.count-value {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 24px;
	font-weight: 700;
	color: #0066cc;
	letter-spacing: -0.02em;
}

.count-desc {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 12px;
	color: #414753;
}

/* ========== 自定义滑块 ========== */

.slider-container {
	position: relative;
}

.slider-track {
	position: relative;
	height: 12px;
	display: flex;
	align-items: center;
}

.slider-track::before {
	content: '';
	position: absolute;
	left: 0;
	right: 0;
	height: 6px;
	background-color: #e8e8ea;
	border-radius: 6px;
}

.slider-fill {
	position: absolute;
	left: 0;
	height: 6px;
	background-color: #0066cc;
	border-radius: 6px;
}

.slider-thumb {
	position: absolute;
	width: 24px;
	height: 24px;
	background-color: #ffffff;
	border: 2px solid #0066cc;
	border-radius: 50%;
	transform: translateX(-50%);
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.slider-labels {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	margin-top: 8px;
}

.slider-label {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 10px;
	font-weight: 700;
	color: rgba(65, 71, 83, 0.5);
	letter-spacing: -0.02em;
}

.hidden-slider {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	opacity: 0;
	height: 50px;
}

/* ========== 保存按钮 ========== */

.save-section {
	padding-top: 40px;
	padding-bottom: 48px;
	width: 100%;
	box-sizing: border-box;
}

.save-btn {
	background-color: #0066cc;
	border-radius: 12px;
	padding: 16px;
	text-align: center;
	box-shadow: 0 8px 30px rgba(0, 102, 204, 0.16);
}

.save-btn:active {
	transform: scale(0.98);
}

.save-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 16px;
	font-weight: 700;
	color: #ffffff;
}

.save-hint {
	display: block;
	text-align: center;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 11px;
	color: rgba(65, 71, 83, 0.6);
	margin-top: 16px;
	line-height: 1.5;
}

/* ========== 底部导航 - 仅图标 ========== */

.bottom-nav {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	gap: 64px;
	padding: 16px 16px 32px;
	background-color: rgba(255, 255, 255, 0.85);
	border-top: 1px solid rgba(0, 0, 0, 0.04);
	padding-bottom: calc(16px + constant(safe-area-inset-bottom));
	padding-bottom: calc(16px + env(safe-area-inset-bottom));
}

.nav-item {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 56px;
	height: 56px;
	border-radius: 50%;
	transition: all 0.2s ease;
}

.nav-item:active {
	transform: scale(0.9);
}

.nav-item.active {
	background-color: rgba(59, 130, 246, 0.1);
}
</style>