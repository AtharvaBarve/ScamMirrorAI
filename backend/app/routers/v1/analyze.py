from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import hashlib
import json

from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.core.database import get_db, Base
from app.models.analysis import AnalysisHistory
from app.services.hybrid_service import hybrid_service
from app.services.url_service import fetch_text
from app.utils.input_validator import validate_and_sanitize_text
from app.services.threat_intelligence_service import ThreatIntelligenceService

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
    # Validate input - exactly one of text or url must be provided
    if not payload.text and not payload.url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'text' or 'url' must be provided.",
        )

    if payload.text and payload.url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide either 'text' or 'url', not both.",
        )

    # Determine input type and content
    if payload.text:
        input_type = "text"
        # Validate and sanitize text input
        sanitized_text, error_msg = validate_and_sanitize_text(payload.text)
        if error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid text input: {error_msg}"
            )
        input_content = sanitized_text
        original_url = None
    elif payload.url:
        input_type = "url"
        # Fetch and extract text from URL
        input_content = await fetch_text(payload.url)
        # Check if fetch_text returned an error message
        if input_content.startswith("[Error:"):
            # Extract the error message for better user feedback
            error_message = input_content[8:-1] if input_content.endswith("]") else input_content[8:]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to process URL: {error_message}"
            )
        # Validate and sanitize the extracted text
        sanitized_text, error_msg = validate_and_sanitize_text(input_content)
        if error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid content extracted from URL: {error_msg}"
            )
        input_content = sanitized_text
        original_url = payload.url
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'text' or 'url' must be provided.",
        )

    # Truncate storage to first 500 chars for DB
    stored_content = input_content[:500]

    # Build cache key
    cache_key = _hash_input(input_type, input_content)
    from app.services.cache_service import get, set
    cached_result = get(cache_key)
    if cached_result is not None:
        # Return cached result
        return AnalyzeResponse(**cached_result)

    # Call the hybrid service to get analysis
    result_dict = await hybrid_service.analyze(
        input_type=input_type,
        input_content=input_content,
        original_url=original_url,
    )

    # Process threat campaign if category is present
    threat_campaign_id = None
    community_intelligence_data = None
    if result_dict.get("category"):
        # Use threat intelligence service to handle campaign logic
        threat_service = ThreatIntelligenceService(db)
        campaign = threat_service.get_or_create_campaign(result_dict["category"])
        threat_campaign_id = campaign.id
        community_intelligence_data = threat_service.get_campaign_intelligence(campaign)

    # Persist to DB
    db_obj = AnalysisHistory(
        input_type=input_type,
        input_content=stored_content,
        verdict=result_dict["verdict"],
        explanation=result_dict["explanation"],
        confidence=float(result_dict["confidence"]),
        category=result_dict["category"],
        risk_factors=json.dumps(result_dict["risk_factors"]),
        recommended_actions=json.dumps(result_dict["recommended_actions"]),
        processing_time=result_dict["processing_time"],
        threat_campaign_id=threat_campaign_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Add community intelligence to the result dict if we have a campaign
    if community_intelligence_data:
        result_dict["community_intelligence"] = community_intelligence_data

    # Cache the result (store as dict)
    set(cache_key, result_dict)

    return AnalyzeResponse(**result_dict)