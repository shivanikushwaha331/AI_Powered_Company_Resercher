# AI Company Research Assistant 🚀

A production-grade, modular, scalable **AI-Powered Corporate Intelligence Research Platform** built with **FastAPI, Python 3.12+, Next.js 15, React 19, TypeScript, Tailwind CSS, ReportLab, OpenRouter LLMs, Serper.dev, and Discord Integration**.

---

## 🌟 Key Features & Capabilities

- 🤖 **Multi-Model OpenRouter LLM Inference**: Select between `google/gemini-2.5-flash`, `anthropic/claude-3.5-sonnet`, `openai/gpt-4o-mini`, and `deepseek/deepseek-r1`.
- 📊 **8-Part Structured JSON Synthesis**: Extracts Company Summary, Products, Services, Pain Points Solved, Business Model, Target Customers, 4-Quadrant SWOT Matrix, and Competitor Suggestions.
- 🔍 **Serper.dev Search & Knowledge Graph**: Resolves official company websites, headquarters, phone, address, and industry signals.
- 🕷️ **Intelligent Asynchronous Crawler**: Crawl4AI + BeautifulSoup fallback discovering About, Products, Services, Solutions, and Pricing pages while ignoring noise/duplicate links.
- 🎯 **Competitor Research & Automated Resolution**: Automated Serper lookup for missing competitor URLs, displaying country badges and reason for competition cards.
- 📄 **Professional ReportLab PDF Export**: Generates PDF reports with Cover Page, SWOT matrix, Competitor table, and running NumberedCanvas `"Page X of Y"` footers.
- 💬 **Enhanced ChatGPT UI & Discord Bot**: Supports chat history management, typing animations, Markdown parsing (headings, code blocks, tables), copy/regenerate buttons, and Discord Bot REST API notifications.

---

## 🏗️ Project Architecture

```
AI_Powered_Company_Resercher/
├── docker-compose.yml         # Multi-container Docker production orchestration
├── vercel.json                # Vercel deployment config
├── .env                       # Live environment secrets configuration
├── backend/
│   ├── Dockerfile             # Python 3.12 FastAPI Docker image
│   ├── config/                # Pydantic environment settings
│   ├── downloads/pdf/         # Compiled ReportLab PDF reports storage
│   ├── routers/               # FastAPI REST & SSE endpoints
│   ├── schemas/               # Validation schemas (pydantic)
│   ├── services/              # Business logic (serper, crawl, ai, competitor, pdf, discord)
│   └── main.py                # FastAPI app factory
├── frontend/
│   ├── Dockerfile             # Next.js 15 Standalone Docker image
│   ├── src/app/               # Next.js 15 App Router pages
│   ├── src/components/        # UI components (chat, settings, ui)
│   ├── src/hooks/             # Custom hooks (use-research-api, use-toast)
│   └── src/services/          # API layer (axios client)
```

---

## 🚀 Deployment Instructions

### Method 1: Self-Hosted Docker Compose (1-Command Full-Stack Startup)

Run both the FastAPI backend and Next.js frontend in production containers with Docker Compose:

```bash
# Build and launch containers in detached mode
docker-compose up --build -d

# Access Services:
# Frontend: http://localhost:3000
# Backend API Docs: http://localhost:8000/docs
```

---

### Method 2: Cloud PaaS Deployment (Vercel + Render / Railway)

#### Step 1: Deploy Backend (FastAPI) to Render / Railway / Fly.io
1. Push your repository to GitHub.
2. Log into [Render](https://render.com) or [Railway](https://railway.app).
3. Create a **New Web Service** pointing to your repository.
4. Select `backend/Dockerfile` as the build strategy.
5. Set Environment Variables:
   - `MOCK_MODE=false`
   - `OPENROUTER_API_KEY=sk-or-v1-...`
   - `SERPER_API_KEY=...`
6. Deploy! Render will give you a backend URL (e.g. `https://company-researcher-api.onrender.com`).

#### Step 2: Deploy Frontend (Next.js 15) to Vercel
1. Log into [Vercel](https://vercel.com).
2. Click **Add New Project** and import your repository.
3. Set Environment Variables in Vercel settings:
   - `NEXT_PUBLIC_API_URL=https://company-researcher-api.onrender.com`
4. Click **Deploy**. Vercel will host your application live!

---

## 🧪 Verification & Test Suite

Run the comprehensive Python verification test suite across all core backend services:

```bash
# Serper.dev Search Verification
PYTHONPATH=. python3 backend/tests/test_serper_service.py

# Intelligent Crawler Verification
PYTHONPATH=. python3 backend/tests/test_intelligent_crawler.py

# OpenRouter LLM Synthesis Verification
PYTHONPATH=. python3 backend/tests/test_openrouter_service.py

# Competitor Research Verification
PYTHONPATH=. python3 backend/tests/test_competitor_service.py

# ReportLab PDF Generation Verification
PYTHONPATH=. python3 backend/tests/test_pdf_generation.py

# Discord Integration Verification
PYTHONPATH=. python3 backend/tests/test_discord_service.py
```
