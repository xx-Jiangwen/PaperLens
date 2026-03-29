/**
 * 收藏状态管理
 */

import { defineStore } from 'pinia'
import { getBookmarks, addBookmark, removeBookmark } from '../api/bookmarks.js'

export const useBookmarksStore = defineStore('bookmarks', {
  state: () => ({
    bookmarks: [],
    bookmarkedIds: new Set(),
    loading: false,
    page: 1,
    hasMore: true
  }),

  getters: {
    /**
     * 是否已收藏
     * @param {string} paperId - 论文 ID
     */
    isBookmarked: (state) => (paperId) => {
      return state.bookmarkedIds.has(paperId)
    },

    /**
     * 收藏数量
     */
    bookmarkCount: (state) => state.bookmarks.length
  },

  actions: {
    /**
     * 获取收藏列表
     * @param {boolean} reset - 是否重置列表
     */
    async fetchBookmarks(reset = false) {
      if (reset) {
        this.page = 1
        this.bookmarks = []
        this.hasMore = true
      }

      if (!this.hasMore) return { code: 200, data: this.bookmarks }

      this.loading = true
      try {
        const res = await getBookmarks({ page: this.page, size: 20 })
        if (res.code === 200 && res.data) {
          if (reset) {
            this.bookmarks = res.data
          } else {
            this.bookmarks = [...this.bookmarks, ...res.data]
          }
          // 更新 ID 集合
          res.data.forEach(item => {
            if (item.paper_id) {
              this.bookmarkedIds.add(item.paper_id)
            }
          })
          this.hasMore = res.data.length >= 20
          if (this.hasMore) {
            this.page++
          }
        }
        return res
      } catch (e) {
        console.error('获取收藏列表失败', e)
        return { code: 500, msg: '获取失败', data: null }
      } finally {
        this.loading = false
      }
    },

    /**
     * 添加收藏
     * @param {string} paperId - 论文 ID
     */
    async addToBookmarks(paperId) {
      try {
        const res = await addBookmark(paperId)
        if (res.code === 200) {
          this.bookmarkedIds.add(paperId)
        }
        return res
      } catch (e) {
        console.error('添加收藏失败', e)
        return { code: 500, msg: '操作失败', data: null }
      }
    },

    /**
     * 取消收藏
     * @param {string} paperId - 论文 ID
     */
    async removeFromBookmarks(paperId) {
      try {
        const res = await removeBookmark(paperId)
        if (res.code === 200) {
          this.bookmarkedIds.delete(paperId)
          // 从列表中移除
          this.bookmarks = this.bookmarks.filter(b => b.paper_id !== paperId)
        }
        return res
      } catch (e) {
        console.error('取消收藏失败', e)
        return { code: 500, msg: '操作失败', data: null }
      }
    },

    /**
     * 切换收藏状态
     * @param {string} paperId - 论文 ID
     */
    async toggleBookmark(paperId) {
      if (this.bookmarkedIds.has(paperId)) {
        return this.removeFromBookmarks(paperId)
      } else {
        return this.addToBookmarks(paperId)
      }
    },

    /**
     * 初始化收藏 ID 集合（从论文列表中提取）
     * @param {Array} papers - 论文列表
     */
    initFromPapers(papers) {
      papers.forEach(paper => {
        if (paper.is_bookmarked) {
          this.bookmarkedIds.add(paper.id)
        }
      })
    }
  }
})