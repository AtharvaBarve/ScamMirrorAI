````# CLAUDE.md - ScamMirror AI Project Memory

## 1. Project Overview
- **Project Name**: ScamMirror AI
- **Hackathon**: ET AI Hackathon 2026
- **Problem Statement**: Users need a quick, reliable way to detect scams in text messages and URLs without installing multiple tools or relying on opaque services.
- **Objective**: Build a demo‑ready web application that takes user‑provided text or URL, runs it through an AI‑powered scam detector, and returns a clear verdict, explanation, and confidence score.

## 2. Current Status
- **Project Completion**: Day 3 – MVP core functionality complete with NVIDIA NIM integration, enhanced response format, frontend display working. Routing issue resolved. Additional polishing underway.
- **Architecture Decisions**:
  - Separate backend (FastAPI) and frontend (Vite + React) repositories in a monorepo.
  - SQLite for development (easy migration to PostgreSQL later).
  - No authentication for MVP (demo only).
  - AI integration via NVIDIA NIM (with heuristic fallback).
- **Tech Stack Finalized**:
  - Frontend: React, Vite, Tailwind CSS, React Router, Axios
  - Backend: FastAPI, SQLAlchemy, Pydantic
  - Database: SQLite (dev) → PostgreSQL (prod)
  - AI: NVIDIA NIM (Nemotron‑3 8B Chat) – HTTP API; heuristic fallback if no API key
- **Features Finalized for MVP**:
  - Text analysis (scam detection)
  - URL analysis (fetch visible text, then same detection)
  - Verdict, explanation, confidence output
  - Enhanced response: category, risk factors, recommended actions, processing time
  - In‑memory TTLCache to avoid duplicate API calls during demo
  - Simple UI with copy‑to‑clipboard
- **Features Intentionally Removed (for now)**:
  - User accounts / authentication
  - Persistent history beyond SQLite (optional later)
  - File upload / image OCR
  - Batch processing
  - Advanced analytics dashboard
  - Rate limiting / logging infrastructure
  - Custom ML model training (deemed out of scope)

## 3. Final Tech Stack
| Layer       | Technology |
|-------------|------------|
| Frontend    | React 18, Vite, Tailwind CSS, React Router v6, Axios |
| Backend     | FastAPI 0.111, Uvicorn, SQLAlchemy 2.0, Pydantic v2 |
| Database    | SQLite (development), PostgreSQL (production) |
| AI          | NVIDIA NIM (Nemotron‑3 8B Chat) – HTTP API; heuristic fallback if no API key |
| DevOps      | Docker (optional), GitHub Actions (later) |
| Other       | HTTPX (async HTTP client), BeautifulSoup4 (text extraction), CacheTools (TTL cache) |

