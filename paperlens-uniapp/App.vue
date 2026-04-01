<script>
import userStore from './stores/user.js'

export default {
	onLaunch: function() {
		console.log('PaperLens App Launch')
		// 初始化用户状态
		userStore.init()
		// 加载 Material Symbols 字体
		this.loadFonts()
	},
	onShow: function() {
		console.log('PaperLens App Show')
	},
	onHide: function() {
		console.log('PaperLens App Hide')
	},
	methods: {
		loadFonts() {
			// 加载 Material Symbols Outlined 字体
			// #ifdef MP-WEIXIN
			wx.loadFontFace({
				family: 'Material Symbols Outlined',
				source: 'url("https://fonts.gstatic.com/s/materialsymbolsoutlined/v180/kJEhBvYX7BgnkSrUwT8OhrdQw4oELdPIeeII9v6oFsLjBuVY.woff2")',
				success: (res) => {
					console.log('Material Symbols 字体加载成功', res)
				},
				fail: (err) => {
					console.error('Material Symbols 字体加载失败', err)
				}
			})
			// 加载 Manrope 字体
			wx.loadFontFace({
				family: 'Manrope',
				source: 'url("https://fonts.gstatic.com/s/manrope/v15/xn7_YH41ul3N3i37EQ-UhZG3mn4.woff2")',
				success: (res) => {
					console.log('Manrope 字体加载成功', res)
				},
				fail: (err) => {
					console.error('Manrope 字体加载失败', err)
				}
			})
			// 加载 Inter 字体
			wx.loadFontFace({
				family: 'Inter',
				source: 'url("https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2")',
				success: (res) => {
					console.log('Inter 字体加载成功', res)
				},
				fail: (err) => {
					console.error('Inter 字体加载失败', err)
				}
			})
			// #endif
		}
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