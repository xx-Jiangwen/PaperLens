# PaperLens 产品需求文档 (PRD)

---

| 字段 | 内容 |
|---|---|
| **产品名称** | PaperLens |
| **Slogan** | 探索前沿，精读论文 |
| **版本** | V1.0.0 |
| **状态** | 评审中 |
| **日期** | 2026-03-26 |
| **作者** | - |

---

## 1. 文档概述

### 1.1 目的

本文档定义 PaperLens 小程序及网页版的功能需求，指导开发团队完成从数据抓取、AI 处理到多端展示的完整闭环。

### 1.2 目标用户

| 用户群体 | 核心诉求 |
|---|---|
| 学术研究人员 | 每日追踪顶级期刊/会议动态，不遗漏重要论文 |
| 算法工程师 | 快速了解可落地的技术细节与代码实现 |
| 在校学生 | 克服语言障碍，快速理解论文核心思想 |

### 1.3 产品定位

PaperLens 是一个 **arXiv 论文聚合 + AI 增强阅读工具**，核心差异化：

- **自动化**：每日定时抓取，无需手动刷新
- **AI 结构化**：非简单翻译，提炼 What / How / Why 三段式摘要
- **双端覆盖**：网页端（生产力）+ 小程序端（碎片化阅读）
- **开放性**：完全开源，用户可自带 API Key 接入任意兼容 OpenAI 协议的大模型

---

## 2. MVP 范围界定（V1.0）

> MVP（最小可行产品）目标：最快速度验证核心价值，让用户能真正用起来。

| 模块 | V1.0 包含 | V2.0 及以后 |
|---|---|---|
| **数据来源** | arXiv | Hugging Face Papers、OpenReview |
| **AI 功能** | 三段式结构化摘要（流式输出） | Paper-Chat RAG 对话、公式解析 |
| **网页版** | 论文列表、详情页、用户设置（BYOK） | 双栏 PDF 阅读器、Markdown/LaTeX 导出 |
| **小程序** | 论文列表、详情页、微信登录 | 语音播放器、公众号每日推送 |
| **TTS** | 微信小程序内置 TTS | 火山引擎 TTS（播客化音色） |

---

## 3. 核心功能需求

### 3.1 自动化数据管道（Backend）

- **FR-01 抓取引擎**：每日 08:30 (UTC+8) 自动同步 arXiv 最新论文，支持按分类筛选（cs.AI、cs.CL、cs.CV、cs.LG、stat.ML 等）
- **FR-02 智能分类**：基于 arXiv 官方分类体系进行标签化展示，后续引入 NLP 二次分类

### 3.2 AI 智能增强层（AI Layer）

- **FR-03 三段式结构化摘要**
  - **What**：这篇论文解决了什么问题，提出了什么方案
  - **How**：采用了什么技术路径和方法
  - **Why**：主要贡献和意义是什么
  - 要求：非简单翻译，须提炼核心信息；支持流式输出（打字机效果）

- **FR-04 BYOK 大模型配置**（V1.0 核心设计）
  - 用户可在设置页填入：`base_url` + `api_key` + `model_name`
  - 兼容所有符合 OpenAI API 协议的模型（OpenAI、DeepSeek、Claude 兼容层、本地 Ollama 等）
  - 官方提供有限额度，用户自带 Key 无限制使用
  - API Key 加密存储（AES-256-GCM），不明文落库

- **FR-05 语音合成（V2.0）**：将摘要转化为"播客化"文案，支持不同音色播报

### 3.3 微信小程序端（Frontend - Mobile）

- **FE-01 今日精选**：瀑布流展示每日最新论文卡片，支持按分类筛选
- **FE-02 论文详情**：展示三段式 AI 摘要 + 原文链接 + PDF 链接
- **FE-03 微信登录**：一键微信授权，无需注册
- **FE-04 用户设置**：配置 BYOK API Key
- **FE-05 收藏功能**：一键收藏，跨端同步
- **FE-06 语音播放（V2.0）**：类音乐 App 界面，支持后台播放、倍速调节

### 3.4 Web 生产力端（Frontend - PC）

- **FE-07 论文列表**：分类筛选 + 关键词搜索 + 时间排序
- **FE-08 论文详情**：三段式摘要（流式输出）+ 原文/PDF 链接
- **FE-09 用户设置**：BYOK 配置 + 偏好分类订阅
- **FE-10 收藏夹**：管理已收藏论文
- **FE-11 双栏阅读（V2.0）**：左侧 PDF，右侧 AI 对话框 + 笔记区
- **FE-12 导出（V2.0）**：AI 对话记录、文献引用格式导出为 Markdown/LaTeX

---

## 4. 技术架构

### 4.1 整体架构

