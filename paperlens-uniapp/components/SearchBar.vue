<template>
	<view class="search-bar" @tap="onTap">
		<view class="search-icon">
			<text class="iconfont">🔍</text>
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
 * @description Apple 风格的搜索框
 */

export default {
	name: 'SearchBar',

	props: {
		/**
		 * 占位文本
		 */
		placeholder: {
			type: String,
			default: '搜索论文'
		},
		/**
		 * 输入值
		 */
		value: {
			type: String,
			default: ''
		},
		/**
		 * 是否只读（点击跳转搜索页）
		 */
		readonly: {
			type: Boolean,
			default: false
		}
	},

	computed: {
		placeholderStyle() {
			return 'color: #C7C7CC;'
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
	background-color: $color-bg-grouped;
	border-radius: $radius-sm;
	padding: 0 $spacing-4;
}

.search-icon {
	margin-right: $spacing-2;
	font-size: $font-size-body;
	opacity: 0.5;
}

.search-input {
	flex: 1;
	height: 80rpx;
	font-size: $font-size-body;
	color: $color-text-primary;
	background: transparent;
}

.search-placeholder {
	flex: 1;
	font-size: $font-size-body;
	color: $color-text-placeholder;
}
</style>