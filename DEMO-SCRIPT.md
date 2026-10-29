# DEMO-SCRIPT.md — Refactor.ai
**Competition:** Nebius × NVIDIA Global AI Hackathon  
**Track:** Coding and Agentic Engineering  
**Target Duration:** 2 minutes 45 seconds (Under the 3-minute strict limit)  

---

## 🎬 Pre-Recording Checklist
- [ ] Backend running: `python3 backend/main.py`
- [ ] Frontend running: `cd frontend && npm run dev`
- [ ] Browser open at `http://localhost:5173` (Full screen 1080p, 100% zoom)
- [ ] Microphone tested and clear
- [ ] Clean browser tab (no bookmarks bar, clean developer console)

---

## ⏱️ Video Script with Timestamps

### [0:00 - 0:25] The Problem & Introduction
* **Visual:** Open on the Refactor.ai header, showing the clean dark IDE interface and the tag line: *"Autonomous Code Refactoring Platform • Nebius Token Factory & NVIDIA Nemotron"*.
* **Speaker:**  
  *"Hey everyone! Developers spend over 40% of their working hours reading, untangling, and fixing legacy code. Code reviews drag on for days because manual refactoring is repetitive and risky.*  
  *Meet **Refactor.ai**—an autonomous code refactoring platform built for the **Nebius × NVIDIA Global AI Hackathon** in the **Coding and Agentic Engineering** track. It's powered directly by **NVIDIA open-source models** running on **Nebius Token Factory** high-performance open infrastructure."*

---

### [0:25 - 1:15] Demo Journey 1: Performance & Readability Refactor
* **Visual:**  
  1. Click the **"Python Order"** sample snippet button.  
  2. Show messy code with single-letter variables (`t`, `x`, `y`, `z`) and unoptimized logic.
  3. Point to the **Target Goal** selector and select **"📖 Readability"**.
  4. Click the primary **"⚡ Refactor Code"** button.
  5. The UI shows an active progress state and instantly displays the refactored code alongside the provider indicator badge.
* **Speaker:**  
  *"Let's start with a classic scenario: a messy Python billing function full of magic numbers, single-letter variables, and zero documentation. We pick the 'Readability' goal and hit Refactor.*  
  *Look at the output: Refactor.ai automatically introduces PEP 484 type annotations, extracts magic numbers into constants, and structures the return contract.*  
  *Next, let's switch to the **Insights & Explanations** tab. Notice that instead of just dumping code, Refactor.ai provides line-by-line explanations, highlights performance improvements, and warns of any risk tradeoffs."*

---

### [1:15 - 1:55] Demo Journey 2: Security Audit (SQL Injection Mitigation)
* **Visual:**  
  1. Click **"SQL Vuln"** sample code. Show `SELECT * FROM users WHERE id = '{user_id}'`.
  2. Select the **"🛡️ Security Audit"** goal.
  3. Click **"⚡ Refactor Code"**.
  4. Show the sanitized parameterized query (`WHERE id = ?`), boundary check, and projected column selection.
* **Speaker:**  
  *"Now let's test a critical engineering challenge: security. We load an active SQL injection vulnerability.*  
  *With one click on 'Security Audit', the model identifies the CWE-89 injection risk, replaces raw string formatting with parameterized prepared statements, and sanitizes incoming user input. Developers can immediately copy the code or download the file directly into their project."*

---

### [1:55 - 2:30] Technical Architecture: NVIDIA Nemotron + Nebius Infrastructure
* **Visual:**  
  1. Highlight the **Provider Badge** in the top-right corner.
  2. Bring up the architecture diagram or the `/api/config-status` endpoint in a split tab.
* **Speaker:**  
  *"Under the hood, Refactor.ai features a resilient multi-tier architecture:*  
  *Our primary engine is the **NVIDIA Nemotron open-source model** family (`nvidia/Nemotron-3_5-Lightning`) accessed through **Nebius Token Factory's** high-throughput OpenAI-compatible API.*  
  *For developer resilience, we've integrated a secondary fallback with **Groq** and an offline deterministic engine, ensuring zero downtime during review.*  
  *Every request is validated, strictly bounded, and never executes untrusted code on the server."*

---

### [2:30 - 2:45] Conclusion & Future Vision
* **Visual:** Return to the full Refactor.ai interface.
* **Speaker:**  
  *"Refactor.ai demonstrates how open AI models and open infrastructure can supercharge developer productivity. The entire project is open-source under the MIT license, backed by a 100% passing automated test suite.*  
  *Thank you Nebius and NVIDIA for the incredible platform!"*
