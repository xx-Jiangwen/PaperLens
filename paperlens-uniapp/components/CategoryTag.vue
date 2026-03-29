<template>
	<view :class="['category-tag', { active }]" @tap="onTap">
		{{ text }}
	</view>
</template>

<script>
/**
 * CategoryTag - 分类标签组件
 * @description 用于显示论文分类或筛选标签
 */

export default {
	name: 'CategoryTag',

	props: {
		/**
		 * 标签文本
		 */
		text: {
			type: String,
			default: ''
		},
		/**
		 * 是否激活
		 */
		active: {
			type: Boolean,
			default: false
		}
	},

	methods: {
		onTap() {
			this.$emit('tap', this.text)
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.category-tag {
	display: inline-flex;
	align-items: center;
	height: 48rpx;
	padding: 0 $spacing-3;
	background-color: $color-bg-grouped;
	color: $color-text-secondary;
	border-radius: 12rpx;
	font-size: $font-size-footnote;
	font-weight: $font-weight-medium;
	transition: all $duration-fast;
}

.category-tag.active {
	background-color: $color-primary-light;
	color: $color-primary;
}
</style>