from sqlalchemy.orm import Session
from app.models.threat_campaign import ThreatCampaign
from uuid import uuid4


class ThreatIntelligenceService:
    """Service for managing threat intelligence and campaign tracking."""

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_campaign(self, threat_family: str) -> ThreatCampaign:
        """
        Get existing threat campaign for family or create new one.

        Args:
            threat_family: The threat category/family

        Returns:
            ThreatCampaign: The campaign object
        """
        campaign = self.db.query(ThreatCampaign).filter(
            ThreatCampaign.threat_family == threat_family
        ).first()

        if campaign:
            # Update existing campaign
            campaign.report_count += 1
            # last_seen will update automatically via onupdate=func.now()
            self.db.add(campaign)
        else:
            # Create new campaign
            threat_id = f"TC-{uuid4().hex[:8].upper()}"
            campaign = ThreatCampaign(
                threat_id=threat_id,
                threat_family=threat_family,
                report_count=1
            )
            self.db.add(campaign)
            # Flush to get the campaign ID if it's new
            self.db.flush()

        return campaign

    def get_campaign_intelligence(self, campaign: ThreatCampaign) -> dict:
        """
        Convert campaign object to intelligence dictionary for API response.

        Args:
            campaign: The ThreatCampaign object

        Returns:
            dict: Intelligence data for API response
        """
        return {
            "threat_id": campaign.threat_id,
            "threat_family": campaign.threat_family,
            "report_count": campaign.report_count,
            "first_seen": campaign.first_seen.isoformat() if campaign.first_seen else None,
            "last_seen": campaign.last_seen.isoformat() if campaign.last_seen else None
        }