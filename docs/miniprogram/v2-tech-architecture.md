# PaperLens 微信小程序技术架构文档 V2

---

| 字段 | 内容 |
|---|---|
| **文档版本** | V2.0 |
| **状态** | 已定稿 |
| **最后更新** | 2026-03-27 |
| **目标读者** | 小程序开发者、后端开发者 |

---

## 1. 技术选型

### 1.1 前端技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| **运行时** | uni-app (Vue 3) | Vue 语法、多端支持、社区成熟 |
| **状态管理** | Pinia | Vue 3 官方推荐 |
| **UI组件** | 原生组件 | 避免第三方依赖，减少包体积 |
| **网络请求** | uni.request | 封装统一拦截器 |
| **本地存储** | uni.storage | 存储 Token、用户偏好缓存 |

### 1.2 后端技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| **框架** | FastAPI | 自动 Swagger 文档，async 支持 |
| **ORM** | SQLAlchemy 2.0 | 支持 SQLite → PostgreSQL 切换 |
| **数据库** | PostgreSQL | 生产环境 |
| **缓存** | Redis | 推荐结果缓存、会话管理 |
| **定时任务** | APScheduler | 每日论文抓取、推荐计算 |
| **消息队列** | Celery (可选) | AI 摘要异步生成 |

### 1.3 AI 服务

| 服务 | 用途 | 实现 |
|------|------|------|
| LLM | AI 摘要生成、问答 | OpenAI / DeepSeek / 自定义 |
| Embedding | 论文向量表示 | text-embedding-ada-002 |
| 推荐 | 个性化推荐算法 | 协同过滤 + 内容匹配 |

---

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              客户端层                                    │
│  ┌─────────────────────┐              ┌─────────────────────┐          │
│  │    微信小程序        │              │      Web 端          │          │
│  │  uni-app (Vue 3)    │              │    Vue 3 + Vite     │          │
│  └──────────┬──────────┘              └──────────┬──────────┘          │
└─────────────┼─────────────────────────────────────┼────────────────────┘
              │                                     │
              └──────────────────┬──────────────────┘
                                 │ HTTPS / WSS
┌────────────────────────────────┼────────────────────────────────────────┐
│                         API 网关层                                       │
│  ┌─────────────────────────────┴─────────────────────────────┐          │
│  │                      Nginx                                 │          │
│  │         (反向代理 / SSL 终结 / 限流 / 负载均衡)             │          │
│  └─────────────────────────────┬─────────────────────────────┘          │
└────────────────────────────────┼────────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────┐
│                         服务层                                           │
│  ┌─────────────────────────────┴─────────────────────────────┐          │
│  │                     FastAPI 应用                           │          │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │          │
│  │  │ 论文服务    │ │ 用户服务    │ │ 推荐服务    │          │          │
│  │  └─────────────┘ └─────────────┘ └─────────────┘          │          │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │          │
│  │  │ AI 服务     │ │ 认证服务    │ │ 推送服务    │          │          │
│  │  └─────────────┘ └─────────────┘ └─────────────┘          │          │
│  └───────────────────────────────────────────────────────────┘          │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────┐
│                         数据层                                           │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │  PostgreSQL   │  │     Redis     │  │  对象存储     │               │
│  │  (主数据库)    │  │  (缓存/队列)   │  │  (PDF缓存)   │               │
│  └───────────────┘  └───────────────┘  └───────────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────┐
│                         外部服务                                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │  arXiv API    │  │   LLM API     │  │  微信 API     │               │
│  │  (论文数据)    │  │  (AI 服务)     │  │  (登录/推送)  │               │
│  └───────────────┘  └───────────────┘  └───────────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 小程序端架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          uni-app 小程序                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         页面层 (Pages)                           │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │   │
│  │  │  home   │  │  detail │  │ profile │  │ settings│            │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│  ┌─────────────────────────────────┴───────────────────────────────┐   │
│  │                         组件层 (Components)                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │PaperCard │  │SearchBar │  │ TabBar   │  │ AIChat   │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│  ┌─────────────────────────────────┴───────────────────────────────┐   │
│  │                         状态层 (Store)                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │  user    │  │  papers  │  │ bookmarks│  │ settings │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│  ┌─────────────────────────────────┴───────────────────────────────┐   │
│  │                         服务层 (Services)                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │ api/auth │  │api/papers│  │api/chat  │  │api/user  │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│  ┌─────────────────────────────────┴───────────────────────────────┐   │
│  │                         工具层 (Utils)                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │ request  │  │ storage  │  │  router  │  │  logger  │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 目录结构

