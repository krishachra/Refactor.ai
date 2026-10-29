# AGENTS.md — RefactorMind
# Hackathon: Nebius × NVIDIA Global AI Hackathon | Created: 2026-10-28

Extends the global `Hackathon-Autopilot/AGENTS.md`. Read both.

---

## Project Scope

Working directory: `hackathons/nebius-nvidia-2026/`
Do NOT modify files outside this directory.

---

## Required Technologies (MANDATORY)

- **Primary AI**: Nebius Token Factory (`https://api.tokenfactory.nebius.com/v1/`)
- **NVIDIA Model**: `nvidia/Nemotron-3_5-Lightning` (verify via `/v1/models` on startup)
- **SDK**: OpenAI Python SDK pointed at Nebius base URL
- **Secondary (optional)**: Groq `llama-3.1-8b-instant` for resilience

**Never** label Groq output as NVIDIA output.
**Never** label demo fixture output as live AI output.

---

## Track: Coding and Agentic Engineering

The app must demonstrate a real agentic coding workflow:
- Structured prompt engineering (JSON output format enforced).
- Multi-field structured response (original, refactored, explanations).
- Provider transparency in UI.

---

## Judging Strategy

| Criterion | Our Approach |
|-----------|-------------|
| Technological Implementation | Nebius + NVIDIA Nemotron, structured JSON prompting, OpenAI SDK |
| Design | Split editor/diff/explanation UI, dark code editor theme, responsive |
| Potential Impact | Real developer pain (legacy code), quantifiable time savings |
| Quality of Idea | Focused diff+explanation in one view, honest provider badge |

---

## Stack

- Frontend: Vite + React + TypeScript (port 5173)
- Backend: FastAPI + Python 3.14 (port 8000)
- AI: openai SDK → Nebius Token Factory → NVIDIA Nemotron
- Storage: None (stateless — no DB needed)
- Deployment: Render (backend) + Vercel (frontend) — free tier

---

## Security Rules (Project-specific)

- `NEBIUS_API_KEY` and `GROQ_API_KEY`: backend `.env` only.
- Never log API keys, even partially.
- Never send API key to frontend.
- `/api/health` returns provider name but never the key.
- User code snippets: limit to 50,000 chars, strip null bytes.

---

## Provider Adapter Contract

```python
class RefactorResponse:
    original_code: str
    refactored_code: str
    language: str
    goal: str
    explanations: list[str]  # per-change explanations
    provider: str            # "nebius-nvidia" | "groq" | "demo"
    model: str               # exact model ID used
    tokens_used: int
```

---

## API Contract

### POST /api/refactor
```json
Request:
{
  "code": "...",
  "goal": "readability|performance|add_types|security|modernize",
  "language": "python|javascript|typescript|java|go|auto",
  "context": "optional extra context"
}

Response:
{
  "original_code": "...",
  "refactored_code": "...",
  "language": "python",
  "goal": "readability",
  "explanations": ["Changed x to y because...", ...],
  "provider": "nebius-nvidia",
  "model": "nvidia/Nemotron-3_5-Lightning",
  "tokens_used": 1234,
  "processing_ms": 2100
}
```

### GET /api/health
```json
{
  "status": "ok",
  "primary_provider": "nebius",
  "primary_model": "nvidia/Nemotron-3_5-Lightning",
  "primary_configured": true,
  "secondary_provider": "groq",
  "secondary_configured": false,
  "version": "1.0.0"
}
```

---

## Definition of Done

- [ ] `uvicorn main:app` starts without errors.
- [ ] `npm run dev` serves frontend.
- [ ] POST /api/refactor returns valid RefactorResponse.
- [ ] Diff view renders original vs refactored.
- [ ] Provider badge shows real provider.
- [ ] Demo mode works when no key is configured.
- [ ] Unit tests: provider adapter, input validation, response parsing.
- [ ] `npm run build` succeeds.
- [ ] `python3 -m pytest tests/ -v` passes.