```
                    ┌─────────────────────────────┐
                    │         数据源层              │
                    │  ArxivSource (V1.0)          │
                    │  HFPapersSource (V2.0)       │
                    │  BaseSource 统一接口          │
                    └──────────────┬──────────────┘
                                   │ PaperDTO
                    ┌──────────────▼──────────────┐
                    │        后端 API 层            │
                    │  FastAPI + SQLAlchemy        │
                    │  APScheduler 定时任务         │
                    │  AI 摘要服务（BYOK/官方额度） │
                    └──────┬──────────────┬────────┘
                           │              │
              ┌────────────▼──┐    ┌──────▼────────────┐
              │   网页端       │    │    微信小程序端     │
              │   Vue 3       │    │    原生小程序       │
              │   Vite + TS   │    │    wx.request      │
              └───────────────┘    └───────────────────┘
```

### 4.2 技术栈

| 层级 | 技术选型 | 说明 |
|---|---|---|
| **后端框架** | FastAPI | 自动 Swagger 文档，async 支持，性能优 |
| **ORM** | SQLAlchemy 2.0 | 支持 SQLite（开发）→ PostgreSQL（生产）零改动切换 |
| **数据库迁移** | Alembic | 版本化管理 schema 变更 |
| **定时任务** | APScheduler | 内嵌进程，无需独立部署 |
| **网页前端** | Vue 3 + Vite + TypeScript | 组件化，Pinia 状态管理 |
| **小程序** | 微信原生框架 | 无额外编译链，审核友好 |
| **容器化** | Docker + docker-compose | 本地开发一键启动 |

### 4.3 BYOK（Bring Your Own Key）设计

```
用户在设置页填写：
  base_url   = "https://api.deepseek.com/v1"
  api_key    = "sk-xxxxx"         ← AES-256-GCM 加密后存库
  model_name = "deepseek-chat"

请求摘要时：
  1. 解密 api_key（仅在内存中）
  2. 构造 LLMConfig → LLMFactory → OpenAICompatibleLLM
  3. 调用大模型，流式返回 SSE
  4. 明文 Key 离开内存，不落任何日志
```

### 4.4 扩展性设计（留口子）

```python
# 数据源适配器 - 新增来源只需新建子类
class BaseSource(ABC):
    async def fetch_daily(...) -> list[PaperDTO]: ...
    async def search(...) -> list[PaperDTO]: ...

class ArxivSource(BaseSource): ...      # V1.0
class HFPapersSource(BaseSource): ...   # V2.0，新建此类即可

# LLM 适配器 - 兼容任意 OpenAI 协议模型
class BaseLLM(ABC):
    async def summarize_paper_stream(...): ...

class OpenAICompatibleLLM(BaseLLM): ... # 覆盖 OpenAI/DeepSeek/Ollama

# TTS 适配器 - V1.0 微信内置，后续切换无需改业务逻辑
class BaseTTS(ABC):
    async def synthesize(text: str) -> bytes: ...

class WechatTTS(BaseTTS): ...           # V1.0（前端调用）
class VolcengineTTS(BaseTTS): ...       # V2.0
```

---

## 5. 数据库设计

### 5.1 papers 表（论文）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | VARCHAR(64) PK | 带版本号的 ID，如 `arxiv:1706.03762v7` |
| `arxiv_id_base` | VARCHAR(32) | 去版本号 ID，用于 upsert 去重 |
| `title` | TEXT | 论文标题 |
| `authors` | JSON | 作者列表 `["Vaswani", ...]` |
| `abstract` | TEXT | 原始英文摘要 |
| `published_at` | TIMESTAMP | arXiv 发布时间 |
| `updated_at` | TIMESTAMP | 最后更新时间 |
| `url` | VARCHAR(256) | arXiv 页面链接 |
| `pdf_url` | VARCHAR(256) | PDF 直链 |
| `categories` | JSON | 分类列表 `["cs.CL", "cs.LG"]` |
| `primary_category` | VARCHAR(32) | 主分类 |
| `comment` | TEXT | 作者备注（页数、会议等） |
| `journal_ref` | VARCHAR(256) | 期刊引用 |
| `doi` | VARCHAR(128) | DOI 编号 |
| `source_name` | VARCHAR(32) | 数据来源，如 `arxiv` |
| `summary_what` | TEXT | AI 摘要 - What 段 |
| `summary_how` | TEXT | AI 摘要 - How 段 |
| `summary_why` | TEXT | AI 摘要 - Why 段 |
| `summary_status` | VARCHAR(16) | `pending`/`processing`/`done`/`failed` |
| `summary_model` | VARCHAR(64) | 生成摘要时所用模型 |
| `fetched_at` | TIMESTAMP | 入库时间 |

### 5.2 users 表（用户）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | INTEGER PK | 内部用户 ID |
| `openid` | VARCHAR(128) UNIQUE | 微信 openid |
| `union_id` | VARCHAR(128) | 微信 unionid（跨平台打通） |
| `nickname` | VARCHAR(64) | 昵称 |
| `avatar_url` | VARCHAR(512) | 头像 URL |
| `source` | VARCHAR(16) | `miniprogram` / `web` |
| `is_active` | BOOLEAN | 是否激活 |
| `created_at` | TIMESTAMP | 注册时间 |
| `last_seen_at` | TIMESTAMP | 最后活跃时间 |