### 3.1 小程序目录结构

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
│   │   ├── index.vue            # 首页
│   │   ├── search.vue           # 搜索页
│   │   └── detail.vue           # 论文详情
│   ├── profile/
│   │   ├── index.vue            # 我的
│   │   ├── bookmarks.vue        # 收藏夹
│   │   └── settings.vue         # 设置
│   └── auth/
│       └── login.vue            # 登录
│
├── components/                  # 组件
│   ├── PaperCard.vue            # 论文卡片
│   ├── SearchBar.vue            # 搜索框
│   ├── TabBar.vue               # 底部导航
│   ├── CategoryTag.vue          # 分类标签
│   ├── AISummary.vue            # AI摘要面板
│   └── ChatInput.vue            # 对话输入
│
├── stores/                      # 状态管理
│   ├── index.js                 # Store 入口
│   ├── user.js                  # 用户状态
│   ├── papers.js                # 论文状态
│   ├── bookmarks.js             # 收藏状态
│   └── settings.js              # 设置状态
│
├── api/                         # API 接口
│   ├── index.js                 # API 入口
│   ├── client.js                # 请求封装
│   ├── auth.js                  # 认证接口
│   ├── papers.js                # 论文接口
│   ├── user.js                  # 用户接口
│   ├── chat.js                  # 对话接口
│   └── bookmarks.js             # 收藏接口
│
├── utils/                       # 工具函数
│   ├── request.js               # 请求工具
│   ├── storage.js               # 存储工具
│   ├── router.js                # 路由工具
│   ├── format.js                # 格式化工具
│   └── logger.js                # 日志工具
│
├── static/                      # 静态资源
│   ├── images/                  # 图片
│   └── icons/                   # 图标
│
└── styles/                      # 样式
    ├── variables.scss           # 变量
    ├── mixins.scss              # 混入
    └── common.scss              # 公共样式
```

### 3.2 后端目录结构

```
paperlens-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI 入口
│   ├── config.py                # 配置
│   │
│   ├── api/                     # API 路由
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── papers.py        # 论文接口
│   │   │   ├── auth.py          # 认证接口
│   │   │   ├── user.py          # 用户接口
│   │   │   ├── chat.py          # 对话接口
│   │   │   ├── bookmarks.py     # 收藏接口
│   │   │   └── recommendations.py # 推荐接口
│   │   └── deps.py              # 依赖注入
│   │
│   ├── models/                  # 数据模型
│   │   ├── __init__.py
│   │   ├── paper.py             # 论文模型
│   │   ├── user.py              # 用户模型
│   │   ├── bookmark.py          # 收藏模型
│   │   ├── preference.py        # 偏好模型
│   │   └── chat.py              # 对话模型
│   │
│   ├── schemas/                 # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── paper.py
│   │   ├── user.py
│   │   ├── bookmark.py
│   │   └── chat.py
│   │
│   ├── services/                # 业务逻辑
│   │   ├── __init__.py
│   │   ├── paper_service.py     # 论文服务
│   │   ├── user_service.py      # 用户服务
│   │   ├── auth_service.py      # 认证服务
│   │   ├── bookmark_service.py  # 收藏服务
│   │   ├── chat_service.py      # 对话服务
│   │   ├── recommendation_service.py # 推荐服务
│   │   └── push_service.py      # 推送服务
│   │
│   ├── sources/                 # 数据源
│   │   ├── __init__.py
│   │   ├── base.py              # 基类
│   │   ├── arxiv.py             # arXiv
│   │   ├── acl.py               # ACL
│   │   └── neurips.py           # NeurIPS
│   │
│   ├── llm/                     # LLM 服务
│   │   ├── __init__.py
│   │   ├── base.py              # 基类
│   │   ├── openai_compatible.py # OpenAI 兼容
│   │   └── prompts.py           # Prompt 模板
│   │
│   └── utils/                   # 工具
│       ├── __init__.py
│       ├── security.py          # 安全工具
│       ├── cache.py             # 缓存工具
│       └── logger.py            # 日志工具
│
├── alembic/                     # 数据库迁移
│   ├── versions/
│   └── env.py
│
├── tests/                       # 测试
│   ├── __init__.py
│   ├── test_papers.py
│   ├── test_auth.py
│   └── test_recommendations.py
│
├── alembic.ini
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 4. 数据库设计

