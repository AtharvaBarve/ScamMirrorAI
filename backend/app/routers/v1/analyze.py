from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import hashlib

from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.core.database import get_db, Base
from app.models.analysis import AnalysisHistory
from app.services.claude_service import ClaudeService
from app.services.url_service import fetch_text
from app.services.cache_service import get, set

router = APIRouter()

def _hash_input(input_type: str, content: str) -> str:
    """Create a deterministic cache key from input."""
    return hashlib.sha256(f"{input_type}:{content}".encode()).hexdigest()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze text or URL for scam likelihood.
    """
    # Determine input type and content
    if payload.text:
        input_type = "text"
        input_content = payload.text.strip()
    elif payload.url:
        input_type = "url"
        # Fetch and extract text from URL
        input_content = await fetch_text(payload.url)
        if not input_content or input_content.startswith("[Error"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not fetch or extract content from the provided URL.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'text' or 'url' must be provided.",
        )

    # Truncate storage to first 500 chars for DB
    stored_content = input_content[:500]

    # Build cache key
    cache_key = _hash_input(input_type, input_content)
    cached_result = get(cache_key)
    if cached_result is not None:
        # Return cached result
        return AnalyzeResponse(**cached_result)

    # Call the AI service (ClaudeService) to get analysis
    result_dict = await ClaudeService.call_nim(input_content)

    # Ensure result dict has expected keys
    if not all(k in result_dict for k in ("verdict", "explanation", "confidence")):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid response from AI service.",
        )

    # Persist to DB
    db_obj = AnalysisHistory(
        input_type=input_type,
        input_content=stored_content,
        verdict=result_dict["verdict"],
        explanation=result_dict["explanation"],
        confidence=float(result_dict["confidence"]),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Cache the result (store as dict)
    set(cache_key, result_dict)

    return AnalyzeResponse(**result_dict)