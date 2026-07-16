from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.core.database import Base


class ThreatCampaign(Base):
    __tablename__ = "threat_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(String(20), unique=True, index=True, nullable=False)  # e.g., "TC-ABC123"
    threat_family = Column(String(50), nullable=False, index=True)  # e.g., "Financial Scam"
    report_count = Column(Integer, nullable=False, default=1)
    first_seen = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_threat_campaigns_threat_family", "threat_family"),
    )