### 4.1 ER 图

```
┌─────────────────┐       ┌─────────────────┐
│     users       │       │     papers      │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ openid          │       │ title           │
│ nickname        │       │ authors (JSON)  │
│ avatar_url      │       │ abstract        │
│ created_at      │       │ categories(JSON)│
└────────┬────────┘       │ source          │
         │                │ published_at    │
         │                │ summary_*       │
         │                └────────┬────────┘
         │                         │
         │    ┌────────────────────┼────────────────────┐
         │    │                    │                    │
         │    ▼                    ▼                    ▼
┌────────┴────────┐    ┌─────────────────┐    ┌─────────────────┐
│    bookmarks    │    │  preferences    │    │  swipe_actions  │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ user_id (FK)    │    │ user_id (FK)    │    │ user_id (FK)    │
│ paper_id (FK)   │    │ categories(JSON)│    │ paper_id (FK)   │
│ created_at      │    │ keywords (JSON) │    │ action          │
└─────────────────┘    │ updated_at      │    │ created_at      │
                       └─────────────────┘    └─────────────────┘
```

### 4.2 表结构

#### papers 表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | VARCHAR(64) PK | 论文ID，如 `arxiv:1706.03762` |
| `title` | TEXT | 论文标题 |
| `authors` | JSON | 作者列表 |
| `abstract` | TEXT | 原文摘要 |
| `categories` | JSON | 分类列表 |
| `source` | VARCHAR(32) | 数据源 |
| `source_url` | VARCHAR(512) | 原文链接 |
| `pdf_url` | VARCHAR(512) | PDF链接 |
| `published_at` | TIMESTAMP | 发布时间 |
| `summary_what` | TEXT | AI摘要 - What |
| `summary_how` | TEXT | AI摘要 - How |
| `summary_why` | TEXT | AI摘要 - Why |
| `summary_status` | VARCHAR(16) | 摘要状态 |
| `embedding` | VECTOR(1536) | 论文向量 (可选) |
| `created_at` | TIMESTAMP | 入库时间 |

#### users 表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | 用户ID |
| `openid` | VARCHAR(128) UNIQUE | 微信openid |
| `unionid` | VARCHAR(128) | 微信unionid |
| `nickname` | VARCHAR(64) | 昵称 |
| `avatar_url` | VARCHAR(512) | 头像URL |
| `created_at` | TIMESTAMP | 注册时间 |
| `last_seen_at` | TIMESTAMP | 最后活跃时间 |

#### preferences 表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | ID |
| `user_id` | INTEGER FK | 用户ID |
| `categories` | JSON | 感兴趣的分类 |
| `daily_count` | INTEGER | 每日推送数量 |
| `push_enabled` | BOOLEAN | 是否开启推送 |
| `push_time` | TIME | 推送时间 |
| `llm_config` | JSON | BYOK配置 |
| `updated_at` | TIMESTAMP | 更新时间 |

#### swipe_actions 表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | ID |
| `user_id` | INTEGER FK | 用户ID |
| `paper_id` | VARCHAR(64) FK | 论文ID |
| `action` | VARCHAR(16) | `bookmark`/`skip` |
| `created_at` | TIMESTAMP | 操作时间 |

---

## 5. API 设计

### 5.1 接口概览

| 模块 | 方法 | 路径 | 说明 |
|------|------|------|------|
| **认证** | POST | `/api/v1/auth/wx-login` | 微信登录 |
| | POST | `/api/v1/auth/refresh` | 刷新Token |
| **论文** | GET | `/api/v1/papers/today` | 今日精选 |
| | GET | `/api/v1/papers` | 论文列表 |
| | GET | `/api/v1/papers/{id}` | 论文详情 |
| | GET | `/api/v1/papers/search` | 搜索论文 |
| **用户** | GET | `/api/v1/users/me` | 用户信息 |
| | GET | `/api/v1/users/stats` | 阅读统计 |
| **偏好** | GET | `/api/v1/preferences` | 获取偏好 |
| | PUT | `/api/v1/preferences` | 更新偏好 |
| **收藏** | GET | `/api/v1/bookmarks` | 收藏列表 |
| | POST | `/api/v1/bookmarks/{paper_id}` | 添加收藏 |
| | DELETE | `/api/v1/bookmarks/{paper_id}` | 取消收藏 |
| **行为** | POST | `/api/v1/actions/skip/{paper_id}` | 跳过论文 |
| **AI** | POST | `/api/v1/chat/paper/{paper_id}` | 论文问答 |
| | GET | `/api/v1/summary/{paper_id}` | 获取AI摘要 |
| | POST | `/api/v1/summary/{paper_id}/retry` | 重试生成摘要 |

