from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    text: str | None = None
    url: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "text": "Congratulations! You have won a free gift card. Click here to claim!",
                "url": None
            }
        }

class AnalyzeResponse(BaseModel):
    verdict: str = Field(..., example="Likely Scam")
    explanation: str = Field(..., example="The message contains typical scam indicators such as unsolicited prize offers and urgency to click a link.")
    confidence: float = Field(..., ge=0.0, le=1.0, example=0.92)

    class Config:
        schema_extra = {
            "example": {
                "verdict": "Likely Scam",
                "explanation": "The message contains typical scam indicators such as unsolicited prize offers and urgency to click a link.",
                "confidence": 0.92,
            }
        }