## 4. Architecture & Data Flow
1. **User Interaction** – React frontend (React component (`Analyzer`) collects input (text or URL) and sends POST request via Axios to `/api/v1/analyze`.
2. **API Layer** – FastAPI route validates request with Pydantic model.
3. **Input Handling** – If URL, `url_service.fetch_text` retrieves the page, strips scripts/styles, extracts visible text (capped at ~3000 chars). Results cached per URL.
4. **Caching** – Before calling AI, a SHA256 hash of (`input_type`, `content`) is checked in an in‑memory TTLCache (default 5 min). If hit, cached result is returned.
5. **AI Service** – `claude_service.call_nim` builds a few‑shot prompt and calls NVIDIA NIM endpoint (or heuristic fallback). The model is instructed to output JSON `{verdict, explanation, confidence, category, risk_factors, recommended_actions, processing_time}`.
6. **Persistence** – Successful result is saved to `analysis_history` table (SQLAlchemy ORM) for possible later review.
7. **Response** – Pydantic model serializes the result back to the frontend.
8. **UI Rendering** – `ResultCard` displays verdict (color‑coded), confidence bar, explanation, category, risk factors (as chips), recommended actions (as chips), processing time, and copy button.

### Data Flow Diagram (textual)
```
[React UI] --Axios POST /api/v1/analyze--> [FastAPI Router]
        |                                      |
        |<-- JSON Response (verdict, etc.) ----|
        |
        v
[URL Service (if URL)] <--HTTP GET--> [Target Website]
        |
        v
[Cache (TTL)] <--lookup/store--> [AI Service (NIM/Heuristic)]
        |
        v
[DB Layer (SQLAlchemy)] <--INSERT--> [analysis_history table]
        |
        v
[Return JSON to caller]
```

## 5. Folder Structure
```
scam-mirror-ai/
├─ backend/
│  ├─ app/
│  │  ├─ main.py                 # FastAPI entry point
│  │  ├─ core/
│  │  │  ├─ config.py            # Settings (pydantic-settings)
│  │  │  ├─ database.py          # Engine, Session, Base
│  │  │  └─ security.py          # placeholder for API‑key handling
│  │  ├─ models/                 # SQLAlchemy models
│  │  │  └─ analysis.py          # AnalysisHistory table
│  │  ├─ routers/
│  │  │  ├─ __init__.py
│  │  │  └─ v1/
│  │  │     ├─ __init__.py
│  │  │  └─ analyze.py           # POST /api/v1/analyze
│  │  ├─ schemas/
│  │  │  ├─ __init__.py
│  │  │  └─ analyze.py           # Pydantic request/response models
│  │  ├─ services/
│  │  │  ├─ __init__.py
│  │  │  ├─ claude_service.py    # NIM wrapper (with heuristic fallback)
│  │  │  ├─ url_service.py       # HTTP fetch + text extraction
│  │  │  └─ cache_service.py     # Thin wrapper over cachetools.TTLCache
│  ├─ alembic/                   # Alembic migration files (empty for now)
│  ├─ requirements.txt
│  ├─ .env.example
│  ├─ .env                       # local dev (not committed)
│  ├─ Dockerfile                 # optional
│  └─ scam_mirror.db             # SQLite file (created on first run)
├─ frontend/
│  ├─ public/
│  │  └─ index.html
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ Layout.jsx           # wrapper with header/footer
│  │  │  ├─ Analyzer.jsx         # input form + hook call
│  │  │  ├─ ResultCard.jsx       # display result + copy button
│  │  │  └─ Spinner.jsx          # loading indicator
│  │  ├─ hooks/
│  │  │  └─ useAnalyze.js        # Axios wrapper
│  │  ├─ routes/
│  │  │  └─ index.jsx            # React Router v6 config
│  │  ├─ utils/
│  │  │  └─ constants.js         # API base (empty, proxied by Vite)
│  │  ├─ App.jsx                 # router provider
│  │  ├─ main.jsx                # React entry
│  │  └─ index.css               # Tailwind imports
│  ├─ index.html
│  ├─ package.json
│  ├─ vite.config.js             # proxy to backend
│  ├─ .env.example
│  └─ Dockerfile                 # optional
├─ docker-compose.yml            # optional local dev
├─ README.md
└─ .gitignore
```

## 6. Database Schema
```sql
-- Table: analysis_history
CREATE TABLE analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_type VARCHAR(10) NOT NULL,   -- 'text' or 'url'
    input_content TEXT NOT NULL,       -- truncated to first 500 chars for storage
    verdict VARCHAR(20) NOT NULL,      -- e.g., 'Likely Scam'
    explanation TEXT NOT NULL,
    confidence FLOAT NOT NULL,         -- 0.0 – 1.0
    category VARCHAR(50),              -- e.g., 'Financial Scam'
    risk_factors TEXT,                 -- JSON array of strings
    recommended_actions TEXT,          -- JSON array of strings
    processing_time FLOAT,             -- seconds
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ix_analysis_history_created_at ON analysis_history(created_at);
```
*SQLAlchemy model mirrors the above (see `backend/app/models/analysis.py`).*

## 7. REST API Design
| Method | Endpoint            | Description                                    | Request Body (JSON)                     | Success Response (200)                              |
|--------|---------------------|-----------------------------------------------|-----------------------------------------|------------------------------------------------------|
| POST   | `/api/v1/analyze`   | Analyze text or URL for scam likelihood       | `{ "text?: string, "url?: string }`     | `{ verdict, explanation, confidence, category, risk_factors, recommended_actions, processing_time }` |
| GET    | `/api/v1/health`    | Simple liveness check                         | –                                       | `{ status: "ok" }`                                   |
| GET    | `/api/v1/history`   | *(Optional, not in MVP)* return recent rows   | Query `?limit=20`                       | Array of `{ id, input_type, verdict, confidence, created_at }` |

*All responses are plain JSON; errors follow standard HTTP codes with JSON body `{ "detail": "..."}`.*

## 8. AI Pipeline (NIM / Heuristic)
1. **Prompt Engineering** – System + few‑shot examples instruct the model to output strict JSON.
2. **Request** – POST to `NIM_API_URL` with JSON payload:
   ```json
   {
     "model": "nemotron-3-8b-chat",
     "messages": [{ "role": "user", "content": "<prompt>" }],
     "temperature": 0.0,
     "max_tokens": 256,
     "response_format": { "type": "json_object" }
   }
   ```
3. **Response Parsing** – Extract `choices[0].message.content`, parse JSON; on failure, fallback to heuristic.
4. **Heuristic Fallback (if no API key)** – simple keyword scan (free, prize, urgent, click here, etc.) to produce a plausible verdict.
5. **Caching** – Results cached by input hash to reduce API calls during live demo.
6. **Enhanced Response** – Model instructed to return additional fields: category, risk factors, recommended actions, processing time.

## 9. Development Rules
- **No Over‑Engineering**: Only add what is needed for the demo.
- **Complexity Cap**: Keep overall architectural complexity ≤ 6/10 (current estimate ~4).
- **Ship First**: Prioritize end‑to‑end working flow over polish; polish only after core works.
- **Preserve Architecture**: Do not change layering or tech choices unless a blocker proves them impossible.
- **Prefer Maintainability**: Favor clear, minimal code; avoid premature abstractions.
- **Dependency Discipline**: Add new libraries only after explicit justification; avoid heavyweight frameworks.
- **Testing**: Manual testing is sufficient for MVP; automated tests can be added post‑hackathon if time permits.

## 10. Coding Standards
- **Python**: Follow PEP 8; use `ruff` or `flake8` if available; keep lines < 88 char; docstrings for public functions.
- **JavaScript/React**: Use functional components with hooks; ES‑2022; `eslint` with `react/recommended`; no `any` in TypeScript (we’re using plain JS, so keep variable names descriptive).
- **Naming**: `snake_case` for Python files/variables, `camelCase` for JS variables, `PascalCase` for React components.
- **Commits**: Atomic, descriptive messages; prefix with area if helpful (e.g., `feat: add URL fetch`, `fix: cache key collision`).
- **Formatting**: Use built‑in formaters (`black` for Python, `prettier` for JS) – run before commit if installed.
- **Environment Variables**: Keep secrets out of repo; use `.env.example` for template; never commit actual keys.

## 11. Current Progress
**Completed (Day 1)**
- [x] Repository initialized with backend/frontend folders
- [x] Backend: FastAPI app with CORS, SQLAlchemy setup, Alembic ready
- [x] Database model `AnalysisHistory`
- [x] Pydantic schemas for request/response
- [x] Service layer: `claude_service` (mock/heuristic), `url_service` (fetch+extract), `cache_service` (TTLCache)
- [x] API router `/api/v1/analyze` that orchestrates flow, caches, stores to DB
- [x] Health endpoint `/api/v1/health`
- [x] Backend requirements.txt and .env.example
- [x] Frontend: Vite + React + Tailwind setup
- [x] Frontend components: Layout, Analyzer, ResultCard, Spinner
- [x] Frontend hook `useAnalyze` wrapping Axios
- [x] Routing with React Router v6 (single page for now)
- [x] Proxy configured in `vite.config.js` to forward `/api/*` to backend
- [x] Basic styling with Tailwind (responsive, centered card)
- [x] Dockerfiles for both services (optional)
- [x] docker‑compose.yml (optional)
- [x] README with setup instructions
- [x] Initial git commit

**Completed (Day 2)**
- [x] Integrated real NVIDIA NIM API call with retry logic and heuristic fallback
- [x] Enhanced response format to include category, risk factors, recommended actions, processing time
- [x] Updated frontend ResultCard to display all new fields
- [x] Fixed frontend routing to properly serve index.html for client-side routes
- [x] Verified end-to-end functionality for both text and URL analysis
- [x] Confirmed fallback heuristic works when API key missing/invalid

**Completed (Day 3)**
- [x] Improved URL fetch: added timeout, better content extraction, error UI
- [x] Added simple history list (last 5) to the sidebar
- [x] Added loading skeletons while waiting for AI response
- [ ] Implement dark‑mode toggle (optional)
- [ ] Write a deployment script (Docker Compose or platform‑specific)
- [ ] Record a 60‑second demo video
- [ ] Finalize README with troubleshooting FAQ
- [ ] (Optional) Add basic logging to file/stdout
- [ ] (Optional) Add rate‑limiting middleware for NIM calls

## 12. Daily Progress Log
**Date: 2026-07-14**
- **Completed**: Improved URL fetch with timeout and better content extraction; added history sidebar; implemented loading skeletons; verified all Day 3 in-progress tasks completed.
- **Decisions**: Prioritized user experience improvements; maintained backward compatibility; ensured robust error handling for edge cases.
- **Bugs Fixed**: Fixed timeout handling in URL service; improved loading state transitions; corrected history sidebar styling on mobile.
- **Next Day's Tasks**: Implement dark‑mode toggle; create deployment script; record demo video; finalize README.

**Date: 2025-07-14**
- **Completed**: Integrated real NVIDIA NIM API call with retry logic and heuristic fallback; enhanced response format with new fields; fixed frontend routing issue where path in vite.config.js).
- **Next Day's Tasks**: Improve URL fetch robustness; add history sidebar; implement loading skeletons.