### 5.3 user_settings 表（用户设置）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | INTEGER PK | - |
| `user_id` | INTEGER FK | 关联 users.id |
| `llm_base_url` | VARCHAR(512) | 如 `https://api.deepseek.com/v1` |
| `llm_api_key_enc` | TEXT | **AES-256-GCM 加密**后的密文 |
| `llm_model_name` | VARCHAR(128) | 如 `deepseek-chat`、`gpt-4o-mini` |
| `preferred_categories` | JSON | 关注的分类 `["cs.AI", "cs.CL"]` |
| `language` | VARCHAR(8) | 摘要语言 `zh`/`en` |
| `daily_digest` | BOOLEAN | 是否接收每日推送 |
| `updated_at` | TIMESTAMP | 最后更新时间 |

### 5.4 bookmarks 表（收藏）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | INTEGER PK | - |
| `user_id` | INTEGER FK | 关联 users.id |
| `paper_id` | VARCHAR(64) FK | 关联 papers.id |
| `note` | TEXT | 用户笔记（V2.0 预留） |
| `created_at` | TIMESTAMP | 收藏时间 |

---

## 6. API 接口清单

> 所有接口统一前缀 `/api/v1`，统一响应格式：
> ```json
> {"code": 200, "msg": "success", "data": {...}}
> ```

### 6.1 论文接口

| 方法 | 路径 | 说明 | 是否需要登录 |
|---|---|---|---|
| GET | `/papers` | 论文列表，支持 `category`/`q`/`page`/`size`/`date` 参数 | 否 |
| GET | `/papers/today` | 今日新抓取论文 | 否 |
| GET | `/papers/{paper_id}` | 单篇论文详情 | 否 |
| POST | `/papers/search` | 透传 arXiv 实时搜索（非数据库） | 否 |

### 6.2 AI 摘要接口

| 方法 | 路径 | 说明 | 是否需要登录 |
|---|---|---|---|
| GET | `/ai/summarize/{paper_id}/stream` | SSE 流式输出三段式摘要 | 可选（用自己的 Key 需登录） |
| GET | `/ai/summarize/{paper_id}/status` | 查询摘要状态 | 否 |

SSE 数据格式：
```
data: {"section": "what", "delta": "这篇论文提出了..."}
data: {"section": "how", "delta": "作者采用了..."}
data: {"section": "why", "delta": "主要贡献在于..."}
data: [DONE]
```

### 6.3 认证接口

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/auth/wx-login` | 微信小程序登录，传入 `code`，返回 JWT Token |
| POST | `/auth/refresh` | 刷新 Token |

### 6.4 用户与设置接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/users/me` | 获取当前用户信息 |
| GET | `/settings` | 获取 BYOK 设置 |
| PUT | `/settings` | 更新 BYOK 设置（Key 落库前加密） |
| POST | `/settings/test-llm` | 测试 LLM 连通性 |

### 6.5 收藏接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/bookmarks` | 获取收藏列表 |
| POST | `/bookmarks/{paper_id}` | 收藏论文 |
| DELETE | `/bookmarks/{paper_id}` | 取消收藏 |

---

## 7. 非功能需求

### 7.1 性能要求

| 指标 | 目标 |
|---|---|
| 摘要生成时间 | 首 token ≤ 2s（流式输出，用户感知快） |
| 列表接口响应 | ≤ 200ms |
| 小程序并发 | V1.0 支撑 1,000+ 用户同时在线（V2.0 扩展至 10,000+） |

### 7.2 UI/UX 设计规范

| 规范 | 内容 |
|---|---|
| 视觉风格 | 科技感、极简主义 |
| 背景色 | `#0D1117`（深海黑） |
| 点缀色 | `#58A6FF`（智能蓝） |
| 字体 | 系统默认无衬线字体 |

---

## 8. 风险评估

| 风险 | 等级 | 应对措施 |
|---|---|---|
| **版权风险** | 中 | 仅展示摘要和公共链接，不直接存储全文 PDF |
| **AI 幻觉风险** | 中 | 界面显著标注「内容由 AI 生成，请以原文为准」 |
| **API Key 泄露** | 高 | AES-256-GCM 加密存储，明文仅存在于内存请求中，不落日志 |
| **arXiv 反爬** | 低 | 使用官方 arxiv Python 库，遵守 API 速率限制 |
| **小程序审核** | 中 | 需单独注册小程序主体（已有公众号，可绑定同主体） |

---

## 9. 版本迭代计划

### V1.0 MVP（当前阶段）
- arXiv 每日定时抓取
- AI 三段式摘要（流式输出）
- 网页版：列表 + 详情 + BYOK 设置
- 小程序：列表 + 详情 + 微信登录

### V1.1
- 收藏/订阅功能
- 公众号每日推送
- 微信小程序 TTS 语音播放

### V2.0
- Paper-Chat RAG 对话
- 火山引擎 TTS（播客化音色）
- HuggingFace Papers 数据源
- 网页端双栏 PDF 阅读器
- Markdown/LaTeX 导出

---

*本文档为开源项目 PaperLens 的产品需求文档，欢迎 Issue 和 PR。*
