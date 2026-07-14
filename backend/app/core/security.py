from app.core.config import settings

def get_anthropic_api_key() -> str:
    return settings.ANTHROPIC_API_KEY