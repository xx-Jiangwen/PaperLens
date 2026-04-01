<template>
	<view class="tab-bar">
		<view
			:class="['tab-item', { active: currentPath === '/pages/home/index' }]"
			@tap="switchTab('/pages/home/index')"
		>
			<MdIcon
				name="home"
				size="44"
				:color="currentPath === '/pages/home/index' ? '#3b82f6' : '#71717a'"
				:filled="currentPath === '/pages/home/index'"
			/>
			<text class="tab-label">首页</text>
		</view>
		<view
			:class="['tab-item', { active: currentPath === '/pages/profile/index' }]"
			@tap="switchTab('/pages/profile/index')"
		>
			<MdIcon
				name="person"
				size="44"
				:color="currentPath === '/pages/profile/index' ? '#3b82f6' : '#71717a'"
				:filled="currentPath === '/pages/profile/index'"
			/>
			<text class="tab-label">个人</text>
		</view>
	</view>
</template>

<script>
import MdIcon from '@/components/MdIcon.vue'

export default {
	name: 'TabBar',
	components: {
		MdIcon
	},

	props: {
		currentPath: {
			type: String,
			default: '/pages/home/index'
		}
	},

	methods: {
		switchTab(path) {
			if (this.currentPath === path) return
			uni.switchTab({ url: path })
		}
	}
}
</script>

<style lang="scss" scoped>
.tab-bar {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	gap: 16px;
	padding: 12px 16px 32px;
	background-color: rgba(255, 255, 255, 0.85);
	border-top: 1px solid rgba(0, 0, 0, 0.04);
	z-index: 999;
}

.tab-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 8px 24px;
	border-radius: 12px;
	transition: all 0.2s ease;
}

.tab-item:active {
	transform: scale(0.9);
}

.tab-item.active {
	background-color: rgba(59, 130, 246, 0.1);
}

.tab-label {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 12px;
	font-weight: 500;
	color: #71717a;
	margin-top: 4px;
}

.tab-item.active .tab-label {
	color: #3b82f6;
}
</style>