<template>
	<view class="page">
		<!-- 顶部导航栏 -->
		<view class="header" :style="{ paddingTop: navBarTop + 'px' }">
			<view class="header-inner" :style="{ height: navBarHeight + 'px' }">
				<view class="header-left">
					<view class="icon-btn">
						<MdIcon name="menu" size="48" color="#414753" />
					</view>
				</view>
				<text class="brand-title">PaperLens</text>
				<view class="header-right">
					<view class="icon-btn" @tap="goToSearch">
						<MdIcon name="search" size="48" color="#0066cc" />
					</view>
				</view>
			</view>
		</view>

		<!-- 主内容区 -->
		<scroll-view class="main-content" :style="{ paddingTop: headerHeight + 'px' }" scroll-y>
			<!-- 标题区域 -->
			<view class="title-section">
				<view class="title-border"></view>
				<view class="title-content">
					<text class="page-title">学术动态</text>
					<text class="page-subtitle">为您挑选的最新学术论文</text>
				</view>
			</view>

			<!-- 切换按钮 -->
			<view class="tab-container">
				<view class="tab-switch">
					<view
						class="tab-btn"
						:class="{ active: currentTab === 'featured' }"
						@tap="switchToFeatured"
					>
						<text class="tab-text">一周精选</text>
					</view>
					<view
						class="tab-btn"
						:class="{ active: currentTab === 'all' }"
						@tap="switchToAll"
					>
						<text class="tab-text">全部论文</text>
					</view>
				</view>
			</view>

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
					<!-- 收藏按钮 -->
					<view class="bookmark-btn" @tap.stop="onBookmark(paper)">
						<MdIcon
							name="bookmark"
							size="48"
							:color="isBookmarked(paper.id) ? '#0066cc' : '#c1c6d5'"
							:filled="isBookmarked(paper.id)"
						/>
					</view>

					<!-- 卡片内容 -->
					<view class="card-content">
						<!-- 研究方向标签 -->
						<view class="category-badge" :class="getCategoryClass(paper)">
							<text class="category-text">{{ formatCategory(paper) }}</text>
						</view>

						<!-- 论文标题 -->
						<text class="card-title">{{ paper.title }}</text>

						<!-- 作者 -->
						<text class="card-authors">{{ formatAuthors(paper.authors) }}</text>

						<!-- 关键词标签 -->
						<view class="keywords-row" v-if="paper.categories && paper.categories.length > 0">
							<text
								v-for="(cat, index) in paper.categories.slice(0, 3)"
								:key="index"
								class="keyword-tag"
							>{{ cat }}</text>
						</view>

						<!-- 摘要 -->
						<text class="card-abstract">{{ paper.abstract }}</text>
					</view>
				</view>

				<!-- 加载中状态 -->
				<view v-if="loading && papers.length > 0" class="loading-more-state">
					<text class="loading-text">加载中...</text>
				</view>

				<!-- 空状态 -->
				<view v-if="!loading && papers.length === 0" class="empty-state">
					<MdIcon name="description" size="128" color="#c1c6d5" />
					<text class="empty-text">暂无论文</text>
				</view>
			</view>

			<!-- 分页组件 -->
			<view v-if="!loading && papers.length > 0" class="pagination">
				<view
					class="page-btn"
					:class="{ disabled: currentPage === 1 }"
					@tap="goToPrevPage"
				>
					<MdIcon name="arrow-back" size="36" :color="currentPage === 1 ? '#c1c6d5' : '#0066cc'" />
				</view>
				<view class="page-info">
					<text class="page-text">第 {{ currentPage }}/{{ totalPages }} 页</text>
				</view>
				<view class="page-jump">
					<input
						class="page-input"
						type="number"
						v-model="jumpPage"
						placeholder="跳转"
						@confirm="goToPage"
					/>
				</view>
				<view
					class="page-btn"
					:class="{ disabled: currentPage >= totalPages }"
					@tap="goToNextPage"
				>
					<MdIcon name="chevron-right" size="36" :color="currentPage >= totalPages ? '#c1c6d5' : '#0066cc'" />
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
import userStore from '@/stores/user.js'
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
			navBarHeight: 56,
			currentTab: 'featured',
			jumpPage: ''
		}
	},

	computed: {
		papers() {
			return this.currentTab === 'featured'
				? this.papersStore.featuredPapers
				: this.papersStore.allPapers
		},
		loading() {
			return this.currentTab === 'featured'
				? this.papersStore.featuredLoading
				: this.papersStore.allLoading
		},
		hasMore() {
			return this.currentTab === 'featured'
				? this.papersStore.featuredHasMore
				: this.papersStore.allHasMore
		},
		currentPage() {
			return this.currentTab === 'featured'
				? this.papersStore.featuredPage
				: this.papersStore.allPage
		},
		totalPages() {
			const total = this.currentTab === 'featured'
				? this.papersStore.featuredTotal
				: this.papersStore.allTotal
			return Math.ceil(total / 10) || 1
		},
		headerHeight() {
			return this.navBarTop + this.navBarHeight + 16
		}
	},

	onLoad() {
		const systemInfo = uni.getSystemInfoSync()
		this.statusBarHeight = systemInfo.statusBarHeight || 20

		try {
			const menuRect = uni.getMenuButtonBoundingClientRect()
			if (menuRect) {
				this.navBarTop = menuRect.bottom + 8
				this.navBarHeight = menuRect.height
			}
		} catch (e) {
			this.navBarTop = this.statusBarHeight + 44
		}

		if (userStore.isLoggedIn()) {
			this.bookmarksStore.fetchBookmarks(true)
		}

		this.papersStore.fetchFeaturedPapers(1)
	},

	onPullDownRefresh() {
		if (userStore.isLoggedIn()) {
			this.bookmarksStore.fetchBookmarks(true)
		}

		const refreshPromise = this.currentTab === 'featured'
			? this.papersStore.fetchFeaturedPapers(this.currentPage)
			: this.papersStore.fetchAllPapers(this.currentPage)

		refreshPromise.finally(() => {
			uni.stopPullDownRefresh()
		})
	},

	methods: {
		formatCategory(paper) {
			if (paper.primary_category) {
				return this.translateCategory(paper.primary_category)
			}
			if (paper.categories && paper.categories.length > 0) {
				return this.translateCategory(paper.categories[0])
			}
			return 'Paper'
		},

		translateCategory(cat) {
			const categoryMap = {
				'cs.CV': 'Computer Vision',
				'cs.CL': 'NLP',
				'cs.LG': 'Machine Learning',
				'cs.AI': 'Artificial Intelligence',
				'cs.RO': 'Robotics',
				'cs.NE': 'Neural Computing',
				'stat.ML': 'Statistics',
				'math.OC': 'Optimization',
				'physics': 'Physics',
				'q-bio': 'Quantitative Biology',
				'eess': 'Electrical Engineering'
			}
			for (const key in categoryMap) {
				if (cat.startsWith(key)) {
					return categoryMap[key]
				}
			}
			return cat.toUpperCase()
		},

		getCategoryClass(paper) {
			const cat = paper.primary_category || (paper.categories && paper.categories[0]) || ''
			if (cat.startsWith('cs.CV')) return 'category-cv'
			if (cat.startsWith('cs.CL')) return 'category-nlp'
			if (cat.startsWith('cs.RO')) return 'category-robotics'
			if (cat.startsWith('cs.LG') || cat.startsWith('stat.ML')) return 'category-ml'
			return 'category-default'
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
			const wasBookmarked = this.isBookmarked(paper.id)
			await this.bookmarksStore.toggleBookmark(paper.id)
			uni.showToast({
				title: wasBookmarked ? '已取消收藏' : '已收藏',
				icon: 'success'
			})
		},

		switchTab(url) {
			uni.switchTab({ url })
		},

		switchToFeatured() {
			if (this.currentTab === 'featured') return
			this.currentTab = 'featured'
			if (this.papersStore.featuredPapers.length === 0) {
				this.papersStore.fetchFeaturedPapers(1)
			}
		},

		switchToAll() {
			if (this.currentTab === 'all') return
			this.currentTab = 'all'
			if (this.papersStore.allPapers.length === 0) {
				this.papersStore.fetchAllPapers(1)
			}
		},

		goToPrevPage() {
			if (this.loading || this.currentPage <= 1) return
			const page = this.currentPage - 1
			if (this.currentTab === 'featured') {
				this.papersStore.fetchFeaturedPapers(page)
			} else {
				this.papersStore.fetchAllPapers(page)
			}
		},

		goToNextPage() {
			if (this.loading || this.currentPage >= this.totalPages) return
			const page = this.currentPage + 1
			if (this.currentTab === 'featured') {
				this.papersStore.fetchFeaturedPapers(page)
			} else {
				this.papersStore.fetchAllPapers(page)
			}
		},

		goToPage() {
			const page = parseInt(this.jumpPage)
			if (!page || page < 1 || page > this.totalPages) {
				uni.showToast({
					title: `请输入 1-${this.totalPages} 之间的页码`,
					icon: 'none'
				})
				return
			}
			if (this.loading) return
			if (this.currentTab === 'featured') {
				this.papersStore.fetchFeaturedPapers(page)
			} else {
				this.papersStore.fetchAllPapers(page)
			}
			this.jumpPage = ''
		}
	}
}
</script>