### 5.2 接口详情

#### 微信登录

```
POST /api/v1/auth/wx-login

Request:
{
  "code": "wx.login()返回的code"
}

Response:
{
  "code": 200,
  "data": {
    "token": "jwt_token",
    "user": {
      "id": 1,
      "nickname": "微信用户",
      "avatar_url": "https://..."
    },
    "is_new_user": true
  }
}
```

#### 今日精选

```
GET /api/v1/papers/today

Headers:
  Authorization: Bearer <token>

Response:
{
  "code": 200,
  "data": {
    "date": "2026-03-27",
    "papers": [
      {
        "id": "arxiv:1706.03762",
        "title": "Attention Is All You Need",
        "authors": ["Vaswani", "Shazeer"],
        "abstract_preview": "这篇论文提出了...",
        "categories": ["cs.AI", "cs.CL"],
        "source": "arxiv",
        "published_at": "2017-06-12",
        "has_summary": true
      }
    ],
    "total": 5
  }
}
```

#### 论文详情

```
GET /api/v1/papers/{id}

Response:
{
  "code": 200,
  "data": {
    "id": "arxiv:1706.03762",
    "title": "Attention Is All You Need",
    "authors": ["Vaswani", "Shazeer", "Parmar"],
    "abstract": "The dominant sequence...",
    "categories": ["cs.AI", "cs.CL"],
    "source": "arxiv",
    "source_url": "https://arxiv.org/abs/1706.03762",
    "pdf_url": "https://arxiv.org/pdf/1706.03762",
    "published_at": "2017-06-12",
    "summary": {
      "status": "done",
      "what": "这篇论文提出了...",
      "how": "作者采用了...",
      "why": "主要贡献在于..."
    },
    "is_bookmarked": false
  }
}
```

#### 论文问答

```
POST /api/v1/chat/paper/{paper_id}

Request:
{
  "question": "这篇论文的核心贡献是什么？"
}

Response (SSE):
data: {"delta": "这篇论文的核心贡献是提出了Transformer架构..."}
data: {"delta": "它完全基于注意力机制..."}
data: [DONE]
```

#### 收藏/跳过

```
POST /api/v1/bookmarks/{paper_id}

Response:
{
  "code": 200,
  "data": {
    "bookmarked": true,
    "created_at": "2026-03-27T10:30:00Z"
  }
}

POST /api/v1/actions/skip/{paper_id}

Response:
{
  "code": 200,
  "data": {
    "skipped": true
  }
}
```

---

## 6. 推荐系统

### 6.1 推荐算法

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          推荐系统架构                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────┐                                                      │
│   │  用户行为    │  收藏/跳过/阅读时长/点击                              │
│   └──────┬──────┘                                                      │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      特征提取                                    │  │
│   │  • 分类偏好权重 (cs.AI: 0.85, cs.CL: 0.72...)                  │  │
│   │  • 关键词偏好向量                                                │  │
│   │  • 作者偏好                                                      │  │
│   │  • 时间偏好 (最新 vs 经典)                                       │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      候选生成                                    │  │
│   │  • 内容匹配: 论文向量与用户偏好向量相似度                        │  │
│   │  • 协同过滤: 相似用户喜欢的论文                                  │  │
│   │  • 热度推荐: 高引用/高讨论论文                                   │  │
│   │  • 探索推荐: 新领域论文 (避免信息茧房)                          │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      排序 & 过滤                                 │  │
│   │  • 多路召回融合 (权重: 内容40% + 协同30% + 热度15% + 探索15%)   │  │
│   │  • 去重 (已收藏/已跳过的论文降权)                               │  │
│   │  • 多样性保证 (每个分类最多N篇)                                  │  │
│   │  • 数量限制 (用户设置的上限，最多10篇)                          │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      推荐结果                                    │  │
│   │  每日精选论文列表                                                │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 推荐权重更新

