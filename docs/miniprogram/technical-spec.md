# PaperLens 微信小程序技术规范

---

| 字段 | 内容 |
|---|---|
| **文档版本** | V1.0 |
| **状态** | 草稿 |
| **最后更新** | 2026-03-26 |
| **目标读者** | 小程序开发者、代码审查者、后续贡献者 |

---

## 0. 文档元信息

### 0.1 目的

本文档定义 PaperLens 微信小程序 V1.0 的技术实现规范，指导开发团队完成高质量代码交付。

### 0.2 与 PRD 的关系

- **PRD**（`docs/product/PRD.md`）：定义产品"做什么"和"为什么做"
- **本规范**：定义"如何实现"，包括架构设计、代码规范、接口契约等

### 0.3 版本追踪

| 版本 | 日期 | 变更内容 |
|---|---|---|
| 1.0 | 2026-03-26 | 初始版本 |

---

## 1. 项目概述

### 1.1 产品背景

PaperLens 是一个 arXiv 论文聚合 + AI 增强阅读工具。微信小程序是 V1.0 的主要客户端，面向碎片化阅读场景（通勤、等待、休息时间）。

**核心用户场景**：
- 打开小程序 → 浏览今日 arXiv 新论文 → 点击感兴趣的论文 → 查看 AI 三段式摘要 → 复制原文链接/PDF 链接

### 1.2 技术栈

| 层级 | 技术选型 | 说明 |
|---|---|---|
| **运行时** | uni-app（Vue 3） | Vue 语法、多端支持、社区成熟 |
| **后端通信** | `uni.request` + REST API | 基于 FastAPI 后端 |
| **认证** | 微信 OAuth + JWT Token | 存储于 Storage |
| **UI 组件库** | 无（V1.0 使用原生组件） | 避免第三方依赖，减少包体积 |

> **注意**：原计划使用微信小程序原生框架，已于 2026-03-27 改为 uni-app（Vue 3）。详见 [ADR-002](../adr/002-native-miniprogram.md)。

### 1.3 小程序配置

#### pages.json 关键配置

```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": { "navigationBarTitleText": "今日论文" }
    },
    {
      "path": "pages/detail/detail",
      "style": { "navigationBarTitleText": "论文详情" }
    },
    {
      "path": "pages/settings/settings",
      "style": { "navigationBarTitleText": "设置" }
    }
  ],
  "globalStyle": {
    "navigationBarBackgroundColor": "#0d1117",
    "navigationBarTextStyle": "white",
    "navigationBarTitleText": "PaperLens",
    "backgroundColor": "#0d1117"
  },
  "tabBar": {
    "list": [
      { "pagePath": "pages/index/index", "text": "今日论文" },
      { "pagePath": "pages/settings/settings", "text": "设置" }
    ],
    "backgroundColor": "#0d1117",
    "selectedColor": "#58a6ff"
  }
}
```

#### 所需权限

- `uni.login`：微信登录
- `uni.request`：网络请求（需配置合法域名）
- `uni.setClipboardData`：复制链接到剪贴板

### 1.4 开发环境搭建

#### 前置要求

- HBuilderX >= 3.8.0
- 微信开发者工具 >= 1.06.2307260
- 后端服务已启动（本地或远程）

#### 本地开发配置

1. 使用 HBuilderX 打开 `paperlens-uniapp/` 目录
2. 运行 → 运行到小程序模拟器 → 微信开发者工具
3. 在微信开发者工具中勾选"不校验合法域名"
4. 修改 `api/client.js` 中的 `BASE_URL` 为本地后端地址

#### 环境切换策略

```javascript
// api/client.js
const BASE_URL = 'https://api.paperlens.io/api/v1';  // 生产环境
// const BASE_URL = 'http://localhost:8000/api/v1';  // 开发环境（注释切换）
```

---

## 2. 文件结构与命名规范

### 2.1 目录结构

