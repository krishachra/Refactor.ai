# Refactor.ai ⚡
> **Autonomous Multi-Model Code Refactoring & Modernization Platform**  
> Primary Development Engine: **Google Gemini API** (Free Tier Supported)  
> Mandatory Hackathon Infrastructure: **NVIDIA Nemotron** on **Nebius Token Factory**  
> *Track: Coding & Agentic Engineering (Nebius × NVIDIA Global AI Hackathon)*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-brightgreen.svg)]()
[![React: 19](https://img.shields.io/badge/React-19-cyan.svg)]()
[![Vite: 8](https://img.shields.io/badge/Vite-8-purple.svg)]()
[![Google Gemini API](https://img.shields.io/badge/AI%20Engine-Google%20Gemini%20Flash-4285F4.svg)]()
[![Nebius Token Factory](https://img.shields.io/badge/Infrastructure-Nebius%20Token%20Factory-indigo.svg)]()
[![NVIDIA Open-Source](https://img.shields.io/badge/Model-NVIDIA%20Nemotron-76b900.svg)]()

---

## 📌 Executive Summary & User Journey

Software engineers spend over **40% of their time** reading, refactoring, and fixing legacy or insecure code. 

**Refactor.ai** provides an automated, multi-model refactoring workflow that converts complex, undocumented, or vulnerable code into clean, production-grade software:
1. **Interactive Source Input:** Paste any code snippet or select from built-in sample scenarios (Billing Logic, Deeply Nested Branching, Async Network Fetch, SQL Injection).
2. **10 Refactoring Objectives:**
   - 📖 **Improve Readability:** Self-documenting naming, structured formatting.
   - 🔀 **Reduce Complexity:** Flattening nested if/else ladders, early exits.
   - ⚡ **Improve Performance:** Transforming quadratic $O(N \cdot M)$ loops into linear $O(N + M)$ algorithms.
   - 🐛 **Identify Potential Bugs:** Catching mutable default arguments, resource leaks, off-by-one errors.
   - 🛠️ **Improve Maintainability:** Encapsulating loose params into dataclasses/schemas.
   - 💬 **Add Comments:** Step-by-step explanatory annotations.
   - 🔍 **Explain Code:** Plain-English walkthrough of mathematical & architectural logic.
   - 🏷️ **Add Types:** PEP 484 static typing, TypeScript interfaces.
   - 🛡️ **Security Audit:** Mitigating CWE-89 SQL injection, sanitizing inputs.
   - ✨ **Modernize:** Upgrading legacy callbacks to modern ECMAScript async/await and Fetch API.
3. **Transparent Analysis & Side-by-Side Comparison:** Returns clean refactored code, line-by-line explanations, quantified improvements, tradeoff warnings, and a side-by-side diff.
4. **Export & Portability:** One-click clipboard copy or direct file download (`.py`, `.js`, `.ts`).

---

## 🏗️ Multi-Provider Architecture

Refactor.ai decouples refactoring business logic from underlying inference vendors via a clean `ProviderAdapter`:

```
┌─────────────────────────────────────────────────────────────┐
│                 React 19 + Vite 8 Frontend                  │
│   • Multi-Goal Selector (10 Specialized Objectives)         │
│   • Side-by-Side Diff & Line Comparison View                │
│   • Live Telemetry (Active Provider, Model, Latency)        │
│   • Explicit Safety Disclaimer Warning                      │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / REST (5173 -> 8000)
┌──────────────────────────────▼──────────────────────────────┐
│                Refactor.ai Backend (FastAPI / REST)         │
│   • GET  /health              (Status, active model)        │
│   • GET  /api/config-status   (Provider readiness)          │
│   • POST /api/refactor        (Validation, size limit, rate)│
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    ProviderAdapter                    │  │
│  │  1. Primary Dev: Google Gemini API (Free Tier)        │  │
│  │  2. Hackathon Compliance: Nebius (NVIDIA Nemotron)    │  │
│  │  3. Secondary Fallback: Groq (llama-3.1-8b-instant)   │  │
│  │  4. Deterministic Demo Mode (Offline Baseline)        │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
┌──────────────┐       ┌──────────────┐        ┌──────────────┐
│Google Gemini │       │Nebius Token  │        │Groq API      │
│API (REST)    │       │Factory       │        │(Fallback)    │
│gemini-2.5-   │       │NVIDIA        │        │llama-3.1-    │
│flash         │       │Nemotron-3_5  │        │8b-instant    │
└──────────────┘       └──────────────┘        └──────────────┘
```

---

## ⚡ Quick Start & Setup

### 1. Configure Environment
```bash
cd hackathons/refactor-ai
cp .env.example .env
```
To enable live AI inference, configure either:
- **Google Gemini API** (Free tier available at [Google AI Studio](https://aistudio.google.com/apikey)):
  ```bash
  AI_PROVIDER=gemini
  GEMINI_API_KEY="your-gemini-key"
  ```
- **Nebius Token Factory** (NVIDIA Nemotron model):
  ```bash
  AI_PROVIDER=nebius
  NEBIUS_API_KEY="your-nebius-key"
  ```
*(If no keys are configured, Refactor.ai automatically runs in offline **Deterministic Demo Mode** with full UI support).*

### 2. Start Backend Server
```bash
python3 backend/main.py
```
*Backend runs on `http://localhost:8000`.* Verify status:
```bash
curl http://localhost:8000/health
```

### 3. Start Frontend Client
```bash
cd frontend
npm run dev
```
*Open [http://localhost:5173](http://localhost:5173) in your browser.*

---

## 🧪 Automated Testing & Verification

Refactor.ai is verified by **19 automated unit and integration tests**:

```bash
python3 -m unittest discover -s tests -v
```

**Test Coverage Highlights:**
- `test_gemini_provider_mock_call`: Verifies REST payload assembly and JSON extraction for Google Gemini.
- `test_gemini_quota_exhausted_handling`: Gracefully handles HTTP 429 quota exhaustion.
- `test_nebius_provider_mock_call`: Verifies NVIDIA Nemotron model integration.
- `test_fallback_gemini_to_nebius`: Automatically falls back across configured providers.
- `test_journey_*`: Tests readability, security audits, boundary checks (empty code, 50k character limit).

---

## 🚀 Production Deployment

Deploying Refactor.ai on zero-cost free tiers:
- **Backend on Render:** Python 3 service using [`render.yaml`](render.yaml).
- **Frontend on Vercel:** Edge static delivery with `/api` proxy using [`vercel.json`](vercel.json).
- Detailed deployment guide in [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

---

## 📄 License & Safety
Released under the [MIT License](LICENSE).  
*Disclaimer: AI-generated code requires human review and must be validated against your project's test suite prior to production deployment.*
