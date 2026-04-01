<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header" :style="{ paddingTop: navBarTop + 'px' }">
			<view class="header-inner" :style="{ height: navBarHeight + 'px' }">
				<view class="header-left">
					<view class="icon-btn">
						<MdIcon name="menu" size="48" color="#3b82f6" />
					</view>
				</view>
				<text class="brand-title">PaperLens</text>
				<view class="header-right">
					<view class="icon-btn" @tap="goToSearch">
						<MdIcon name="search" size="48" color="#3b82f6" />
					</view>
				</view>
			</view>
		</view>

		<!-- 主内容区 -->
		<scroll-view class="main-content" :style="{ paddingTop: headerHeight + 'px' }" scroll-y="true">
			<!-- 标题 -->
			<view class="page-title">学术动态</view>

			<!-- 论文列表 -->
			<view class="paper-list">
				<!-- 加载状态 -->
				<view v-if="loading && papers.length === 0" class="loading-state">
					<text class="loading-text">加载中...</text>
				</view>

				<!-- 论文卡片 -->
				<view
					v-for="paper in papers"
					:key="paper.id"
					class="paper-card"
					@tap="goToDetail(paper)"
				>
					<view class="card-top">
						<view class="source-badge">{{ formatSource(paper) }}</view>
						<view class="bookmark-btn" @tap.stop="onBookmark(paper)">
							<MdIcon
								name="bookmark"
								size="48"
								:color="isBookmarked(paper.id) ? '#0066cc' : '#0066cc'"
								:filled="isBookmarked(paper.id)"
								:class="{ 'icon-dim': !isBookmarked(paper.id) }"
							/>
						</view>
					</view>
					<view class="card-title">{{ paper.title }}</view>
					<view class="card-authors">{{ formatAuthors(paper.authors) }}</view>
					<view class="card-abstract">{{ paper.abstract }}</view>
				</view>

				<!-- 空状态 -->
				<view v-if="!loading && papers.length === 0" class="empty-state">
					<MdIcon name="description" size="128" color="#c1c6d5" />
					<text class="empty-text">暂无论文</text>
				</view>
			</view>
		</scroll-view>

		<!-- 底部导航 -->
		<view class="bottom-nav">
			<view class="nav-item active" @tap="switchTab('/pages/home/index')">
				<MdIcon name="home" size="52" color="#3b82f6" filled />
			</view>
			<view class="nav-item" @tap="switchTab('/pages/profile/index')">
				<MdIcon name="person" size="52" color="#a1a1aa" />
			</view>
		</view>
	</view>
</template>

<script>
import { usePapersStore } from '@/stores/papers.js'
import { useBookmarksStore } from '@/stores/bookmarks.js'
import MdIcon from '@/components/MdIcon.vue'

export default {
	components: {
		MdIcon
	},

	setup() {
		const papersStore = usePapersStore()
		const bookmarksStore = useBookmarksStore()
		return { papersStore, bookmarksStore }
	},

	data() {
		return {
			statusBarHeight: 20,
			navBarTop: 20,
			navBarHeight: 56
		}
	},

	computed: {
		papers() {
			return this.papersStore.featuredPapers
		},
		loading() {
			return this.papersStore.featuredLoading
		},
		headerHeight() {
			return this.navBarTop + this.navBarHeight + 16
		}
	},

	onLoad() {
		// 获取状态栏高度和胶囊按钮位置
		const systemInfo = uni.getSystemInfoSync()
		this.statusBarHeight = systemInfo.statusBarHeight || 20

		// 获取微信胶囊按钮位置，确保导航栏不被遮挡
		try {
			const menuRect = uni.getMenuButtonBoundingClientRect()
			if (menuRect) {
				// 导航栏顶部位置 = 胶囊底部 + 间距
				this.navBarTop = menuRect.bottom + 8
				// 导航栏高度与胶囊对齐
				this.navBarHeight = menuRect.height
			}
		} catch (e) {
			// 非微信环境使用默认值
			this.navBarTop = this.statusBarHeight + 44
		}

		this.papersStore.fetchFeaturedPapers()
	},

	onPullDownRefresh() {
		this.papersStore.fetchFeaturedPapers().finally(() => {
			uni.stopPullDownRefresh()
		})
	},

	methods: {
		formatSource(paper) {
			if (paper.arxiv_id) return `ARXIV:${paper.arxiv_id}`
			if (paper.categories && paper.categories.length > 0) {
				return paper.categories[0].toUpperCase()
			}
			return 'PAPER'
		},

		formatAuthors(authors) {
			if (!authors || authors.length === 0) return ''
			const display = authors.slice(0, 3).join(', ')
			const more = authors.length > 3 ? ' 等' : ''
			return `${display}${more}`
		},

		isBookmarked(paperId) {
			return this.bookmarksStore.isBookmarked(paperId)
		},

		goToSearch() {
			uni.navigateTo({ url: '/pages/home/search' })
		},

		goToDetail(paper) {
			uni.navigateTo({
				url: `/pages/home/detail?id=${encodeURIComponent(paper.id)}`
			})
		},

		async onBookmark(paper) {
			await this.bookmarksStore.toggleBookmark(paper.id)
			uni.showToast({
				title: this.isBookmarked(paper.id) ? '已取消收藏' : '已收藏',
				icon: 'success'
			})
		},

		switchTab(url) {
			uni.switchTab({ url })
		}
	}
}
</script>