```python
# 用户行为权重
ACTION_WEIGHTS = {
    'bookmark': 1.0,      # 收藏 = 强正向
    'skip': -0.5,         # 跳过 = 负向
    'view_detail': 0.3,   # 查看详情 = 弱正向
    'share': 0.8,         # 分享 = 强正向
}

def update_preference(user_id: int, paper_id: str, action: str):
    """更新用户偏好权重"""
    paper = get_paper(paper_id)
    weight = ACTION_WEIGHTS[action]

    # 更新分类权重
    for category in paper.categories:
        current = user.preferences.categories.get(category, 0.5)
        # 指数移动平均
        new_weight = current * 0.9 + weight * 0.1
        user.preferences.categories[category] = new_weight

    # 更新关键词权重
    keywords = extract_keywords(paper.abstract)
    for keyword in keywords:
        current = user.preferences.keywords.get(keyword, 0.5)
        new_weight = current * 0.9 + weight * 0.1
        user.preferences.keywords[keyword] = new_weight

    save_preferences(user)
```

### 6.3 冷启动策略

```python
def get_recommendations_for_new_user(user_id: int, selected_categories: List[str]):
    """新用户推荐策略"""
    # 1. 基于用户选择的分类，推荐热门论文
    papers = []

    for category in selected_categories:
        # 获取该分类下近期热门论文
        hot_papers = get_hot_papers(
            category=category,
            days=7,
            limit=3
        )
        papers.extend(hot_papers)

    # 2. 补充一些探索性论文
    explore_papers = get_explore_papers(
        exclude_categories=selected_categories,
        limit=2
    )
    papers.extend(explore_papers)

    # 3. 按热度排序
    papers.sort(key=lambda p: p.citation_count, reverse=True)

    return papers[:user.preferences.daily_count]
```

---

## 7. 微信集成

### 7.1 微信登录流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   小程序     │     │   后端      │     │   微信API   │     │   数据库    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       │ 1. wx.login()     │                   │                   │
       │ ─────────────────>│                   │                   │
       │    返回 code      │                   │                   │
       │ <─────────────────│                   │                   │
       │                   │                   │                   │
       │ 2. POST /auth/wx-login               │                   │
       │ ─────────────────>│                   │                   │
       │                   │ 3. code → openid  │                   │
       │                   │ ─────────────────>│                   │
       │                   │   返回 openid     │                   │
       │                   │ <─────────────────│                   │
       │                   │                   │                   │
       │                   │ 4. 查找/创建用户  │                   │
       │                   │ ─────────────────────────────────────>│
       │                   │        用户信息   │                   │
       │                   │ <─────────────────────────────────────│
       │                   │                   │                   │
       │ 5. 返回 JWT Token │                   │                   │
       │ <─────────────────│                   │                   │
       │                   │                   │                   │
```

### 7.2 推送服务

```python
# 服务号模板消息
async def send_template_message(openid: str, papers: List[Paper]):
    """发送服务号模板消息"""
    template_id = "YOUR_TEMPLATE_ID"

    data = {
        "touser": openid,
        "template_id": template_id,
        "url": "pages/home/index",
        "data": {
            "date": {"value": datetime.now().strftime("%Y年%m月%d日")},
            "count": {"value": str(len(papers))},
            "papers": {"value": "\n".join([p.title for p in papers[:3]])}
        }
    }

    response = await wechat_api.post("/message/template/send", json=data)
    return response

# 小程序订阅消息
async def send_subscribe_message(openid: str, papers: List[Paper]):
    """发送小程序订阅消息"""
    template_id = "YOUR_SUBSCRIBE_TEMPLATE_ID"

    data = {
        "touser": openid,
        "template_id": template_id,
        "page": "pages/home/index",
        "data": {
            "thing1": {"value": "今日论文精选"},
            "number2": {"value": str(len(papers))},
            "time3": {"value": datetime.now().strftime("%H:%M")}
        }
    }

    response = await wechat_api.post("/subscribeMessage/send", json=data)
    return response
