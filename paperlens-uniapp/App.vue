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

<style>
/* 全局样式 */
page {
	background-color: #0d1117;
	color: #e6edf3;
	font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

/* 公共布局类 */
.uni-row {
	flex-direction: row;
}

.uni-column {
	flex-direction: column;
}
</style>