```
paperlens-uniapp/
├── App.vue                # App 生命周期、全局状态
├── main.js                # 应用入口
├── pages.json             # 页面注册、tabBar、window 配置
├── manifest.json          # 应用配置
├── uni.scss               # 全局样式变量
├── api/
│   ├── client.js          # uni.request 封装、Token 注入
│   ├── papers.js          # 论文相关 API
│   ├── auth.js            # 认证 API
│   └── settings.js        # 设置 API
├── stores/
│   └── user.js            # 用户状态管理
├── pages/
│   ├── index/             # 论文列表页（tabBar）
│   │   └── index.vue
│   ├── detail/            # 论文详情页
│   │   └── detail.vue
│   └── settings/          # 设置页（tabBar）
│       └── settings.vue
└── static/                # 静态资源
```

### 2.2 命名规范

| 类型 | 规范 | 示例 |
|---|---|---|
| 页面目录 | `kebab-case`，与路由一致 | `pages/detail/detail` |
| Vue 组件 | `PascalCase` | `PaperCard.vue` |
| JS 变量/函数 | `camelCase` | `getPapers`, `activeCategory` |
| CSS class | `kebab-case` | `paper-card`, `summary-section` |
| `data-*` 属性 | 小写，单词用连字符 | `data-id`, `data-cat` |
| API 模块导出 | 命名导出，不用 default | `export function getPapers() {}` |

### 2.3 页面注册顺序

`pages.json` 中 `pages` 数组的第一个页面为启动页：

```json
{
  "pages": [
    {
      "path": "pages/index/index",      // 启动页
      "style": { "navigationBarTitleText": "今日论文" }
    },
    {
      "path": "pages/detail/detail",
      "style": { "navigationBarTitleText": "论文详情" }
    },
    {
      "path": "pages/settings/settings",
      "style": { "navigationBarTitleText": "设置" }
    }
  ]
}
```

---

## 3. 全局状态与 App 生命周期

### 3.1 用户状态管理

```javascript
// stores/user.js
import { wxLogin } from '../api/auth'

const userStore = {
  state: {
    token: null,    // string | null — JWT Token
    userId: null,   // number | null — 用户 ID
  },

  init() {
    // 从 Storage 恢复 Token
    this.state.token = uni.getStorageSync('token') || null
    this.state.userId = uni.getStorageSync('userId') || null
  },

  setToken(token, userId) {
    this.state.token = token
    this.state.userId = userId
    uni.setStorageSync('token', token)
    uni.setStorageSync('userId', userId)
  },

  clear() {
    this.state.token = null
    this.state.userId = null
    uni.removeStorageSync('token')
    uni.removeStorageSync('userId')
  },

  async performWxLogin() {
    return new Promise((resolve, reject) => {
      uni.login({
        success: (res) => {
          const code = res.code
          // 调用后端登录接口
          wxLogin(code).then((loginRes) => {
            if (loginRes.code === 200 && loginRes.data) {
              this.setToken(loginRes.data.token, loginRes.data.user_id)
              resolve(true)
            } else {
              resolve(false)
            }
          })
        },
        fail: () => resolve(false)
      })
    })
  }
}

export default userStore
```

### 3.2 App.vue 入口

```vue
<script>
import userStore from './stores/user.js'

export default {
  onLaunch() {
    // 初始化用户状态
    userStore.init()
  }
}
</script>

<style>
page {
  background-color: #0d1117;
  color: #e6edf3;
}
</style>
```

### 3.3 Token 持久化

- **存储**：`uni.setStorageSync('token', token)`
- **读取**：`uni.getStorageSync('token')`
- **清除**：`uni.removeStorageSync('token')`

### 3.4 已知限制（V1）

- 无 Token 过期检测（依赖后端返回 401）
- 无 Token 刷新机制（V1.1 补充）
- 无显式登出按钮（V1.1 补充）

---

## 4. API 集成层

### 4.1 api/client.js — 请求封装

