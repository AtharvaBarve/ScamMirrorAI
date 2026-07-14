from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1 import analyze
from app.core.database import engine, Base

app = FastAPI(title="ScamMirror AI API")

# CORS - allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    # Create database tables
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}