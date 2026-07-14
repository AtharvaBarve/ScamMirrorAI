from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ScamMirror AI"

    # Database
    DATABASE_URL: str = f"sqlite:///./scam_mirror.db"

    # NVIDIA NIM / Claude API (if using)
    NIM_API_KEY: str = ""
    NIM_API_URL: str = "https://integrate.api.nvidia.com/v1/chat/completions"
    NIM_MODEL: str = "nemotron-3-8b-chat"

    # Cache TTL in seconds
    CACHE_TTL: int = 300

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()