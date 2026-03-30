<template>
	<view class="page">
		<!-- 昵称 -->
		<view class="section" v-if="isLoggedIn">
			<view class="section-title">昵称</view>
			<input
				class="nickname-input"
				v-model="nickname"
				placeholder="输入昵称"
				maxlength="20"
			/>
		</view>

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

		<!-- 退出登录 -->
		<view class="logout-section" v-if="isLoggedIn">
			<button class="btn-logout" @tap="logout">退出登录</button>
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
import { getUserInfo, updateUserInfo } from '@/api/user.js'

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
			nickname: '',
			isLoggedIn: false
		}
	},

	onLoad() {
		this.isLoggedIn = userStore.isLoggedIn()
		this.loadSettings()
	},

	methods: {
		async loadSettings() {
			if (!userStore.isLoggedIn()) return
			await this.settingsStore.fetchSettings()
			this.selectedCategories = [...this.settingsStore.categories]
			this.dailyCount = this.settingsStore.dailyCount
			// 加载昵称
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

		logout() {
			uni.showModal({
				title: '确认退出',
				content: '退出登录后需要重新登录才能使用完整功能',
				confirmText: '退出',
				confirmColor: '#FF3B30',
				success: (res) => {
					if (res.confirm) {
						userStore.clear()
						this.isLoggedIn = false
						uni.reLaunch({ url: '/pages/home/index' })
					}
				}
			})
		},

		async save() {
			if (!userStore.isLoggedIn()) {
				const success = await userStore.performWxLogin()
				if (!success) {
					uni.showToast({ title: '登录失败', icon: 'none' })
					return
				}
			}

			// 保存昵称
			const trimmed = this.nickname.trim()
			if (trimmed) {
				const userRes = await updateUserInfo({ nickname: trimmed })
				if (userRes.code !== 200) {
					uni.showToast({ title: userRes.msg || '昵称保存失败', icon: 'none' })
					return
				}
			}

			// 保存偏好设置
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
	margin-bottom: $spacing-3;
}

.nickname-input {
	height: 80rpx;
	background-color: $color-bg-grouped;
	border-radius: $radius-sm;
	padding: 0 $spacing-4;
	font-size: $font-size-body;
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

.logout-section {
	margin: $spacing-6 $spacing-4 $spacing-4;
}

.btn-logout {
	background-color: $color-bg-card;
	color: $color-error;
	font-weight: $font-weight-semibold;
	border-radius: $radius-sm;
	font-size: $font-size-body;
	border: none;
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