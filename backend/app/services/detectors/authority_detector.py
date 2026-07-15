# detectors/authority_detector.py
from typing import Dict, List, Any
from app.services.risk_engine import Detector, ThreatSignal, ThreatSeverity


class AuthorityDetector(Detector):
    """Detects impersonation of authority figures."""

    # Keywords and phrases that indicate false authority
    AUTHORITY_KEYWORDS = [
        "cbi", "fbi", "irs", "police", "bank", "official", "government",
        "supreme court", "rbi", "sebi", "traffic police", "income tax"
    ]

    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        text = features.get("text", "").lower()
        signals = []
        for keyword in self.AUTHORITY_KEYWORDS:
            if keyword in text:
                signals.append(ThreatSignal(
                    name="Authority Impersonation",
                    description=f"Authority keyword '{keyword}' found in the message.",
                    severity=ThreatSeverity.HIGH,
                    confidence=0.85,
                    evidence=keyword
                ))
        return signals