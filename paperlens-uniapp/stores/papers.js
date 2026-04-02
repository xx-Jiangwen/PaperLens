/**
 * 论文状态管理
 */

import { defineStore } from 'pinia'
import { getTodayPapers, getPapers, getPaper } from '../api/papers.js'

export const usePapersStore = defineStore('papers', {
  state: () => ({
    // 一周精选
    featuredPapers: [],
    featuredLoading: false,
    featuredPage: 1,
    featuredHasMore: true,
    featuredTotal: 0,

    // 全部论文
    allPapers: [],
    allLoading: false,
    allPage: 1,
    allHasMore: true,
    allTotal: 0,
    selectedSource: null,

    // 当前论文详情
    currentPaper: null,
    detailLoading: false
  }),

  getters: {
    /**
     * 是否有精选论文
     */
    hasFeaturedPapers: (state) => state.featuredPapers.length > 0,

    /**
     * 是否有更多论文
     */
    hasMorePapers: (state) => state.allHasMore
  },

  actions: {
    /**
     * 获取一周精选论文
     * @param {number} page - 页码
     */
    async fetchFeaturedPapers(page = 1) {
      this.featuredPage = page
      this.featuredLoading = true
      try {
        const res = await getTodayPapers({ page, size: 10 })
        if (res.code === 200 && res.data) {
          this.featuredPapers = res.data.items || res.data
          this.featuredTotal = res.data.total || 0
          this.featuredHasMore = res.data.hasMore !== undefined
            ? res.data.hasMore
            : (res.data.items || res.data).length >= 10
        }
        return res
      } catch (e) {
        console.error('获取精选论文失败', e)
        return { code: 500, msg: '获取失败', data: null }
      } finally {
        this.featuredLoading = false
      }
    },

    /**
     * 获取全部论文
     * @param {number} page - 页码
     */
    async fetchAllPapers(page = 1) {
      this.allPage = page
      this.allLoading = true
      try {
        const params = {
          page,
          size: 10
        }
        if (this.selectedSource) {
          params.source = this.selectedSource
        }

        const res = await getPapers(params)
        if (res.code === 200 && res.data) {
          this.allPapers = res.data.items || res.data
          this.allTotal = res.data.total || 0
          this.allHasMore = res.data.hasMore !== undefined
            ? res.data.hasMore
            : (res.data.items || res.data).length >= 10
        }
        return res
      } catch (e) {
        console.error('获取论文列表失败', e)
        return { code: 500, msg: '获取失败', data: null }
      } finally {
        this.allLoading = false
      }
    },

    /**
     * 设置数据源筛选
     * @param {string|null} source - 数据源
     */
    setSelectedSource(source) {
      this.selectedSource = source
      this.fetchAllPapers(1)
    },

    /**
     * 获取论文详情
     * @param {string} paperId - 论文 ID
     */
    async fetchPaperDetail(paperId) {
      this.detailLoading = true
      try {
        const res = await getPaper(paperId)
        if (res.code === 200 && res.data) {
          this.currentPaper = res.data
        }
        return res
      } catch (e) {
        console.error('获取论文详情失败', e)
        return { code: 500, msg: '获取失败', data: null }
      } finally {
        this.detailLoading = false
      }
    },

    /**
     * 清除当前论文
     */
    clearCurrentPaper() {
      this.currentPaper = null
    }
  }
})