**Date: 2025-07-13**
- **Completed**: Repository initialized with backend/frontend folders; basic backend API with FastAPI; frontend skeleton with Vite + React; integration stubs for services.
- **Decisions**: Chose separate backend/frontend in monorepo; selected SQLite for dev; opted for heuristic fallback initially.
- **Bugs Fixed**: Initial dependency conflicts resolved (SQLAlchemy version, pydantic-settings).
- **Next Day's Tasks**: Implement real NVIDIA NIM API integration; enhance response format; update frontend display.

## 13. Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| NVIDIA NIM API key unavailable or rate‑limited | Medium | High (demo could fail) | Keep heuristic fallback; monitor usage; if key missing, clearly indicate demo mode. |
| URL fetching blocked by target site (CORS, bot protection) | Medium | Medium | Provide fallback message; limit fetched size; use common user‑agent; optionally use a third‑party text extraction API (if time). |
| Time‑box overflow due to perfectionism | High | Medium | Strict adherence to development rules; daily timeboxing; demo‑first mindset. |
| Dependencies conflict (e.g., SQLAlchemy version) | Low | Medium | Pin versions in `requirements.txt`; use virtualenv; test import after each change. |
| Inaccurate scam detection leading to poor demo | Low | High | Rely on strong prompt engineering; keep demo examples simple and clearly scam/safe. |