```javascript
// api/client.js
const BASE_URL = 'https://api.paperlens.io/api/v1';

/**
 * 封装 uni.request
 * @param {string} url - 相对路径（不含 BASE_URL）
 * @param {object} options - uni.request 参数
 * @returns {Promise} - 返回 res.data（含 {code, msg, data}）
 */
export function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token');

    uni.request({
      url: `${BASE_URL}${url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.header,
      },
      success: (res) => {
        resolve(res.data);  // 返回完整响应体 {code, msg, data}
      },
      fail: reject,
    });
  });
}
```

**设计要点**：
- `BASE_URL` 是唯一配置后端地址的地方
- 自动注入 `Authorization: Bearer <token>`
- **不**自动解包 `data` 字段，由调用方处理

### 4.2 统一响应格式

所有后端接口返回：

```json
{
  "code": 200,
  "msg": "success",
  "data": { ... }
}
```

**调用约定**：
- 判断成功：`res.code === 200`
- 错误提示：使用 `res.msg` 作为 Toast 内容

### 4.3 api/papers.js — 论文 API

```javascript
// api/papers.js
import { request } from './client';

/**
 * 获取今日论文
 */
export function getTodayPapers() {
  return request('/papers/today');
}

/**
 * 获取论文列表（支持筛选）
 * @param {object} params - { category?, q?, page?, size?, date? }
 */
export function getPapers(params = {}) {
  const query = Object.entries(params)
    .filter(([, v]) => v)  // 过滤 falsy 值
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&');

  return request(`/papers${query ? '?' + query : ''}`);
}

/**
 * 获取论文详情
 * @param {string} id - 论文 ID（需 encodeURIComponent）
 */
export function getPaper(id) {
  return request(`/papers/${encodeURIComponent(id)}`);
}
```

### 4.4 V2 API 模块规划

```
api/
├── client.js       (V1)
├── papers.js       (V1)
├── auth.js         (V1)
├── settings.js     (V1)
├── ai.js           (V2 — SSE 流式摘要)
├── bookmarks.js    (V1.1 — 收藏)
└── ...
```

### 4.5 SSE 流式摘要设计（V2）

uni-app 微信小程序不原生支持 `EventSource`，V2 需采用以下方案之一：

- **方案 A**：`uni.request` + `responseType: 'text'` + 手动解析 SSE
- **方案 B**：云函数代理 SSE → WebSocket

**SSE 数据协议**：

```
data: {"section": "what", "delta": "这篇论文提出了..."}
data: {"section": "how", "delta": "作者采用了..."}
data: {"section": "why", "delta": "主要贡献在于..."}
data: [DONE]
```

---

## 5. 页面规范

### 5.1 pages/index — 论文列表

**路由**：`/pages/index/index`（tabBar 启动页）

#### 页面 Data 契约

```javascript
data: {
  papers: [],                    // Paper[]
  loading: false,                // boolean
  activeCategory: '',            // string — '' 表示"全部"
  categories: ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML'],
},
```

#### 生命周期

```javascript
onLoad() {
  this.fetchPapers();
},

onPullDownRefresh() {
  this.fetchPapers().finally(() => {
    uni.stopPullDownRefresh();
  });
},
```

#### 核心方法

```javascript
methods: {
  async fetchPapers() {
    this.loading = true;

    try {
      const { activeCategory } = this;
      let res;
      if (activeCategory && activeCategory !== '全部') {
        res = await getPapers({ category: activeCategory });
      } else {
        res = await getTodayPapers();
      }

      if (res.code === 200) {
        this.papers = res.data;
      } else {
        uni.showToast({ title: res.msg, icon: 'none' });
      }
    } catch (e) {
      uni.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      this.loading = false;
    }
  },

  onCategoryTap(e) {
    const cat = e.currentTarget.dataset.cat;
    this.activeCategory = cat;
    this.fetchPapers();
  },

  onPaperTap(e) {
    const id = e.currentTarget.dataset.id;
    uni.navigateTo({
      url: `/pages/detail/detail?id=${encodeURIComponent(id)}`,
    });
  },
}
```

#### Vue 模板结构

```html
<template>
  <view class="container">
    <!-- 分类筛选滚动条 -->
    <scroll-view class="categories" scroll-x>
      <view
        v-for="(item, index) in categories"
        :key="index"
        :class="['cat-tag', activeCategory === item ? 'active' : '']"
        :data-cat="item"
        @tap="onCategoryTap"
      >{{ item }}</view>
    </scroll-view>

    <!-- 加载状态 -->
    <view v-if="loading" class="loading">加载中...</view>

    <!-- 论文列表 -->
    <view v-else class="papers">
      <view
        v-for="paper in papers"
        :key="paper.id"
        class="paper-card"
        :data-id="paper.id"
        @tap="onPaperTap"
      >
        <view class="tags">
          <text
            v-for="(cat, catIndex) in paper.categories.slice(0, 2)"
            :key="catIndex"
            class="tag"
          >{{ cat }}</text>
        </view>
        <view class="title">{{ paper.title }}</view>
        <view class="authors">{{ paper.authors[0] }} 等</view>
        <view :class="['summary-status', paper.summary_status]">
          {{ paper.summary_status === 'done' ? 'AI 摘要已生成' : 'AI 摘要生成中' }}
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view v-if="!loading && papers.length === 0" class="empty">
      暂无论文
    </view>
  </view>
