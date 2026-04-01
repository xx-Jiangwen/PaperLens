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
/* 全局样式 - 使用系统字体确保兼容性 */

/* ========== 全局盒模型与溢出控制 ========== */
/* 注意：小程序不支持 * 通配符，需逐元素设置 */
view,
text,
image,
button,
input,
textarea,
scroll-view,
swiper,
swiper-item {
	box-sizing: border-box;
}

/* 页面基础样式 */
page {
	background-color: #F5F5F7;
	color: #1a1c1d;
	font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
	font-size: 16px;
	line-height: 1.4;
	overflow-x: hidden;
	width: 100%;
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

/* 文字截断工具类 */
.text-ellipsis {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.text-clamp-2 {
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
}

.text-clamp-3 {
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 3;
	-webkit-box-orient: vertical;
}

/* 安全区域 */
.safe-area-bottom {
	padding-bottom: constant(safe-area-inset-bottom);
	padding-bottom: env(safe-area-inset-bottom);
}
</style>