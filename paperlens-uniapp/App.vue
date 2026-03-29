<script>
import userStore from './stores/user.js'

export default {
	onLaunch: function() {
		console.log('PaperLens App Launch')
		// 初始化用户状态
		userStore.init()
	},
	onShow: function() {
		console.log('PaperLens App Show')
	},
	onHide: function() {
		console.log('PaperLens App Hide')
	}
}
</script>

<style lang="scss">
@import '@/styles/variables.scss';

/* 全局样式 */
page {
	background-color: $color-bg-grouped;
	color: $color-text-primary;
	font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
	font-size: $font-size-body;
	line-height: $line-height-normal;
}

/* 公共布局类 */
.flex-row {
	display: flex;
	flex-direction: row;
}

.flex-column {
	display: flex;
	flex-direction: column;
}

/* 隐藏滚动条 */
::-webkit-scrollbar {
	display: none;
	width: 0;
	height: 0;
}

/* 按钮重置 */
button {
	margin: 0;
	padding: 0;
	background: none;
	border: none;
	line-height: inherit;
}

button::after {
	border: none;
}
</style>