</template>
```

#### V2 扩展点

- **无限滚动**：`onReachBottom` + `page` 参数
- **搜索**：顶部搜索框 + `getPapers({ q })`
- **收藏图标**：卡片右上角心形图标（需 `api/bookmarks.js`）

---

### 5.2 pages/detail — 论文详情

**路由**：`/pages/detail/detail?id=<encodedId>`（navigateTo）

#### 页面 Data 契约

```javascript
data: {
  paper: null,                   // Paper | null
  summary: {                     // 从 paper 提取
    what: '',
    how: '',
    why: '',
  },
  generating: false,             // V2 预留：on-demand 触发生成
},
```

#### 生命周期

```javascript
onLoad(options) {
  const id = decodeURIComponent(options.id);
  this.loadPaper(id);
},

loadPaper(id) {
  getPaper(id)
    .then((res) => {
      if (res.code === 200) {
        const paper = res.data;
        const summary = {
          what: paper.summary_what || '',
          how: paper.summary_how || '',
          why: paper.summary_why || '',
        };
        this.setData({ paper, summary });
      } else {
        wx.showToast({ title: res.msg, icon: 'error' });
      }
    })
    .catch(() => {
      wx.showToast({ title: '加载失败', icon: 'error' });
    });
},
```

#### 核心方法

```javascript
openArxiv() {
  const { paper } = this.data;
  wx.setClipboardData({
    data: paper.url,
    success: () => {
      wx.showToast({ title: '链接已复制', icon: 'success' });
    },
  });
},

openPdf() {
  const { paper } = this.data;
  wx.setClipboardData({
    data: paper.pdf_url,
    success: () => {
      wx.showToast({ title: 'PDF 链接已复制，请在浏览器打开', icon: 'none' });
    },
  });
},

speakSummary() {
  // V1：复制摘要文本
  // V2：替换为 TTS 播放
  const { summary } = this.data;
  const text = `What: ${summary.what}\n\nHow: ${summary.how}\n\nWhy: ${summary.why}`;
  wx.setClipboardData({
    data: text,
    success: () => {
      wx.showToast({ title: '摘要已复制', icon: 'success' });
    },
  });
},
```

#### 摘要状态展示逻辑

| `summary_status` | UI 表现 |
|---|---|
| `done` | 展示三段式摘要 + AI 免责声明 |
| `processing` | 展示"AI 摘要生成中..."（V1.1 优化为进度条） |
| `pending` / `failed` | 展示"暂无 AI 摘要，将在后台自动生成" |

#### WXML 结构

```xml
<view class="container" wx:if="{{paper}}">
  <!-- 标题与作者 -->
  <view class="title">{{paper.title}}</view>
  <view class="authors">{{paper.authors.join(', ')}}</view>

  <!-- 分类标签 -->
  <view class="tags">
    <text wx:for="{{paper.categories}}" wx:key="*this" class="tag">{{item}}</text>
  </view>

  <!-- 操作按钮 -->
  <view class="action-btns">
    <button class="btn-secondary" bindtap="openArxiv">复制原文链接</button>
    <button class="btn-primary" bindtap="openPdf">打开 PDF</button>
  </view>

  <!-- AI 摘要区域 -->
  <view class="summary-section">
    <view class="section-title">AI 结构化摘要</view>

    <view wx:if="{{paper.summary_status === 'done'}}">
      <view class="summary-item">
        <view class="label">What（解决了什么问题）</view>
        <view class="content">{{summary.what}}</view>
      </view>
      <view class="summary-item">
        <view class="label">How（采用了什么方法）</view>
        <view class="content">{{summary.how}}</view>
      </view>
      <view class="summary-item">
        <view class="label">Why（主要贡献）</view>
        <view class="content">{{summary.why}}</view>
      </view>

      <view class="disclaimer">内容由 AI 生成，请以原文为准</view>

      <button class="btn-ghost" bindtap="speakSummary">复制摘要文本</button>
    </view>

    <view wx:elif="{{paper.summary_status === 'processing'}}" class="empty">
      AI 摘要生成中...
    </view>

    <view wx:else class="empty">
      暂无 AI 摘要，将在后台自动生成
    </view>
  </view>

  <!-- 原始摘要 -->
  <view class="abstract-section">
    <view class="section-title">原始摘要（英文）</view>
    <view class="abstract-text">{{paper.abstract}}</view>
  </view>
