# TASKS.md — Refactor.ai
# Hackathon: Nebius × NVIDIA Global AI Hackathon (Deadline: 30 Oct 2026, 22:30 IST)

---

## Sprint 1: Multi-Model Architecture & Providers

| ID | Task | Priority | Status | Acceptance Criteria |
|----|------|----------|--------|---------------------|
| T-01 | Discover workspace & preserve existing projects | HIGH | DONE | Autopilot environment reused, scratch projects preserved |
| T-02 | PROJECT-BRIEF.md & Architecture specification | HIGH | DONE | Track, concept, and Nebius/NVIDIA/Gemini specs defined |
| T-03 | Config & Settings with Pydantic | HIGH | DONE | Environment loading & safe defaults verified |
| T-04 | Request/Response Data Schemas | HIGH | DONE | Expanded schemas (10 goals, warning disclaimers) |
| T-05 | Google Gemini Provider Adapter | HIGH | DONE | REST generateContent integration with free tier support |
| T-06 | Nebius Token Factory Adapter | HIGH | DONE | Preserved NVIDIA Nemotron-3_5-Lightning integration |
| T-07 | Zero-Dependency REST Server (backend/main.py) | HIGH | DONE | /health, /api/config-status, and /api/refactor functional |

---

## Sprint 2: Frontend Implementation & Integration

| ID | Task | Priority | Status | Acceptance Criteria |
|----|------|----------|--------|---------------------|
| T-08 | React 19 + Vite 8 UI Scaffold | HIGH | DONE | Clean compilation in 126ms |
| T-09 | 10 Refactoring Objectives Selector | HIGH | DONE | Readability, Complexity, Performance, Bugs, Security, etc. |
| T-10 | Side-by-Side Diff Comparison View | HIGH | DONE | Added dedicated Side-by-Side Comparison tab in App.jsx |
| T-11 | Provider Status & Model Telemetry Badge | HIGH | DONE | Clear live AI vs deterministic demo mode indicator |
| T-12 | Safety Disclaimer Display | MEDIUM | DONE | Unverified code disclaimer banner added |
| T-13 | Copy & Download Controls | MEDIUM | DONE | Clipboard and file download functional |

---

## Sprint 3: Verification, Edge Cases & Deployment Packaging

| ID | Task | Priority | Status | Acceptance Criteria |
|----|------|----------|--------|---------------------|
| T-14 | Automated Unit & Integration Tests | HIGH | DONE | 19/19 tests passing (`test_backend.py`, `test_handler.py`, `test_user_journey.py`) |
| T-15 | Edge Case & Validation Handling | HIGH | DONE | Empty code, >50k chars, invalid goals, markdown unwrap tested |
| T-16 | Provider Error & Timeout Handling | HIGH | DONE | HTTP 401, 429 quota exhaustion, timeouts mocked & verified |
| T-17 | Frontend Production Build | HIGH | DONE | `npm run build` succeeds cleanly in 126ms |
| T-18 | Production Deployment Configs | HIGH | DONE | `vercel.json`, `render.yaml`, and `docs/DEPLOYMENT.md` updated |
| T-19 | Submission Artifacts | HIGH | DONE | `README.md`, `LICENSE`, `DEMO-SCRIPT.md`, and `SUBMISSION-CHECKLIST.md` updated |

---

## Remaining External User Actions

| ID | Item | Required Action | Status |
|---|---|---|---|
| B-01 | Real Gemini Live Inference Key | Add `GEMINI_API_KEY` to local `.env` if testing live AI inference | AWAITING USER KEY (Deterministic Demo mode functional) |
| B-02 | Real Nebius/NVIDIA Live Test | Add `NEBIUS_API_KEY` to local `.env` for competition compliance call | AWAITING USER KEY (Mocked & Adapter Verified) |
| B-03 | Git Commit & Push Authorization | User authorizes `git commit` and `git push` to public repo | AWAITING USER AUTHORIZATION |
| B-04 | Live Cloud Deployment | User authorizes linking repo to Render & Vercel dashboards | AWAITING USER AUTHORIZATION |
