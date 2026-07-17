import httpx
from bs4 import BeautifulSoup
import asyncio
from app.core.config import settings
from app.services.cache_service import get, set
import logging

logger = logging.getLogger(__name__)

async def fetch_text(url: str) -> str:
    """
    Fetch the URL and extract visible text.
    Uses a simple heuristic: get <title> and main paragraph text.
    Limits the returned text to first 3000 characters to keep prompt size manageable.
    Results are cached for the duration of CACHE_TTL.
    """
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        return "[Error: Invalid URL format. Please provide a URL starting with http:// or https://]"

    # Heuristics: Domain Intelligence
    suspicious_metadata = []
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # 1. Suspicious TLDs
    if domain.endswith(('.xyz', '.top', '.club', '.online', '.site', '.click')):
        suspicious_metadata.append("WARNING: URL uses a highly suspicious top-level domain often associated with spam/scams.")
        
    # 2. IP-Based URLs
    import re
    if re.match(r'^[\d\.]+(:\d+)?$', domain):
        suspicious_metadata.append("WARNING: URL uses a raw IP address instead of a registered domain name (common in phishing).")
        
    # 3. URL Shorteners
    shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'ow.ly', 'is.gd']
    if any(s in domain for s in shorteners):
        suspicious_metadata.append("WARNING: URL is masked using a link shortener service to hide the true destination.")

    # Check cache first
    cache_key = f"url_text:{url}"
    cached = get(cache_key)
    if cached is not None:
        return "\n".join(suspicious_metadata) + "\n\n" + cached if suspicious_metadata else cached

    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=httpx.Timeout(10.0, read=20.0),
            headers={"User-Agent": "ScamMirrorBot/1.0"},
        ) as client:
            try:
                resp = await client.get(url)
                resp.raise_for_status()
            except httpx.TimeoutException:
                return "[Error: Request timed out. Please try again later or check the URL.]"
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return "[Error: Page not found (404). Please check the URL and try again.]"
                elif e.response.status_code == 403:
                    return "[Error: Access forbidden (403). The website may be blocking automated access.]"
                elif e.response.status_code >= 500:
                    return f"[Error: Server error ({e.response.status_code}). Please try again later.]"
                else:
                    return f"[Error: HTTP {e.response.status_code}. Please check the URL and try again.]"
            except httpx.RequestError as e:
                return "[Error: Unable to connect to the server. Please check the URL and your internet connection.]"

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
            
        if suspicious_metadata:
            combined = "\n".join(suspicious_metadata) + "\n\n--- Extracted Content ---\n" + combined

        # Cache
        set(cache_key, combined)
        return combined
    except Exception as e:
        logger.error(f"Unexpected error fetching URL {url}: {str(e)}")
        return "[Error: An unexpected error occurred while processing the URL. Please try again.]"