</view>
```

#### V2 扩展点

- **SSE 流式摘要**：`generating` 状态 + 实时渲染 delta
- **TTS 播放**：`speakSummary()` 改为调用音频播放
- **收藏按钮**：`action-btns` 中添加心形图标
- **RAG Chat**：底部可展开聊天面板

---

### 5.3 pages/settings — BYOK 配置

**路由**：`/pages/settings/settings`（tabBar）

#### 页面 Data 契约

```javascript
data: {
  form: {
    llm_base_url: '',          // string
    llm_model_name: '',        // string
    llm_api_key: '',           // string — write-only
    language: 'zh',            // 'zh' | 'en'
  },
  apiKeySet: false,            // boolean — 后端返回 llm_api_key_set
  testing: false,              // boolean — 按钮加载状态
},
```

#### 生命周期

```javascript
onLoad() {
  this.loadSettings();
},

loadSettings() {
  request('/settings')
    .then((res) => {
      if (res.code === 200) {
        const data = res.data;
        this.setData({
          'form.llm_base_url': data.llm_base_url || '',
          'form.llm_model_name': data.llm_model_name || '',
          'form.language': data.language || 'zh',
          apiKeySet: data.llm_api_key_set || false,
        });
      }
    })
    .catch(() => {
      // 未登录或加载失败，静默处理
    });
},
```

#### 核心方法

```javascript
onInput(e) {
  const key = e.currentTarget.dataset.key;
  const value = e.detail.value;
  this.setData({
    [`form.${key}`]: value,
  });
},

testLLM() {
  this.setData({ testing: true });

  request('/settings/test-llm', { method: 'POST' })
    .then((res) => {
      wx.showToast({ title: res.msg, icon: res.code === 200 ? 'success' : 'error' });
    })
    .catch(() => {
      wx.showToast({ title: '测试失败', icon: 'error' });
    })
    .finally(() => {
      this.setData({ testing: false });
    });
},

save() {
  const { form } = this.data;
  const payload = { ...form };

  // 空 API Key 不发送（保留服务端已存储的密钥）
  if (!payload.llm_api_key) {
    delete payload.llm_api_key;
  }

  request('/settings', {
    method: 'PUT',
    data: payload,
  })
    .then((res) => {
      if (res.code === 200) {
        wx.showToast({ title: '保存成功', icon: 'success' });
        if (payload.llm_api_key) {
          this.setData({ apiKeySet: true });
        }
      } else {
        wx.showToast({ title: res.msg, icon: 'error' });
      }
    })
    .catch(() => {
      wx.showToast({ title: '保存失败', icon: 'error' });
    });
},
```

#### 表单字段说明

| 字段 | 输入类型 | Placeholder | 说明 |
|---|---|---|---|
| `llm_base_url` | text | `https://api.openai.com/v1` | API Base URL |
| `llm_model_name` | text | `gpt-4o-mini` | 模型名称 |
| `llm_api_key` | password | "已设置" 或 "输入 API Key" | 密钥，永不回填 |

