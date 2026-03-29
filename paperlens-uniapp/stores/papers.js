/**
 * 论文状态管理
 */

import { defineStore } from 'pinia'
import { getTodayPapers, getPapers, getPaper } from '../api/papers.js'

export const usePapersStore = defineStore('papers', {
  state: () => ({
    // 今日精选
    featuredPapers: [],
    featuredLoading: false,

    // 全部论文
    allPapers: [],
    allLoading: false,
    allPage: 1,
    allHasMore: true,
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
     * 获取今日精选论文
     */
    async fetchFeaturedPapers() {
      this.featuredLoading = true
      try {
        const res = await getTodayPapers()
        if (res.code === 200 && res.data) {
          this.featuredPapers = res.data
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
     * @param {boolean} reset - 是否重置列表
     */
    async fetchAllPapers(reset = false) {
      if (reset) {
        this.allPage = 1
        this.allPapers = []
        this.allHasMore = true
      }

      if (!this.allHasMore) return { code: 200, data: this.allPapers }

      this.allLoading = true
      try {
        const params = {
          page: this.allPage,
          size: 20
        }
        if (this.selectedSource) {
          params.source = this.selectedSource
        }

        const res = await getPapers(params)
        if (res.code === 200 && res.data) {
          if (reset) {
            this.allPapers = res.data
          } else {
            this.allPapers = [...this.allPapers, ...res.data]
          }
          this.allHasMore = res.data.length >= 20
          if (this.allHasMore) {
            this.allPage++
          }
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
      this.fetchAllPapers(true)
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