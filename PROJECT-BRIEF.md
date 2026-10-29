# PROJECT-BRIEF.md — RefactorMind
# Hackathon: Nebius × NVIDIA Global AI Hackathon | 2026-10-28

---

## Competition Summary

| Field | Value |
|-------|-------|
| Hackathon | Nebius × NVIDIA Global AI Hackathon |
| Organizer | Nebius + NVIDIA via Devpost |
| Deadline | 30 October 2026, 10:30 PM IST |
| Track | **Coding and Agentic Engineering** |
| Required tech | Nebius Token Factory + NVIDIA open-source model |
| Judging (equal weight) | Technological Implementation, Design, Potential Impact, Quality of Idea |

---

## Concept

**Name:** RefactorMind
**Tagline:** *AI-powered code refactoring agent — paste legacy code, get production-ready code.*

---

## Problem Statement

Developers spend 30–40% of their time reading and understanding existing codebases — not writing new code. Legacy code, quick hacks, undocumented functions, and inconsistent style slow every team down. Code review is time-consuming. Junior developers struggle to modernize code they didn't write.

---

## Target Users

- Junior-to-mid developers inheriting legacy codebases.
- Engineers doing code review who want AI-suggested improvements.
- Teams enforcing type safety (migrating JavaScript → TypeScript, Python 2 → Python 3).
- Developers learning best practices through examples.

---

## Proposed Solution

RefactorMind is a web application powered by NVIDIA's Nemotron model (via Nebius Token Factory) that:

1. Accepts a code snippet in any major language.
2. Takes a user-selected refactoring goal:
   - **Readability** — rename variables, add comments, improve structure.
   - **Performance** — identify bottlenecks, suggest optimizations.
   - **Add Types** — add TypeScript/Python type annotations.
   - **Security Audit** — find injections, unsafe patterns, insecure defaults.
   - **Modernize** — upgrade syntax (Python 2→3, ES5→ES2024, etc.).
3. Returns the refactored code with a line-by-line diff and explanation.
4. Shows the exact NVIDIA model and Nebius endpoint used.

---

## Core User Journey

1. User lands on RefactorMind.
2. Pastes code into the editor (or selects a sample).
3. Selects a refactoring goal.
4. Optionally selects the language (auto-detected if blank).
5. Clicks "Refactor with NVIDIA".
6. Sees: refactored code | side-by-side diff | explanation panel.
7. Copies result or downloads as file.
8. Provider badge shows: `NVIDIA Nemotron via Nebius Token Factory`.

---

## Differentiating Feature

**Structured diff + explanation in one view.** Unlike generic AI chat, RefactorMind:
- Forces the model to return structured JSON (original, refactored, explanations array).
- Renders a real syntax-highlighted diff.
- Shows the reasoning for each change, not just the changed code.
- Is honest about the provider used (verifiable in the UI).

---

## Required Technology Match

| Requirement | Implementation |
|-------------|---------------|
| Nebius Token Factory | Backend calls `https://api.tokenfactory.nebius.com/v1/` |
| NVIDIA open-source model | `nvidia/Nemotron-3_5-Lightning` (primary) |
| OpenAI-compatible API | Uses `openai` Python SDK pointed at Nebius base URL |
| Provider transparency | Model name + provider shown in every response |

---

## Architecture

```
Browser (React + TypeScript + Vite)
    ↕ REST API
FastAPI Backend (Python)
    ├── /api/refactor  POST — main endpoint
    ├── /api/health    GET  — health + provider status
    └── /api/models    GET  — available models
    ↓
ProviderAdapter
    ├── Primary: Nebius Token Factory (NVIDIA Nemotron)
    └── Fallback: Groq (llama-3.1-8b-instant) — clearly labeled
```

---

## Risks and Fallbacks

| Risk | Likelihood | Fallback |
|------|-----------|---------|
| No Nebius API key | HIGH (user must provide) | Demo mode with fixture output, labeled |
| Nebius rate limit | MEDIUM | Retry with exponential backoff |
| Model returns non-JSON | MEDIUM | Response parser with fallback text mode |
| No Groq key | LOW | Nebius only; Groq is optional |

---

## Definition of Done

- [ ] Application starts from README instructions.
- [ ] Refactor endpoint returns structured response.
- [ ] NVIDIA model called via Nebius (verified by API response).
- [ ] Diff view renders correctly.
- [ ] Error states (no key, timeout, invalid input) handled.
- [ ] Tests pass (unit + smoke).
- [ ] Production build succeeds.
- [ ] HACKATHON-CHECKLIST.md fully verified.