**空 API Key 处理规则**：
- 如果用户未填写 `llm_api_key`，提交时删除该字段
- 这保留了服务端已加密存储的密钥，避免误覆盖

#### WXML 结构

```xml
<view class="container">
  <view class="section">
    <view class="section-title">大模型配置（BYOK）</view>

    <view class="form-item">
      <view class="label">API Base URL</view>
      <input
        class="input"
        value="{{form.llm_base_url}}"
        data-key="llm_base_url"
        bindinput="onInput"
        placeholder="https://api.openai.com/v1"
      />
    </view>

    <view class="form-item">
      <view class="label">模型名称</view>
      <input
        class="input"
        value="{{form.llm_model_name}}"
        data-key="llm_model_name"
        bindinput="onInput"
        placeholder="gpt-4o-mini"
      />
    </view>

    <view class="form-item">
      <view class="label">API Key</view>
      <input
        class="input"
        type="password"
        value="{{form.llm_api_key}}"
        data-key="llm_api_key"
        bindinput="onInput"
        placeholder="{{apiKeySet ? '已设置（留空不修改）' : '输入 API Key'}}"
      />
    </view>

    <view class="hint">支持 OpenAI、DeepSeek、本地 Ollama 等兼容 OpenAI 协议的模型</view>

    <button class="btn-ghost" loading="{{testing}}" bindtap="testLLM">测试连通性</button>
  </view>

  <button class="btn-primary save-btn" bindtap="save">保存设置</button>
</view>
```

#### 安全说明

- API Key 通过 HTTPS 传输
- 服务端使用 AES-256-GCM 加密存储
- 客户端永不存储明文 Key（仅 Storage 中存 Token）
- 后端返回 `llm_api_key_set` 布尔值，不返回密钥原文

#### V2 扩展点

- **偏好分类订阅**：`preferred_categories` 多选芯片
- **每日推送开关**：`daily_digest` 开关
- **语言切换**：`language` 下拉选择

---

## 6. 组件规范

V1.0 组件目录为占位符，V1.1 在出现复用时促进为组件。

### 6.1 components/paper-card

**促进时机**：当 `index.wxml` 卡片标记超过 ~25 行或需要复用（如收藏页）

#### Properties

```javascript
properties: {
  paper: { type: Object, value: null },
  // V2: bookmarked: { type: Boolean, value: false },
},
```

#### Events

```javascript
// 触发 tap 事件，detail 为 { id }
this.triggerEvent('tap', { id: this.properties.paper.id });
```

### 6.2 components/summary-panel

**促进时机**：当摘要展示需要复用或 SSE 流式渲染逻辑复杂时

#### Properties

```javascript
properties: {
  summary: {
    type: Object,
    value: { what: '', how: '', why: '' },
  },
  status: {  // 'pending' | 'processing' | 'done' | 'failed'
    type: String,
    value: 'pending',
  },
},
```

#### Events

```javascript
// 用户点击复制/TTS 按钮
this.triggerEvent('speak');
```

---

## 7. UI 设计系统

### 7.1 色彩 Token

| Token | Hex | 用途 |
|---|---|---|
| `color-bg-base` | `#0d1117` | 页面背景 |
| `color-bg-card` | `#161b22` | 卡片/区块背景 |
| `color-bg-input` | `#0d1117` | 输入框背景 |
| `color-border` | `#30363d` | 边框（输入框、按钮） |
| `color-text-primary` | `#e6edf3` | 标题、正文 |
| `color-text-secondary` | `#c9d1d9` | 摘要正文 |
| `color-text-muted` | `#8b949e` | 作者、标签、提示 |
| `color-accent` | `#58a6ff` | 激活状态、主按钮、链接 |
| `color-accent-bg` | `#1f4168` | 标签背景、激活分类背景 |
| `color-success` | `#3fb950` | 摘要状态"已生成" |

### 7.2 字号规范

| 用途 | 字号 | 字重 | 颜色 |
|---|---|---|---|
| 论文标题（详情） | 16px | 600 | `color-text-primary` |
| 论文标题（卡片） | 14px | 400 | `color-text-primary` |
| 正文 / 摘要 | 14px | 400 | `color-text-secondary` |
| 作者、标签、提示 | 12px | 400 | `color-text-muted` |
| 标签、状态徽章 | 11px | 400 | `color-accent` |