```

---

## 8. 性能优化

### 8.1 缓存策略

```python
# Redis 缓存设计
CACHE_KEYS = {
    # 今日精选 (每日更新)
    "daily_papers:{user_id}": TTL(3600 * 24),

    # 论文详情
    "paper:{paper_id}": TTL(3600 * 24 * 7),

    # AI摘要
    "summary:{paper_id}": TTL(3600 * 24 * 30),

    # 用户偏好
    "preferences:{user_id}": TTL(3600 * 24),

    # 推荐结果
    "recommendations:{user_id}": TTL(3600 * 6),
}
```

### 8.2 请求优化

```javascript
// 小程序请求封装
class RequestQueue {
  constructor(maxConcurrent = 5) {
    this.queue = [];
    this.running = 0;
    this.maxConcurrent = maxConcurrent;
  }

  async request(options) {
    return new Promise((resolve, reject) => {
      this.queue.push({ options, resolve, reject });
      this.process();
    });
  }

  async process() {
    while (this.running < this.maxConcurrent && this.queue.length > 0) {
      const { options, resolve, reject } = this.queue.shift();
      this.running++;

      try {
        const result = await uni.request(options);
        resolve(result);
      } catch (error) {
        reject(error);
      } finally {
        this.running--;
        this.process();
      }
    }
  }
}
```

### 8.3 图片优化

```javascript
// 论文卡片图片懒加载
<image
  :src="paper.thumbnail_url"
  lazy-load
  mode="aspectFill"
/>
```

---

## 9. 安全设计

### 9.1 Token 设计

```python
# JWT Token 配置
JWT_CONFIG = {
    "algorithm": "HS256",
    "access_token_expire_minutes": 60 * 24 * 7,  # 7天
    "refresh_token_expire_minutes": 60 * 24 * 30, # 30天
}

def create_tokens(user_id: int) -> dict:
    """创建 Token 对"""
    now = datetime.utcnow()

    access_payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=JWT_CONFIG["access_token_expire_minutes"])
    }

    refresh_payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(minutes=JWT_CONFIG["refresh_token_expire_minutes"])
    }

    return {
        "access_token": jwt.encode(access_payload, SECRET_KEY, algorithm=JWT_CONFIG["algorithm"]),
        "refresh_token": jwt.encode(refresh_payload, SECRET_KEY, algorithm=JWT_CONFIG["algorithm"])
    }
```

### 9.2 API Key 加密

```python
from cryptography.fernet import Fernet

class APIKeyEncryption:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, api_key: str) -> str:
        """加密 API Key"""
        return self.fernet.encrypt(api_key.encode()).decode()

    def decrypt(self, encrypted_key: str) -> str:
        """解密 API Key"""
        return self.fernet.decrypt(encrypted_key.encode()).decode()

# 使用示例
encryption = APIKeyEncryption(settings.ENCRYPTION_KEY)

# 存储时加密
user.llm_api_key_enc = encryption.encrypt(api_key)

# 使用时解密
api_key = encryption.decrypt(user.llm_api_key_enc)
```

---

## 10. 部署架构

### 10.1 Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/paperlens
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=paperlens

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app

volumes:
  postgres_data:
  redis_data:
```

### 10.2 定时任务

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# 每日 08:30 抓取论文
@scheduler.scheduled_job('cron', hour=8, minute=30)
async def fetch_papers():
    """抓取每日论文"""
    sources = [ArxivSource(), ACLSource(), NeurIPSSource()]
    for source in sources:
        papers = await source.fetch_daily()
        await save_papers(papers)

# 每日 08:00 生成推荐
@scheduler.scheduled_job('cron', hour=8, minute=0)
async def generate_recommendations():
    """生成每日推荐"""
    users = await get_all_active_users()
    for user in users:
        papers = await recommend_papers(user.id)
        await cache_recommendations(user.id, papers)

# 每日 08:30 发送推送
@scheduler.scheduled_job('cron', hour=8, minute=30)
async def send_daily_push():
    """发送每日推送"""
    users = await get_users_with_push_enabled()
    for user in users:
        papers = await get_cached_recommendations(user.id)
        await send_template_message(user.openid, papers)

scheduler.start()
```

---

*本文档为 PaperLens 微信小程序技术架构文档 V2，基于 2026-03-27 讨论定稿。*