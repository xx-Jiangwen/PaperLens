<template>
	<view class="tab-bar">
		<view
			:class="['tab-item', { active: currentPath === '/pages/home/index' }]"
			@tap="switchTab('/pages/home/index')"
		>
			<text class="tab-icon">📖</text>
			<text class="tab-label">首页</text>
		</view>
		<view
			:class="['tab-item', { active: currentPath === '/pages/profile/index' }]"
			@tap="switchTab('/pages/profile/index')"
		>
			<text class="tab-icon">👤</text>
			<text class="tab-label">我的</text>
		</view>
	</view>
</template>

<script>
/**
 * TabBar - 自定义底部导航栏
 * @description 编辑部风格的底部导航，深蓝渐变激活态
 */

export default {
	name: 'TabBar',

	props: {
		/**
		 * 当前页面路径
		 */
		currentPath: {
			type: String,
			default: '/pages/home/index'
		}
	},

	methods: {
		switchTab(path) {
			if (this.currentPath === path) return
			// 使用 redirectTo 因为首页和我的页是主入口
			uni.redirectTo({
				url: path
			})
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.tab-bar {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	justify-content: center;
	align-items: center;
	padding: $spacing-3 $spacing-8 $spacing-6;
	background-color: rgba($color-bg, 0.9);
	backdrop-filter: blur(20px);
	-webkit-backdrop-filter: blur(20px);
	border-top: 1rpx solid $color-separator;
	opacity: 0.15;
	box-shadow: 0 -8rpx 32rpx rgba(0, 32, 69, 0.04);
	z-index: 999;
}

.tab-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: $spacing-2 $spacing-6;
	color: $color-text-secondary;
	transition: all $duration-fast;
}

.tab-item:active {
	transform: scale(0.95);
}

.tab-item.active {
	background: linear-gradient(135deg, $color-primary 0%, $color-primary-container 100%);
	border-radius: $radius-md;
	color: $color-on-primary;
}

.tab-icon {
	font-size: 40rpx;
	line-height: 1;
}

.tab-label {
	font-size: $font-size-label-xs;
	font-weight: $font-weight-bold;
	letter-spacing: $letter-spacing-widest;
	text-transform: uppercase;
	margin-top: $spacing-1;
}
</style>