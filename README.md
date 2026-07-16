# ScamMirror AI

AI-powered scam detection tool built for the ET AI Hackathon.

## Tech Stack

- **Frontend**: React + Vite + Tailwind CSS + React Router + Axios + date-fns
- **Backend**: FastAPI + SQLAlchemy (SQLite) + Pydantic
- **AI**: NVIDIA NIM (or Anthropic Claude via API) – 0‑shot scam detection via prompt engineering
- **Other**: HTTPX for URL fetching, BeautifulSoup4 for text extraction, CacheTools for simple in‑memory caching

## Features (MVP)

- ✅ Analyze free‑form text messages for scam likelihood
- ✅ Analyze a URL by fetching its visible text and running the same detection
- ✅ Returns verdict (`Likely Scam`, `Likely Safe`, `Uncertain`), explanation, and confidence score
- ✅ Enhanced threat intelligence dashboard with:
  - Threat Level visualization (confidence gauge)
  - Detailed explanation of reasoning
  - Detected threat signals (risk factors)
  - Community Threat Intelligence (tracking similar threats)
  - Protect Others (anonymous reporting and sharing)
  - Threat Report generation (copy/download)
- ✅ Context-based state management for efficient prop passing
- ✅ Responsive UI with copy-to-clipboard functionality
- ✅ Input sanitization and validation for improved security

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+ (or any recent LTS)
- Git

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit .env if you have a NIM API key
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
OpenAPI docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev   # Vite dev server, proxies to backend at http://localhost:8000
```

Open http://localhost:5173 in your browser.

### Environment Variables

Backend (`backend/.env`):
- `DATABASE_URL` – SQLAlchemy URL (default SQLite file)
- `NIM_API_KEY` – optional; if omitted a heuristic fallback is used
- `NIM_API_URL` – NVIDIA NIM endpoint
- `NIM_MODEL` – model name (e.g., `nemotron-3-8b-chat`)
- `CACHE_TTL` – seconds for in‑memory cache (default 300)

Frontend (`frontend/.env`):
- `VITE_API_BASE` – base API path (default `/api`)

### Production Build (Frontend)

```bash
cd frontend
npm run build
# Serve the dist folder with any static file server (e.g., serve -s dist)
```

### Docker (optional)

A simple `docker-compose.yml` is provided to run both services together.

```bash
docker compose up --build
```

## Recent Improvements (July 15, 2026)

- **Context-Based State Management**: Implemented React Context for global state management, eliminating prop drilling and improving performance
- **Enhanced Threat Intelligence Service**: Created dedicated service layer for threat campaign management
- **Modular Backend Architecture**: Separated threat intelligence logic into its own service for better maintainability
- **Improved Date Handling**: Integrated date-fns for consistent date formatting and manipulation
- **Cleaner Component Structure**: All dashboard components now consume context directly
- **Retained Backward Compatibility**: Existing hooks and APIs continue to work as expected

## Project Structure

```
scam-mirror-ai/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/          # config, database, security
│  │  ├─ models/        # SQLAlchemy models (AnalysisHistory, ThreatCampaign)
│  │  ├─ routers/       # API versioning
│  │  ├─ schemas/       # Pydantic models
│  │  ├─ services/      # Claude (NIM), URL fetch, cache, threat intelligence
│  │  └─ models/        # Added ThreatCampaign model
│  ├─ alembic/          # migrations (future)
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend/
│  ├─ public/
│  ├─ src/
│  │  ├─ components/   # UI components
│  │  ├─ context/      # NEW: React Context for state management
│  │  ├─ hooks/        # custom React hooks (updated to use context)
│  │  ├─ routes/       # React Router v6 routes
│  │  ├─ App.jsx       # Wrapped with AnalysisProvider
│  │  ├─ main.jsx
│  │  └─ index.css
│  ├─ index.html
│  ├─ package.json     # Added date-fns dependency
│  ├─ vite.config.js
│  └─ .env.example
└─ README.md
```

## Notes & Limitations

- The AI component relies on a third‑party NIM API. If no key is provided, a rule‑based fallback is used for demo purposes.
- URL fetching is a best‑effort extractor (strips scripts/styles, takes first ~3000 characters). It may fail on sites that block bots or require JavaScript rendering.
- No authentication or persistence of analysis history beyond the SQLite table (optional history UI can be added later).
- Designed for a single‑demo scenario; scaling to many concurrent users would require a proper cache (Redis) and rate‑limiting.

## License

MIT – feel free to fork and adapt for your own hackathon projects.