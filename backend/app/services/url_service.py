import httpx
from bs4 import BeautifulSoup
import asyncio
from app.core.config import settings
from app.services.cache_service import get, set

async def fetch_text(url: str) -> str:
    """
    Fetch the URL and extract visible text.
    Uses a simple heuristic: get <title> and main paragraph text.
    Limits the returned text to first 3000 characters to keep prompt size manageable.
    Results are cached for the duration of CACHE_TTL.
    """
    # Check cache first
    cache_key = f"url_text:{url}"
    cached = get(cache_key)
    if cached is not None:
        return cached

    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=httpx.Timeout(10.0, read=20.0),
            headers={"User-Agent": "ScamMirrorBot/1.0"},
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            html = resp.text

        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        # Remove script and style elements
        for tag in soup(["script", "style", "noscript", "iframe", "svg", "canvas"]):
            tag.decompose()

        # Get title
        title = soup.title.string if soup.title else ""

        # Prefer main content: look for <article>, <main>, or fallback to body
        main = soup.find("article") or soup.find("main") or soup.body
        if main:
            # Get text with separator space
            text = main.get_text(separator=" ", strip=True)
        else:
            text = soup.get_text(separator=" ", strip=True)

        # Combine title and text
        combined = f"{title}\n{text}".strip()

        # Limit length
        max_chars = 3000
        if len(combined) > max_chars:
            combined = combined[:max_chars] + "... [truncated]"

        # Cache
        set(cache_key, combined)
        return combined
    except Exception as e:
        # In case of any error, return an empty string or a placeholder.
        # The caller can decide to treat this as unsafe or ask user to retry.
        return f"[Error fetching URL: {str(e)}]"