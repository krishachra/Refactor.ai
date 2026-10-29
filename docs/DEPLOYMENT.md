# DEPLOYMENT.md — Production Deployment Blueprint

This document details how Refactor.ai is hosted on zero-cost free-tier platforms compliant with hackathon submission standards.

---

## Architecture Topology

```
┌─────────────────────────────────┐
│        Vercel (Frontend)        │
│  - Static React + Vite build    │
│  - Edge CDN delivery            │
│  - Reverse proxy /api to Render │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│         Render (Backend)        │
│  - Python 3 REST microservice   │
│  - Zero-dependency HTTP engine  │
│  - Managed secrets via env vars │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│      Nebius Token Factory       │
│  - NVIDIA Nemotron AI Model     │
└─────────────────────────────────┘
```

---

## 1. Backend Deployment on Render (Free Web Service)

1. **Create Account / Login:** [https://render.com/](https://render.com/)
2. **New Web Service:** Select **Web Service** → Connect your GitHub repository.
3. **Root Directory:** Leave default or set to repository root.
4. **Environment:** `Python 3`
5. **Build Command:**
   ```bash
   pip install pydantic
   ```
6. **Start Command:**
   ```bash
   python backend/main.py $PORT
   ```
7. **Health Check Path:**
   ```
   /health
   ```
8. **Configure Environment Variables (in Render Dashboard):**
   - `NEBIUS_API_KEY`: `<your-nebius-token>` *(stored securely, never logged)*
   - `NEBIUS_BASE_URL`: `https://api.tokenfactory.nebius.com/v1/`
   - `NEBIUS_MODEL`: `nebius/nvidia/Nemotron-3_5-Lightning`
   - `GROQ_API_KEY`: *(optional secondary fallback)*
   - `ALLOWED_ORIGINS`: `https://your-frontend.vercel.app`

---

## 2. Frontend Deployment on Vercel (Free Hobby Tier)

1. **Create Account / Login:** [https://vercel.com/](https://vercel.com/)
2. **Import Project:** Select your GitHub repository.
3. **Framework Preset:** `Vite`
4. **Root Directory:** `frontend`
5. **Build Command:** `npm run build`
6. **Output Directory:** `dist`
7. **Environment Variables:**
   - *(Optional)* Set `VITE_API_URL` to your Render backend URL if not using proxy rules.

---

## 3. Secret Management Audit

- **Frontend Bundle Security:** No server secrets or API keys are bundled into frontend assets.
- **Git Protection:** `.gitignore` explicitly excludes `.env`, `node_modules`, and local cache files.
- **Diagnostics:** The `/health` and `/api/config-status` endpoints disclose only configuration booleans (`configured: true/false`), never revealing secret values.