### 7.3 间距与圆角

| 元素 | 值 |
|---|---|
| 页面内边距 | 12px（列表），16px（详情/设置） |
| 卡片圆角 | 12px |
| 输入框圆角 | 8px |
| 按钮圆角 | 8px（次级），10px（主按钮） |
| 卡片间距 | 12px |
| 区块间距 | 16px |

### 7.4 按钮变体

| 类名 | 背景 | 文字 | 边框 | 用途 |
|---|---|---|---|---|
| `.btn-primary` | `#58a6ff` | `#0d1117` | 无 | 主操作（PDF、保存） |
| `.btn-secondary` | `#21262d` | `#e6edf3` | 无 | 次操作（复制链接） |
| `.btn-ghost` | transparent | `#8b949e` | `1px solid #30363d` | 低优先级（测试、复制文本） |

### 7.5 分类标签样式

| 状态 | 背景 | 文字 |
|---|---|---|
| 默认（滚动芯片） | `#161b22` | `#8b949e` |
| 激活（滚动芯片） | `#1f4168` | `#58a6ff` |
| 内联标签 | `#1f4168` | `#58a6ff` |

---

## 8. 页面路由与导航

### 8.1 路由表

| 页面 | 路径 | 入口方式 | 可返回 |
|---|---|---|---|
| 论文列表 | `/pages/index/index` | tabBar / 启动 | N/A |
| 论文详情 | `/pages/detail/detail` | `wx.navigateTo` | 是 |
| 设置 | `/pages/settings/settings` | tabBar | N/A |

### 8.2 路由参数协议

- **论文 ID**：`?id=<encodeURIComponent(id)>`
- **PDF URL**：`?url=<encodeURIComponent(url)>`（V2）

**约定**：
- 只传 ID，不传复杂对象
- 目标页面 `onLoad` 中解码：`decodeURIComponent(options.id)`

### 8.3 导航规则

- **tabBar 页面**：点击 tabBar 切换（无需代码）
- **非 tabBar 页面**：使用 `uni.navigateTo`（产生返回箭头）
- **禁止使用** `uni.redirectTo`（会移除返回能力）

### 8.4 V2 tabBar 扩展计划

V1.1 添加"收藏"页，tabBar 扩展为三项：

```json
{
  "tabBar": {
    "list": [
      { "pagePath": "pages/index/index", "text": "今日论文" },
      { "pagePath": "pages/bookmarks/bookmarks", "text": "收藏" },
      { "pagePath": "pages/settings/settings", "text": "设置" }
    ]
  }
}
```

---

## 9. 认证与登录流程

### 9.1 登录时序图

```
用户进入需要认证的功能
        │
        ▼
页面调用 userStore.performWxLogin()
        │
        ├── uni.login() ──► 微信服务器 ──► 返回 { code }
        │
        ├── POST /api/v1/auth/wx-login { code }
        │       │
        │       ▼
        │   后端：code → openid
        │        → 查找或创建 User
        │        → 签发 JWT（7 天有效期）
        │        → 返回 { token, user_id }
        │
        ├── 存储 token 到 state + Storage
        │
        └── resolve(true) ──► 调用方继续执行
```

### 9.2 鉴权需求矩阵

| 页面/接口 | 需登录 | 匿名行为 |
|---|---|---|
| index（论文列表） | 否 | 完全可用 |
| detail（论文详情） | 否 | 摘要可用（若已生成） |
| settings（BYOK） | 是（软） | 无 Token 时表单留空，保存静默失败 |
| 收藏功能（V1.1） | 是 | 提示登录 |

### 9.3 Token 过期处理

V1 不主动检测 Token 过期，依赖后端返回 401。

**V1.1 补充**：
- 在 `api/client.js` 中添加响应拦截
- 检测 `code === 401` 时清除 Token 并重新登录

---

## 10. BYOK 配置流程

### 10.1 数据流

