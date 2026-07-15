# ScamMirror AI

AI-powered scam detection tool built for the ET AI Hackathon.

## Tech Stack

- **Frontend**: React + Vite + Tailwind CSS + React Router + Axios
- **Backend**: FastAPI + SQLAlchemy (SQLite) + Pydantic
- **AI**: NVIDIA NIM (or Anthropic Claude via API) – 0‑shot scam detection via prompt engineering
- **Other**: HTTPX for URL fetching, BeautifulSoup4 for text extraction, CacheTools for simple in‑memory caching

## Features (MVP)

- ✅ Analyze free‑form text messages for scam likelihood
- ✅ Analyze a URL by fetching its visible text and running the same detection
- ✅ Returns verdict (`Likely Scam`, `Likely Safe`, `Uncertain`), explanation, and confidence score
- ✅ Basic history (in‑memory cache) to avoid duplicate API calls during demo
- ✅ Responsive UI with copy‑to‑clipboard result

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

## Project Structure

```
scam-mirror-ai/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/          # config, database, security
│  │  ├─ models/        # SQLAlchemy models
│  │  ├─ routers/       # API versioning
│  │  ├─ schemas/       # Pydantic models
│  │  └─ services/      # Claude (NIM), URL fetch, cache
│  ├─ alembic/          # migrations (future)
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend/
│  ├─ public/
│  ├─ src/
│  │  ├─ components/   # UI components (Analyzer, ResultCard, Spinner, Layout)
│  │  ├─ hooks/        # custom React hooks
│  │  ├─ routes/       # React Router v6 routes
│  │  ├─ utils/        # constants
│  │  ├─ App.jsx
│  │  ├─ main.jsx
│  │  └─ index.css
│  ├─ index.html
│  ├─ package.json
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

MIT – feel free to fork and adapt for your own hackathon projects.# ScamMirrorAI
