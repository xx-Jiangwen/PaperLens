# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PaperLens is an arXiv paper aggregation tool with AI-powered structured summaries. It helps researchers discover and read papers efficiently through daily curated recommendations.

**Core positioning:**
- Mini Program = Filter (fragmented browsing)
- PC/Web = Research Station (deep reading)

## Commands

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env   # Configure environment variables
python -m app.main        # Run dev server at http://localhost:8000
```

API docs available at http://localhost:8000/docs

### Web Frontend (Vue 3)

```bash
cd web
npm install
npm run dev      # Development server
npm run build    # Production build
```

### Mini Program (uni-app)

Use HBuilderX or CLI:

```bash
cd paperlens-uniapp
# CLI development (if package.json exists)
npm run dev:mp-weixin   # WeChat mini program
npm run dev:h5          # H5
```

With HBuilderX: Import `paperlens-uniapp` directory directly.

### Docker

```bash
docker-compose up -d    # Start backend + PostgreSQL
```

## Architecture

### Repository Structure

```
paperlens/
├── backend/           # FastAPI backend (Python)
├── web/               # Vue 3 + TypeScript web frontend
├── paperlens-uniapp/  # uni-app mini program (Vue 3) - primary client
├── miniprogram/       # WeChat native mini program (DEPRECATED)
└── docs/              # Documentation
```

### Backend Architecture

```
backend/app/
├── api/               # FastAPI routers (papers, ai, auth, users, settings, bookmarks)
├── models/            # SQLAlchemy models (paper, user, bookmark, user_settings)
├── sources/           # Paper data sources (arxiv_source)
├── ai/                # AI services
│   ├── llm/           # LLM abstraction (OpenAI-compatible)
│   └── summarizer.py  # Paper summarization
├── scheduler/         # APScheduler jobs (daily paper fetch)
└── utils/             # Utilities (crypto for API key encryption)
```

**API Prefix:** `/api/v1`

**Key routes:**
- `/papers` - Paper CRUD, today's papers, search
- `/ai` - AI summary generation, chat
- `/auth` - WeChat login
- `/users` - User profile, stats
- `/settings` - User preferences, BYOK config
- `/bookmarks` - Paper bookmarks

### Frontend Architecture

Both web and uni-app use similar patterns:
- **State:** Pinia stores (user, settings, papers)
- **API:** Axios/uni.request wrapper with auto token injection
- **Views/Pages:** Home, Detail, Settings, Bookmarks

### Database

- **Development:** SQLite (`paperpulse.db`)
- **Production:** PostgreSQL

Key tables: `papers`, `users`, `bookmarks`, `user_settings`

## BYOK (Bring Your Own Key)

Users can configure their own LLM API keys in settings. Supports any OpenAI-compatible endpoint:
- OpenAI / Azure OpenAI
- DeepSeek
- Local Ollama

API keys are encrypted with AES-256-GCM before storage.

## Configuration

Required environment variables (see `.env.example`):
- `DATABASE_URL` - Database connection
- `SECRET_KEY` - JWT signing
- `ENCRYPT_MASTER_KEY` - API key encryption (32-byte hex)
- `WX_APP_ID` / `WX_APP_SECRET` - WeChat mini program
- `OFFICIAL_LLM_*` - Official LLM for batch summary generation
- `DAILY_CATEGORIES` - arXiv categories to fetch (default: cs.AI,cs.CL,cs.CV,cs.LG,stat.ML)

## Documentation

- `docs/product/PRD.md` - Product requirements
- `docs/miniprogram/v2-*.md` - Mini program V2 design docs (product, UI, architecture)
- `docs/backend/api-reference.md` - API reference
- `docs/adr/` - Architecture Decision Records

## Important Notes

- The `miniprogram/` directory is deprecated; use `paperlens-uniapp/` instead
- Mini program is being refactored to V2 with Apple minimalist design - see `docs/superpowers/specs/2026-03-27-paperlens-miniprogram-v2-design.md`
- ADR-002 documents the switch from native to uni-app framework