```
用户填写：base_url + model_name + api_key
        │
        ▼
save() → PUT /api/v1/settings { ... }
            │
            ▼
        后端加密 api_key（AES-256-GCM）
        存储密文到 user_settings.llm_api_key_enc
        返回成功（永不返回明文 Key）
            │
            ▼
        GET /api/v1/settings 返回 { llm_api_key_set: true, ... }
            │
            ▼
        apiKeySet = true → Input placeholder 显示"已设置"
```

### 10.2 空 Key 处理

```javascript
const payload = { ...form };
if (!payload.llm_api_key) {
  delete payload.llm_api_key;  // 保留服务端已存储的密钥
}
```

### 10.3 支持的后端

提示文案："支持 OpenAI、DeepSeek、本地 Ollama 等兼容 OpenAI 协议的模型"

小程序无需判断后端类型，只发送三个字段即可。

### 10.4 连通性测试

```javascript
request('/settings/test-llm', { method: 'POST' })
  .then(res => {
    wx.showToast({ title: res.msg, icon: ... });
  });
```

后端会尝试调用配置的 LLM（`max_tokens=5`）并返回成功/失败消息。

---

## 11. 错误处理与加载状态

### 11.1 Toast 规范

- **成功**：`uni.showToast({ title: '操作成功', icon: 'success' })`
- **失败**：`uni.showToast({ title: res.msg, icon: 'none' })`
- **提示**：`uni.showToast({ title: '提示文本', icon: 'none' })`

**避免使用 `uni.showModal`** 用于常规错误（侵入性强）。

### 11.2 Loading 状态清单

| 页面/操作 | 状态变量 | UI 表现 |
|---|---|---|
| 论文列表加载 | `loading` | `<view wx:if="{{loading}}">加载中...</view>` |
| LLM 连通性测试 | `testing` | `<button loading="{{testing}}">` |
| 摘要生成（V2） | `generating` | Spinner + 流式文字 |

### 11.3 空状态 UI

| 场景 | UI |
|---|---|
| 论文列表为空 | `<view class="empty">暂无论文</view>` |
| 摘要未生成 | `<view class="empty">暂无 AI 摘要，将在后台自动生成</view>` |
| 设置未配置 | 空输入框（可接受） |

### 11.4 V1 已知未处理错误

| 位置 | 问题 | 优先级 |
|---|---|---|
| `pages/index/index.vue` onCategoryTap | 分类筛选失败静默 | 中 |
| `pages/settings/settings.vue` onLoad | 无 Token 时不提示 | 中 |
| `pages/detail/detail.vue` openPdf | 复制后提示不够明显 | 低 |

---

## 12. V2 扩展路线图

| 功能 | V1 插入点 | 实现说明 |
|---|---|---|
| SSE 流式摘要 | `pages/detail/detail.vue` generating 状态 | `uni.request` + 手动解析 SSE 或云函数代理 |
| TTS 播放 | `pages/detail/detail.vue` speakSummary() | `uni.createInnerAudioContext` + 后端 TTS 接口 |
| 收藏 | 新增 `api/bookmarks.js`、`pages/bookmarks` | 后端接口已存在，需登录 |
| 搜索 | `pages/index` 顶部搜索框 | `getPapers({ q })` 已支持 |
| 偏好分类 | `pages/settings` 多选芯片 | `preferred_categories` 字段已存在 |
| RAG Chat | 新页面或底部面板 | 需新后端接口 |

---

## 13. 已知问题与技术债

| 问题 | 位置 | 优先级 | 建议修复版本 |
|---|---|---|---|
| PDF 按钮无实际跳转 | `pages/detail/detail.vue` openPdf | 高 | V1.1 |
| 分类筛选错误静默 | `pages/index/index.vue` onCategoryTap | 中 | V1.1 |
| 设置页未登录不提示 | `pages/settings/settings.vue` onLoad | 中 | V1.1 |
| 无 401 拦截器 | `api/client.js` | 中 | V1.1 |
| 无 Token 过期检测 | `stores/user.js` | 中 | V1.1 |

---

*本文档随小程序版本同步更新。如有疑问，请提交 Issue 或 PR。*