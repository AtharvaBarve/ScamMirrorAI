# detectors/fear_detector.py
from typing import Dict, List, Any
from app.services.risk_engine import Detector, ThreatSignal, ThreatSeverity


class FearDetector(Detector):
    """Detects fear-inducing or threatening language."""

    # Fear-inducing keywords/phrases
    FEAR_KEYWORDS = [
        "arrest", "arrested", "court case", "lawsuit", "fine", "penalty",
        "suspended", "cancelled", "blocked", "blacklisted", "legal action",
        "immediate action", "final notice", "warning", "last chance",
        "account will be closed", "urgent action required", "time is running out"
    ]

    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        text = features.get("text", "").lower()
        signals = []
        for keyword in self.FEAR_KEYWORDS:
            if keyword in text:
                signals.append(ThreatSignal(
                    name="Fear Inducing Language",
                    description=f"Fear-inducing keyword '{keyword}' found in the message.",
                    severity=ThreatSeverity.HIGH,
                    confidence=0.8,
                    evidence=keyword
                ))
        return signals