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
 * @description 编辑部风格的分段控制器（pill 样式）
 */

export default {
	name: 'SegmentedControl',

	props: {
		options: {
			type: Array,
			default: () => []
		},
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
	gap: $spacing-2;
}

.segment {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 44rpx;
	padding: 0 $spacing-4;
	background-color: $color-surface-variant;
	color: $color-on-surface-variant;
	border-radius: $radius-full;
	font-family: $font-family-label;
	font-size: $font-size-label-xs;
	font-weight: $font-weight-bold;
	letter-spacing: $letter-spacing-widest;
	text-transform: uppercase;
	transition: all $duration-fast;
}

.segment.active {
	background-color: $color-primary-container;
	color: $color-on-primary;
}
</style>