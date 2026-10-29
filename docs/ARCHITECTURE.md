# ARCHITECTURE.md — RefactorMind

## System Overview

```
┌─────────────────────────────────────────────┐
│              Browser (React + TS)            │
│                                             │
│  ┌──────────┐    ┌───────────────────────┐  │
│  │  Input   │    │      Output Panel     │  │
│  │  Panel   │───▶│  Refactored Code      │  │
│  │          │    │  Explanations         │  │
│  │ Code     │    │  Provider Badge       │  │
│  │ Goal     │    └───────────────────────┘  │
│  │ Language │                               │
│  └──────────┘                               │
└───────────────────┬─────────────────────────┘
                    │ POST /api/refactor
                    │ (Vite proxy in dev)
┌───────────────────▼─────────────────────────┐
│          FastAPI Backend (Python)            │
│                                             │
│  POST /api/refactor                         │
│  GET  /api/health                           │
│  GET  /api/models                           │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │         ProviderAdapter             │   │
│  │                                     │   │
│  │  1. Primary: Nebius Token Factory   │   │
│  │     └─ NVIDIA Nemotron-3_5-Lightning│   │
│  │                                     │   │
│  │  2. Secondary: Groq (optional)      │   │
│  │     └─ llama-3.1-8b-instant        │   │
│  │                                     │   │
│  │  3. Demo fixture (no keys)         │   │
│  └─────────────────────────────────────┘   │
└───────────────────┬─────────────────────────┘
                    │ OpenAI-compatible API
          ┌─────────▼──────────┐
          │  Nebius Token      │
          │  Factory           │
          │  api.tokenfactory  │
          │  .nebius.com/v1/   │
          └─────────┬──────────┘
                    │
          ┌─────────▼──────────┐
          │  NVIDIA            │
          │  Nemotron-3_5-     │
          │  Lightning         │
          └────────────────────┘
```

## Stack Selection Rationale

| Decision | Choice | Reason |
|----------|--------|--------|
| Backend | FastAPI + Python | Async support, OpenAI SDK, fast dev |
| Frontend | Vite + React + TypeScript | Fast HMR, type safety, judging-friendly |
| AI SDK | openai (Python) | Nebius is OpenAI-compatible — zero adapter code |
| State | React useState/useEffect | Simple stateless app, no Redux needed |
| Storage | None | Refactoring is stateless — no DB required |
| Styling | Plain CSS with variables | Zero dependency, full control, fast load |

## Data Flow

```
1. User types code + selects goal
2. Frontend: POST /api/refactor
3. Backend: validates request (Pydantic)
4. ProviderAdapter.refactor():
   a. Builds system prompt + user message
   b. Calls Nebius Token Factory with JSON response format
   c. Parses response JSON
   d. Returns RefactorResponse
5. Backend: adds X-Processing-Time header, returns JSON
6. Frontend: renders refactored code + explanations
7. Provider badge updates to show actual provider used
```

## Security Architecture

```
User Input
    ↓ (max 50,000 chars, strip null bytes)
Backend validates with Pydantic
    ↓
Prompt constructed (no shell execution)
    ↓
API call to Nebius (key in env var only)
    ↓
Response parsed as JSON (not eval'd)
    ↓
Returned to frontend as JSON
```

- API keys: `.env` only, never in source, never logged, never sent to frontend
- CORS: restricted to known origins
- Body size limit: 500KB
- Timeout: 30s
- No file system access
- No code execution (model generates code, we display it — we do not run it)

## NVIDIA Model Integration

Model: `nvidia/Nemotron-3_5-Lightning`
- High-efficiency transformer for always-on agent tasks
- Supports JSON output mode via response_format parameter
- Context window: sufficient for code refactoring tasks
- Accessed via Nebius Token Factory OpenAI-compatible endpoint

Prompt strategy:
- System prompt enforces strict JSON output schema
- User message contains language, goal, and code
- temperature=0.2 for deterministic, high-quality output
- max_tokens=4096 for complete refactored code

## Deployment Architecture

```
Production:
  Frontend → Vercel (static hosting, free tier)
  Backend  → Render (web service, free tier)
  
Environment variables:
  Render: NEBIUS_API_KEY, GROQ_API_KEY, ALLOWED_ORIGINS
  Vercel: VITE_API_URL=https://refactormind-api.onrender.com

CORS:
  Backend allows: [Vercel URL, localhost:5173, localhost:3000]
```

## File Structure

```
nebius-nvidia-2026/
├── backend/
│   ├── main.py          ← FastAPI app, routes, middleware
│   ├── config.py        ← Pydantic Settings
│   ├── models.py        ← Request/Response Pydantic models
│   ├── provider.py      ← ProviderAdapter, prompt engineering
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── main.tsx     ← React entry
│   │   ├── App.tsx      ← Main component
│   │   ├── App.css      ← All styles
│   │   ├── index.css    ← Reset
│   │   ├── types.ts     ← TypeScript interfaces
│   │   └── api.ts       ← API client
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .env.example
├── tests/
│   └── test_backend.py
├── docs/
├── AGENTS.md
├── PROJECT-BRIEF.md
├── ARCHITECTURE.md      ← This file
├── TASKS.md
├── PROGRESS.md
├── README.md
├── LICENSE
├── SUBMISSION-CHECKLIST.md
└── DEMO-SCRIPT.md
```

