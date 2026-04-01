<template>
	<image
		class="icon-image"
		:src="iconPath"
		:style="{ width: sizePx + 'px', height: sizePx + 'px' }"
		mode="aspectFit"
	/>
</template>

<script>
// 图标路径映射
const ICON_PATHS = {
	// 导航
	home: '/static/icons/home.svg',
	'home-active': '/static/icons/home-active.svg',
	person: '/static/icons/profile.svg',
	'person-active': '/static/icons/profile-active.svg',

	// 操作
	menu: '/static/icons/menu.svg',
	search: '/static/icons/search.svg',
	'arrow-back': '/static/icons/arrow-back.svg',
	'chevron-right': '/static/icons/chevron-right.svg',
	close: '/static/icons/close.svg',

	// 功能
	bookmark: '/static/icons/bookmark.svg',
	'bookmark-active': '/static/icons/bookmark-active.svg',
	settings: '/static/icons/settings.svg',
	share: '/static/icons/share.svg',
	refresh: '/static/icons/refresh.svg',

	// 内容
	description: '/static/icons/description.svg',
	article: '/static/icons/article.svg',

	// AI
	'auto-awesome': '/static/icons/auto-awesome.svg',

	// 其他
	add: '/static/icons/add.svg',
	'keyboard-arrow-down': '/static/icons/keyboard-arrow-down.svg',
	done: '/static/icons/done.svg',
	check: '/static/icons/check.svg',
	edit: '/static/icons/edit.svg'
}

export default {
	name: 'MdIcon',
	props: {
		name: {
			type: String,
			required: true
		},
		size: {
			type: [Number, String],
			default: 44
		},
		color: {
			type: String,
			default: '#1a1c1d'
		},
		filled: {
			type: Boolean,
			default: false
		}
	},
	computed: {
		sizePx() {
			return Number(this.size) / 2
		},
		iconPath() {
			// 如果 filled 为 true，尝试使用 active 版本
			if (this.filled) {
				const activePath = ICON_PATHS[this.name + '-active']
				if (activePath) return activePath
			}
			return ICON_PATHS[this.name] || ICON_PATHS['home']
		}
	}
}
</script>

<style scoped>
.icon-image {
	display: block;
}
</style>