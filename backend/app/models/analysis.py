from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Index
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
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("ix_analysis_history_created_at", "created_at"),)