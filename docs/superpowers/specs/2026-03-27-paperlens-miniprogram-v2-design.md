# PaperLens 微信小程序 V2 重构设计文档

---

| 字段 | 内容 |
|---|---|
| **项目名称** | PaperLens 小程序 V2 重构 |
| **版本** | V2.0 |
| **状态** | 已批准 |
| **创建日期** | 2026-03-27 |
| **设计风格** | Apple 极简风格 |

---

## 1. 项目概述

### 1.1 背景

现有小程序采用 GitHub 深色主题风格，与 V2 产品设计文档定义的 Apple 极简风格差异较大。需要根据 V2 设计文档进行全量重构。

### 1.2 目标

- 按照 V2 产品设计文档实现完整功能
- 采用 Apple 极简设计风格
- 支持浅色/深色模式
- 实现精选推荐、收藏/跳过、AI摘要、轻量问答等核心功能

### 1.3 参考资料

- 产品设计文档: `docs/miniprogram/v2-product-design.md`
- UI设计规范: `docs/miniprogram/v2-ui-design.md`
- 技术架构文档: `docs/miniprogram/v2-tech-architecture.md`

---

## 2. 项目结构

```
paperlens-uniapp/
├── App.vue                      # App 入口
├── main.js                      # 主入口
├── pages.json                   # 页面配置
├── manifest.json                # 应用配置
├── uni.scss                     # 全局样式变量
│
├── pages/                       # 页面
│   ├── home/
│   │   ├── index.vue            # 首页（精选/全部）
│   │   ├── search.vue           # 搜索页
│   │   └── detail.vue           # 论文详情
│   ├── profile/
│   │   ├── index.vue            # 我的
│   │   ├── bookmarks.vue        # 收藏夹
│   │   └── settings.vue         # 设置
│   └── auth/
│       ├── login.vue            # 登录
│       └── onboarding.vue       # 兴趣引导
│
├── components/                  # 组件
│   ├── PaperCard.vue            # 论文卡片
│   ├── SearchBar.vue            # 搜索框
│   ├── CategoryTag.vue          # 分类标签
│   ├── SegmentedControl.vue     # Tab 切换
│   ├── AISummary.vue            # AI摘要面板
│   └── ChatInput.vue            # 对话输入
│
├── stores/                      # Pinia 状态管理
│   ├── index.js
│   ├── user.js
│   ├── papers.js
│   ├── bookmarks.js
│   └── settings.js
│
├── api/                         # API 接口
│   ├── index.js
│   ├── client.js
│   ├── auth.js
│   ├── papers.js
│   ├── user.js
│   ├── chat.js
│   └── bookmarks.js
│
├── utils/                       # 工具函数
│   ├── storage.js
│   └── format.js
│
├── static/                      # 静态资源
│   └── icons/
│
└── styles/                      # 样式
    ├── variables.scss           # 设计系统变量
    └── common.scss              # 公共样式
```

---

## 3. 设计系统

### 3.1 色彩系统

**浅色模式**：
- 背景色: #FFFFFF
- 分组背景: #F2F2F7
- 卡片背景: #FFFFFF
- 主色: #007AFF (Apple Blue)
- 文字主色: #1D1D1F
- 文字次色: #86868B
- 文字辅助: #AEAEB2
- 分割线: #E5E5EA
- 成功色: #34C759
- 警告色: #FF9500
- 错误色: #FF3B30

**深色模式**（自动跟随系统）：
- 背景色: #000000
- 分组背景: #1C1C1E
- 卡片背景: #2C2C2E
- 主色: #0A84FF
- 文字主色: #FFFFFF
- 文字次色: #8E8E93
- 文字辅助: #636366
- 分割线: #38383A
- 成功色: #30D158
- 警告色: #FFD60A
- 错误色: #FF453A

### 3.2 字体系统

- 大标题 (Large Title): 34px / 700
- 标题一 (Title 1): 28px / 700
- 标题二 (Title 2): 22px / 700
- 标题三 (Title 3): 20px / 600
- 标题 (Headline): 17px / 600
- 正文 (Body): 17px / 400
- 次要正文 (Callout): 16px / 400
- 小标题 (Subheadline): 15px / 400
- 注释 (Footnote): 13px / 400
- 说明 (Caption): 12px / 400

### 3.3 间距系统

基础单位: 4px

- 4px: 微间距（图标与文字）
- 8px: 元素内间距
- 12px: 卡片内边距
- 16px: 页面边距
- 20px: 区块间距
- 24px: 大区块间距

### 3.4 圆角系统

- 小圆角: 8px（按钮、输入框、小卡片）
- 中圆角: 12px（论文卡片、列表项）
- 大圆角: 16px（弹窗、模态框）
- 全圆角: 999px（圆形头像、图标按钮）

---

## 4. 页面设计

### 4.1 首页

**功能**：
- 顶部搜索框（点击跳转搜索页）
- Tab 切换：精选 / 全部
- 精选 Tab：今日精选论文卡片流，每张卡片有 [收藏] [跳过] 按钮
- 全部 Tab：数据源筛选（arXiv/ACL/NeurIPS/ICML）+ 论文列表
- 下拉刷新、上拉加载

**状态**：
- `activeTab`: 'featured' | 'all'
- `papers`: 论文列表
- `loading`: 加载状态
- `selectedSource`: 数据源筛选

### 4.2 论文详情页

**功能**：
- 标题、作者、分类标签
- 原文摘要（可展开/收起）
- AI 摘要（默认收起，点击展开）
- 轻量问答输入框 + 快捷问题
- 底部操作栏：收藏 / 分享 / 打开原文

**状态**：
- `paper`: 论文详情
- `summaryExpanded`: AI摘要展开状态
- `isBookmarked`: 收藏状态

### 4.3 我的