<style lang="scss" scoped>
/* ========== 页面基础 ========== */

.page {
	min-height: 100vh;
	background-color: #f3f3f5;
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
	background-color: rgba(255, 255, 255, 0.7);
	backdrop-filter: blur(20px);
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
	color: #1a1c1d;
	letter-spacing: -0.02em;
	text-align: center;
	flex: 1;
}

/* ========== 主内容区 ========== */

.main-content {
	flex: 1;
	padding: 0 16px 120px;
	max-width: 600px;
	margin: 0 auto;
	width: 100%;
	box-sizing: border-box;
	overflow-x: hidden;
}

/* ========== 标题区域 ========== */

.title-section {
	display: flex;
	flex-direction: row;
	margin-bottom: 24px;
	padding-left: 8px;
}

.title-border {
	width: 4px;
	background-color: #0066cc;
	border-radius: 2px;
	margin-right: 12px;
}

.title-content {
	display: flex;
	flex-direction: column;
}

.page-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 28px;
	font-weight: 800;
	color: #1a1c1d;
	letter-spacing: -0.02em;
}

.page-subtitle {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 500;
	color: #414753;
	margin-top: 4px;
}

/* ========== 切换按钮 ========== */

.tab-container {
	display: flex;
	justify-content: center;
	margin-bottom: 24px;
}

