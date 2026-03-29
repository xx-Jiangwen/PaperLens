<template>
	<view class="segmented-control">
		<view
			v-for="option in options"
			:key="option.value"
			:class="['segment', { active: value === option.value }]"
			:data-value="option.value"
			@tap="onTap"
		>
			{{ option.label }}
		</view>
	</view>
</template>

<script>
/**
 * SegmentedControl - Tab 切换组件
 * @description Apple 风格的分段控制器
 */

export default {
	name: 'SegmentedControl',

	props: {
		/**
		 * 选项数组
		 */
		options: {
			type: Array,
			default: () => []
		},
		/**
		 * 当前选中值
		 */
		value: {
			type: [String, Number],
			default: ''
		}
	},

	methods: {
		onTap(e) {
			const value = e.currentTarget.dataset.value
			if (value !== this.value) {
				this.$emit('change', value)
				this.$emit('input', value)
			}
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.segmented-control {
	display: flex;
	flex-direction: row;
	background-color: $color-bg-grouped;
	border-radius: $radius-sm;
	padding: 4rpx;
}

.segment {
	flex: 1;
	display: flex;
	align-items: center;
	justify-content: center;
	height: 64rpx;
	font-size: $font-size-subheadline;
	font-weight: $font-weight-medium;
	color: $color-text-secondary;
	transition: all $duration-fast;
	border-radius: 12rpx;
}

.segment.active {
	background-color: $color-bg-card;
	color: $color-text-primary;
	box-shadow: $shadow-sm;
}
</style>