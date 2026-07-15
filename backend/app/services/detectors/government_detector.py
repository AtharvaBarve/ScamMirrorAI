# detectors/government_detector.py
from typing import Dict, List, Any
from app.services.risk_engine import Detector, ThreatSignal, ThreatSeverity


class GovernmentDetector(Detector):
    """Detects impersonation of government entities."""

    # Government-related keywords
    GOVERNMENT_KEYWORDS = [
        "government", "federal", "state", "internal revenue", "irs", "social security",
        "medicare", "medicaid", "fda", "epa", "homeland security", "border patrol",
        "customs", "immigration", "passport", "visa", "tax refund", "stimulus check"
    ]

    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        text = features.get("text", "").lower()
        signals = []
        for keyword in self.GOVERNMENT_KEYWORDS:
            if keyword in text:
                signals.append(ThreatSignal(
                    name="Government Impersonation",
                    description=f"Government keyword '{keyword}' found in the message.",
                    severity=ThreatSeverity.HIGH,
                    confidence=0.85,
                    evidence=keyword
                ))
        return signals