.tab-switch {
	display: inline-flex;
	flex-direction: row;
	background-color: #e2e2e4;
	border-radius: 12px;
	padding: 4px;
	gap: 4px;
}

.tab-btn {
	padding: 8px 20px;
	border-radius: 8px;
	transition: all 0.2s ease;
}

.tab-btn.active {
	background-color: #ffffff;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.tab-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 600;
	color: #414753;
}

.tab-btn.active .tab-text {
	color: #0066cc;
}

/* ========== 论文卡片 ========== */

.paper-list {
	display: flex;
	flex-direction: column;
	gap: 20px;
	width: 100%;
	box-sizing: border-box;
}

.paper-card {
	background-color: #ffffff;
	border-radius: 16px;
	padding: 24px;
	box-shadow: 0 10px 40px rgba(26, 28, 29, 0.06);
	transition: all 0.3s ease;
	width: 100%;
	box-sizing: border-box;
	position: relative;
}

.paper-card:active {
	transform: translateY(-2px);
	box-shadow: 0 14px 50px rgba(26, 28, 29, 0.1);
}

.bookmark-btn {
	position: absolute;
	top: 20px;
	right: 20px;
	padding: 4px;
}

.card-content {
	display: flex;
	flex-direction: column;
	gap: 12px;
	padding-right: 40px;
}

/* ========== 研究方向标签 ========== */

.category-badge {
	align-self: flex-start;
	padding: 4px 10px;
	border-radius: 999px;
}

.category-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 10px;
	font-weight: 700;
	letter-spacing: 0.05em;
	text-transform: uppercase;
}

.category-cv {
	background-color: rgba(0, 102, 204, 0.1);
}

.category-cv .category-text {
	color: #0066cc;
}

.category-nlp {
	background-color: rgba(136, 55, 0, 0.1);
}

.category-nlp .category-text {
	color: #883700;
}

.category-robotics {
	background-color: rgba(94, 94, 99, 0.15);
}

.category-robotics .category-text {
	color: #46464b;
}

.category-ml {
	background-color: rgba(0, 102, 204, 0.1);
}

.category-ml .category-text {
	color: #0066cc;
}

.category-default {
	background-color: rgba(65, 71, 83, 0.1);
}

.category-default .category-text {
	color: #414753;
}

/* ========== 论文标题 ========== */

.card-title {
	font-family: -apple-system, BlinkMacSystemFont, 'Manrope', 'Segoe UI', Roboto, sans-serif;
	font-size: 20px;
	font-weight: 700;
	color: #1a1c1d;
	line-height: 1.3;
	word-break: break-word;
	overflow-wrap: break-word;
}

/* ========== 作者 ========== */

.card-authors {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 500;
	color: #414753;
}

/* ========== 关键词标签 ========== */

.keywords-row {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	gap: 8px;
}

.keyword-tag {
	padding: 6px 12px;
	border: 1px solid #e8e8ea;
	border-radius: 999px;
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 11px;
	font-weight: 600;
	color: #414753;
	text-transform: uppercase;
	letter-spacing: 0.03em;
}

/* ========== 摘要 ========== */

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

.loading-more-state {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 32px 0;
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

/* ========== 分页组件 ========== */

.pagination {
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	gap: 12px;
	padding: 32px 0 16px;
}

.page-btn {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 44px;
	height: 44px;
	border-radius: 50%;
	background-color: #ffffff;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
	transition: all 0.2s ease;
}

.page-btn:active {
	transform: scale(0.9);
}

.page-btn.disabled {
	opacity: 0.5;
}

.page-info {
	display: flex;
	align-items: center;
	justify-content: center;
	min-width: 80px;
}

.page-text {
	font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
	font-size: 14px;
	font-weight: 600;
	color: #1a1c1d;
}

.page-jump {
	display: flex;
	align-items: center;
}

.page-input {
	width: 60px;
	height: 36px;
	background-color: #ffffff;
	border: 1px solid #e8e8ea;
	border-radius: 8px;
	text-align: center;
	font-size: 14px;
	color: #1a1c1d;
}

.page-input::placeholder {
	color: #c1c6d5;
}

/* ========== 底部导航 ========== */

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