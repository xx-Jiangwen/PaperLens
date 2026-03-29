<template>
	<view class="chat-input">
		<!-- 快捷问题 -->
		<view v-if="quickQuestions && quickQuestions.length > 0" class="quick-questions">
			<scroll-view scroll-x="true" class="questions-scroll">
				<view
					v-for="(q, index) in quickQuestions"
					:key="index"
					class="question-tag"
					:data-question="q"
					@tap="onQuickQuestion"
				>{{ q }}</view>
			</scroll-view>
		</view>

		<!-- 输入框 -->
		<view class="input-row">
			<input
				class="input"
				v-model="inputValue"
				:placeholder="placeholder"
				@confirm="onSend"
			/>
			<view
				:class="['send-btn', { active: inputValue.trim() }]"
				@tap="onSend"
			>
				<text class="send-icon">➤</text>
			</view>
		</view>
	</view>
</template>

<script>
/**
 * ChatInput - 对话输入组件
 * @description 带快捷问题的对话输入框
 */

export default {
	name: 'ChatInput',

	props: {
		/**
		 * 占位文本
		 */
		placeholder: {
			type: String,
			default: '提问关于这篇论文...'
		},
		/**
		 * 快捷问题列表
		 */
		quickQuestions: {
			type: Array,
			default: () => [
				'这篇论文的主要贡献是什么？',
				'方法有什么创新点？',
				'实验结果如何？'
			]
		}
	},

	data() {
		return {
			inputValue: ''
		}
	},

	methods: {
		onSend() {
			const text = this.inputValue.trim()
			if (text) {
				this.$emit('send', text)
				this.inputValue = ''
			}
		},

		onQuickQuestion(e) {
			const question = e.currentTarget.dataset.question
			this.$emit('quickQuestion', question)
		}
	}
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.chat-input {
	background-color: $color-bg-card;
	border-top: 1rpx solid $color-separator;
	padding: $spacing-3 $spacing-4;
	padding-bottom: calc($spacing-3 + env(safe-area-inset-bottom));
}

.quick-questions {
	margin-bottom: $spacing-3;
}

.questions-scroll {
	white-space: nowrap;
}

.question-tag {
	display: inline-flex;
	align-items: center;
	height: 56rpx;
	padding: 0 $spacing-3;
	background-color: $color-bg-grouped;
	color: $color-text-secondary;
	border-radius: $radius-full;
	font-size: $font-size-footnote;
	margin-right: $spacing-2;
}

.input-row {
	display: flex;
	flex-direction: row;
	align-items: center;
}

.input {
	flex: 1;
	height: 72rpx;
	background-color: $color-bg-grouped;
	border-radius: $radius-sm;
	padding: 0 $spacing-4;
	font-size: $font-size-body;
	color: $color-text-primary;
}

.send-btn {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 72rpx;
	height: 72rpx;
	background-color: $color-bg-grouped;
	border-radius: 50%;
	margin-left: $spacing-2;
}

.send-btn.active {
	background-color: $color-primary;
}

.send-icon {
	font-size: $font-size-body;
	color: $color-text-tertiary;
}

.send-btn.active .send-icon {
	color: #FFFFFF;
}
</style>