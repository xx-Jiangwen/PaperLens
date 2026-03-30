<template>
	<view class="search-bar" @tap="onTap">
		<view class="search-icon">
			<text>🔍</text>
		</view>
		<input
			v-if="!readonly"
			class="search-input"
			:value="value"
			:placeholder="placeholder"
			:placeholder-style="placeholderStyle"
			@input="onInput"
			@confirm="onSubmit"
			@focus="onFocus"
		/>
		<view v-else class="search-placeholder">
			{{ placeholder }}
		</view>
	</view>
</template>

<script>
/**
 * SearchBar - 搜索框组件
 * @description 编辑部风格的搜索框
 */

export default {
	name: 'SearchBar',

	props: {
		placeholder: {
			type: String,
			default: '搜索论文'
		},
		value: {
			type: String,
			default: ''
		},
		readonly: {
			type: Boolean,
			default: false
		}
	},

	computed: {
		placeholderStyle() {
			return 'color: #c4c6cf;'
		}
	},

	methods: {
		onTap() {
			if (this.readonly) {
				this.$emit('tap')
			}
		},

		onInput(e) {
			this.$emit('input', e.detail.value)
		},

		onSubmit(e) {
			this.$emit('submit', e.detail.value)
		},

		onFocus(e) {
			this.$emit('focus', e)
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.search-bar {
	display: flex;
	flex-direction: row;
	align-items: center;
	height: 80rpx;
	background-color: $color-surface-container-low;
	border-radius: $radius-full;
	padding: 0 $spacing-4;
}

.search-icon {
	margin-right: $spacing-2;
	font-size: 32rpx;
	opacity: 0.6;
	color: $color-text-secondary;
}

.search-input {
	flex: 1;
	height: 80rpx;
	font-family: $font-family-body;
	font-size: $font-size-body;
	color: $color-text-primary;
	background: transparent;
}

.search-placeholder {
	flex: 1;
	font-family: $font-family-body;
	font-size: $font-size-body;
	color: $color-text-placeholder;
}
</style>