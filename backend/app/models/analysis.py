from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Index, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    input_type = Column(String(10), nullable=False)  # "text" or "url"
    input_content = Column(Text, nullable=False)     # store truncated input
    verdict = Column(String(20), nullable=False)     # e.g., "Likely Scam"
    explanation = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)       # 0.0 - 1.0
    category = Column(String(50), nullable=True)     # e.g., "Financial Scam"
    risk_factors = Column(Text, nullable=True)       # JSON array of strings
    recommended_actions = Column(Text, nullable=True) # JSON array of strings
    processing_time = Column(Float, nullable=True)   # seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Foreign key to ThreatCampaign
    threat_campaign_id = Column(Integer, ForeignKey("threat_campaigns.id"), nullable=True, index=True)

    __table_args__ = (Index("ix_analysis_history_created_at", "created_at"),)