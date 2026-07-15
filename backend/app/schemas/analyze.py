from pydantic import BaseModel, Field
from typing import List, Optional

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
    category: str = Field(..., example="Financial Scam")
    risk_factors: List[str] = Field(default_factory=list, example=["Urgency", "Unsolicited offer"])
    recommended_actions: List[str] = Field(default_factory=list, example=["Do not click any links", "Delete the message"])
    processing_time: float = Field(..., example=1.23)

    class Config:
        json_schema_extra = {
            "example": {
                "verdict": "Likely Scam",
                "explanation": "The message contains typical scam indicators such as unsolicited prize offers and urgency to click a link.",
                "confidence": 0.92,
                "category": "Financial Scam",
                "risk_factors": ["Urgency", "Unsolicited offer"],
                "recommended_actions": ["Do not click any links", "Delete the message"],
                "processing_time": 1.23
            }
        }