from pydantic import BaseModel, Field
from typing import List, Optional


class CommunityIntelligence(BaseModel):
    threat_id: str
    threat_family: str
    report_count: int
    first_seen: str  # ISO format string
    last_seen: str   # ISO format string


class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Congratulations! You have won a free gift card. Click here to claim!",
                "url": None
            }
        }


class AnalyzeResponse(BaseModel):
    verdict: str = Field(..., example="Likely Scam")
    explanation: str = Field(..., example="The message contains typical scam indicators such as unsolicited prize offers and urgency to click a link.")
    confidence: float = Field(..., ge=0.0, le=1.0, example=0.92)
    category: Optional[str] = Field(None, example="Financial Scam")
    risk_factors: List[str] = Field(default_factory=list, example=["Urgency", "Unsolicited offer"])
    recommended_actions: List[str] = Field(default_factory=list, example=["Do not click any links", "Delete the message"])
    processing_time: float = Field(..., example=1.23)
    community_intelligence: Optional[CommunityIntelligence] = None

    class Config:
        json_schema_extra = {
            "example": {
                "verdict": "Likely Scam",
                "explanation": "The message contains typical scam indicators such as unsolicited prize offers and urgency to click a link.",
                "confidence": 0.92,
                "category": "Financial Scam",
                "risk_factors": ["Urgency", "Unsolicited offer"],
                "recommended_actions": ["Do not click any links", "Delete the message"],
                "processing_time": 1.23,
                "community_intelligence": {
                    "threat_id": "TC-ABC123",
                    "threat_family": "Financial Scam",
                    "report_count": 5,
                    "first_seen": "2026-07-14T10:30:00Z",
                    "last_seen": "2026-07-15T14:22:00Z"
                }
            }
        }