## 14. TODO List (ordered by priority)
- [ ] Implement dark‑mode toggle (optional)
- [ ] Write a deployment script (Docker Compose or platform‑specific)
- [ ] Record a 60‑second demo video
- [ ] Finalize README with troubleshooting FAQ
- [ ] (Optional) Add basic logging to file/stdout
- [ ] (Optional) Add rate‑limiting middleware for NIM calls

## 15. Definition of MVP (Minimum Viable Product)
A deployable web app where a user can:
1. Paste a text snippet or enter a URL.
2. Press **Analyze**.
3. Receive a clear verdict (**Likely Scam**, **Likely Safe**, or **Uncertain**) with a short explanation and a confidence percentage.
4. Copy the result to clipboard.
All of this works end‑to‑end (frontend → backend → AI → DB → response) without authentication, using a SQLite backend, and with a fallback heuristic if the external AI API is not available.

## 16. Definition of Done (for this Hackathon)
- The MVP is fully functional as described above.
- The application can be run locally via `docker compose up` (or separate backend/frontend startup scripts).
- A short demo video (< 2 min) shows the flow for both a text example and a URL example.
- The repository is publicly accessible with a clear `README.md` explaining how to run the project.
- No known blocking bugs; edge‑cases produce graceful error messages.
- The code respects the complexity and minimalism guidelines laid out in this document.
- The `CLAUDE.md` file is up‑to‑date reflecting the final state.

---  ``
*End of CLAUDE.md – update```` this file at the end of each work session to keep it as the single source of truth.*