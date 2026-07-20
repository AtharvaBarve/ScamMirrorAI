from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1 import analyze
from app.core.database import engine, Base, ensure_sqlite_schema
from app.utils.logger import setup_logging, get_logger
import logging

# Set up logging
setup_logging()
logger = get_logger(__name__)

app = FastAPI(title="ScamMirror AI API")

import os

# CORS - allow configurable origins, fallback to localhost for dev
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_schema()
    logger.info("Application started successfully")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
