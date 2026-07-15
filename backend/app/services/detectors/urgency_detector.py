# detectors/urgency_detector.py
from typing import Dict, List, Any
from app.services.risk_engine import Detector, ThreatSignal, ThreatSeverity


class UrgencyDetector(Detector):
    """Detects urgency-inducing language."""

    # Keywords that indicate urgency
    URGENCY_KEYWORDS = ["urgent", "immediately", "act now", "limited time", "expires soon"]

    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        text = features.get("text", "").lower()
        signals = []
        for keyword in self.URGENCY_KEYWORDS:
            if keyword in text:
                signals.append(ThreatSignal(
                    name="Urgency Detected",
                    description=f"Urgency keyword '{keyword}' found in the message.",
                    severity=ThreatSeverity.HIGH,
                    confidence=0.8,  # We can adjust based on keyword
                    evidence=keyword
                ))
        return signals