**功能**：
- 用户头像、昵称、阅读统计
- 本周阅读统计（阅读篇数/收藏/跳过）
- 兴趣分布条形图
- 收藏夹入口
- 设置入口

### 4.4 设置页

**功能**：
- 兴趣方向选择（多选，1-5个）
- 每日推送数量（1-10篇）
- 推送设置（开关、时间选择）
- 模型配置 BYOK 入口
- 关于信息

### 4.5 登录页

**功能**：
- 微信一键登录按钮
- 登录成功后跳转兴趣引导页

### 4.6 兴趣引导页

**功能**：
- 选择感兴趣的方向（至少1个，最多5个）
- 开始使用按钮

---

## 5. 组件设计

### 5.1 PaperCard（论文卡片）

**Props**：
- `paper`: 论文数据对象
- `showActions`: 是否显示收藏/跳过按钮

**Events**：
- `@bookmark`: 收藏事件
- `@skip`: 跳过事件
- `@tap`: 点击卡片

**样式**：12px 圆角，16px 内边距，标题 17px/600，摘要预览 2 行截断

### 5.2 SearchBar（搜索框）

**Props**：
- `placeholder`: 占位文本
- `value`: 输入值

**Events**：
- `@input`: 输入事件
- `@submit`: 提交搜索

**样式**：40px 高度，10px 圆角，分组背景色

### 5.3 CategoryTag（分类标签）

**Props**：
- `text`: 标签文本
- `active`: 是否激活

**Events**：
- `@tap`: 点击事件

**样式**：24px 高度，主色 10% 透明度背景，6px 圆角

### 5.4 SegmentedControl（Tab 切换）

**Props**：
- `options`: 选项数组 `[{value, label}]`
- `value`: 当前选中值

**Events**：
- `@change`: 切换事件

**样式**：32px 高度，8px 圆角，激活背景为卡片背景色

### 5.5 AISummary（AI摘要面板）

**Props**：
- `summary`: 摘要数据 `{what, how, why}`
- `status`: 状态（pending/processing/done/failed）

**Events**：
- `@retry`: 重试生成

**样式**：可折叠面板，展开显示 What/How/Why 三段

### 5.6 ChatInput（对话输入）

**Props**：
- `placeholder`: 占位文本
- `quickQuestions`: 快捷问题数组

**Events**：
- `@send`: 发送消息
- `@quickQuestion`: 点击快捷问题

**样式**：输入框 + 发送按钮 + 快捷问题标签

---

## 6. 状态管理设计

### 6.1 用户状态 (stores/user.js)

```js
state: {
  token: null,
  userInfo: { id, nickname, avatar_url },
  isNewUser: false
}
actions: {
  login(), logout(), fetchUserInfo()
}
```

### 6.2 论文状态 (stores/papers.js)

```js
state: {
  featuredPapers: [],      // 今日精选
  allPapers: [],           // 全部论文
  currentPaper: null,      // 详情页当前论文
  loading: false
}
actions: {
  fetchFeaturedPapers(), fetchAllPapers(), fetchPaperDetail()
}
```

### 6.3 收藏状态 (stores/bookmarks.js)

```js
state: {
  bookmarks: [],
  bookmarkedIds: new Set()  // 快速判断是否已收藏
}
actions: {
  fetchBookmarks(), addBookmark(), removeBookmark()
}
```

### 6.4 设置状态 (stores/settings.js)

```js
state: {
  categories: [],          // 兴趣方向
  dailyCount: 5,           // 每日推送数量
  pushEnabled: true,
  pushTime: '08:00'
}
actions: {
  fetchSettings(), updateSettings()
}
```

---

## 7. API 接口封装

| 模块 | 方法 | 接口 |
|------|------|------|
| 认证 | `wxLogin(code)` | POST /auth/wx-login |
| 论文 | `getTodayPapers()` | GET /papers/today |
| 论文 | `getPapers(params)` | GET /papers |
| 论文 | `getPaper(id)` | GET /papers/{id} |
| 论文 | `searchPapers(q)` | GET /papers/search |
| 用户 | `getUserInfo()` | GET /users/me |
| 用户 | `getUserStats()` | GET /users/stats |
| 偏好 | `getPreferences()` | GET /preferences |
| 偏好 | `updatePreferences(data)` | PUT /preferences |
| 收藏 | `getBookmarks()` | GET /bookmarks |
| 收藏 | `addBookmark(paperId)` | POST /bookmarks/{id} |
| 收藏 | `removeBookmark(paperId)` | DELETE /bookmarks/{id} |
| 行为 | `skipPaper(paperId)` | POST /actions/skip/{id} |
| AI | `chatPaper(paperId, question)` | POST /chat/paper/{id} |
| AI | `getSummary(paperId)` | GET /summary/{id} |

---

## 8. 开发阶段

### 阶段一：基础框架
1. 项目初始化（pages.json、manifest.json、App.vue）
2. 设计系统（variables.scss、common.scss）
3. API 客户端和接口封装
4. Pinia stores 基础结构

### 阶段二：核心组件
1. PaperCard 论文卡片
2. SearchBar 搜索框
3. CategoryTag 分类标签
4. SegmentedControl Tab 切换

### 阶段三：主要页面
1. 首页（精选/全部 Tab）
2. 论文详情页
3. 我的页面
4. 设置页面

### 阶段四：功能完善
1. 搜索页
2. 收藏夹页面
3. 登录页 + 兴趣引导页
4. AISummary 和 ChatInput 组件

### 阶段五：优化完善
1. 下拉刷新、上拉加载
2. 加载状态、空状态、错误状态
3. 动效和触觉反馈
4. 深色模式适配

---

*本文档为 PaperLens 微信小程序 V2 重构设计文档，基于 2026-03-27 讨论定稿。*