# PaperLens

> 探索前沿，精读论文 — arXiv 论文聚合 + AI 结构化摘要工具

## 项目结构

```
paperlens/
├── backend/        # FastAPI 后端
├── web/            # Vue 3 网页前端
├── uni-app/        # uni-app 多端小程序 (推荐)
└── miniprogram/    # 微信原生小程序 (已废弃)
```

## 快速启动

### 后端

```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env   # 填写配置
python -m app.main
# 访问 http://localhost:8000/docs 查看 API 文档
```

### 网页前端

```bash
cd web
npm install
npm run dev
```

### uni-app 小程序（推荐）

使用 HBuilder X 或命令行开发：

```bash
cd uni-app
npm install
npm run dev:mp-weixin   # 微信小程序
npm run dev:h5          # H5
```

使用 HBuilder X：直接导入 `uni-app` 目录即可。

### 微信原生小程序（已废弃）

使用微信开发者工具打开 `miniprogram/` 目录。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | FastAPI + SQLAlchemy + APScheduler |
| 数据库 | SQLite（开发）/ PostgreSQL（生产） |
| 网页前端 | Vue 3 + Vite + TypeScript + Pinia |
| 小程序 | uni-app (Vue 3 + TypeScript + Pinia) |

## BYOK 配置

在设置页填入你自己的 LLM 配置，支持所有兼容 OpenAI 协议的模型：

- OpenAI / Azure OpenAI
- DeepSeek
- 本地 Ollama

## 开源协议

MIT License