<style lang="scss" scoped>
/* ========== 页面基础 ========== */

	.page {
		min-height: 100vh;
		background-color: #F5F5F7;
		display: flex;
		flex-direction: column;
		overflow-x: hidden;
		width: 100%;
	}

/* ========== 顶部导航栏 ========== */

	.header {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 100;
		background-color: rgba(255, 255, 255, 0.85);
		border-bottom: 1px solid rgba(0, 0, 0, 0.04);
	}

	.header-inner {
		display: flex;
		flex-direction: row;
	justify-content: space-between;
	align-items: center;
		height: 56px;
		padding: 12px 16px 8px;
		max-width: 600px;
		margin: 0 auto;
	}

.header-left,
	.header-right {
		width: 48px;
		display: flex;
	align-items: center;
	}

	.icon-btn {
		padding: 8px;
	}

	.brand-title {
		font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
		font-size: 20px;
		font-weight: 700;
		color: #18181b;
		letter-spacing: -0.02em;
		text-align: center;
		flex: 1;
	}

/* ========== 主内容区 ========== */

	.main-content {
		flex: 1;
		padding: 0 16px 100px;
		max-width: 600px;
		margin: 0 auto;
		width: 100%;
		box-sizing: border-box;
		overflow-x: hidden;
	}

	.page-title {
		font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
		font-size: 30px;
		font-weight: 800;
		color: #1a1c1d;
		letter-spacing: -0.02em;
		margin-bottom: 24px;
	}

/* ========== 论文卡片 ========== */

	.paper-list {
		display: flex;
		flex-direction: column;
		gap: 20px;
		width: 100%;
		box-sizing: border-box;
		overflow-x: hidden;
	}

	.paper-card {
		background-color: #ffffff;
		border-radius: 12px;
		padding: 20px;
		box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
		transition: all 0.3s ease;
		width: 100%;
		box-sizing: border-box;
		overflow: hidden;
	}

	.paper-card:active {
		box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
		transform: scale(0.98);
	}

	.card-top {
		width: 100%;
		display: flex;
		flex-direction: row;
	justify-content: space-between;
	align-items: flex-start;
		margin-bottom: 12px;
	}

	.source-badge {
		background-color: #e8e8ea;
		color: #414753;
		font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
		font-size: 10px;
		font-weight: 700;
		letter-spacing: 0.1em;
		padding: 4px 10px;
		border-radius: 999px;
			flex-shrink: 0;
	}

	.bookmark-btn {
		padding: 6px;
		margin-top: -6px;
		margin-right: -6px;
			flex-shrink: 0;
	}

	.icon-dim {
		opacity: 0.2;
	}

	.paper-card:active .icon-dim {
		opacity: 0.5;
	}

	.card-title {
		font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
		font-size: 18px;
		font-weight: 700;
		color: #1a1c1d;
		line-height: 1.3;
		margin-bottom: 8px;
		word-break: break-word;
		overflow-wrap: break-word;
	}

	.card-authors {
		font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
		font-size: 14px;
		font-weight: 500;
		color: #626267;
		margin-bottom: 12px;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.card-abstract {
		font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
		font-size: 14px;
		color: #414753;
		line-height: 1.6;
		overflow: hidden;
		text-overflow: ellipsis;
		display: -webkit-box;
		-webkit-line-clamp: 3;
		-webkit-box-orient: vertical;
		word-break: break-word;
	}

/* ========== 加载状态 ========== */

	.loading-state {
		display: flex;
	align-items: center;
	justify-content: center;
		padding: 60px;
	}

	.loading-text {
		font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
		font-size: 16px;
		color: #414753;
	}

/* ========== 空状态 ========== */

	.empty-state {
		display: flex;
		flex-direction: column;
	align-items: center;
	justify-content: center;
		padding: 60px;
	}

	.empty-text {
		font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
		font-size: 16px;
		color: #414753;
		margin-top: 16px;
	}

/* ========== 底部导航 - 仅图标 ========== */

	.bottom-nav {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		display: flex;
		flex-direction: row;
	justify-content: center;
	align-items: center;
		gap: 64px;
		padding: 16px 16px 32px;
		background-color: rgba(255, 255, 255, 0.85);
		border-top: 1px solid rgba(0, 0, 0, 0.04);
	}

	.nav-item {
		display: flex;
	align-items: center;
	justify-content: center;
		width: 56px;
		height: 56px;
		border-radius: 50%;
		transition: all 0.2s ease;
	}

	.nav-item:active {
		transform: scale(0.9);
	}

	.nav-item.active {
		background-color: rgba(59, 130, 246, 0.1);
	}
</style>