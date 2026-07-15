# detectors/phone_detector.py
from typing import Dict, List, Any
from app.services.risk_engine import Detector, ThreatSignal, ThreatSeverity
import re


class PhoneDetector(Detector):
    """Detects phone numbers or requests to call."""

    # Keywords that indicate phone contact
    PHONE_KEYWORDS = [
        "call", "phone", "telephone", "dial", "call now", "phone number",
        "contact us", "hotline", "helpline"
    ]

    # Simple regex for phone numbers (basic patterns)
    PHONE_PATTERNS = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # XXX-XXX-XXXX
        r'\b\(\d{3}\)\s*\d{3}[-.]?\d{4}\b',  # (XXX) XXX-XXXX
        r'\b\d{10,12}\b'  # 10-12 digits
    ]

    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        text = features.get("text", "")
        signals = []

        # Check for keywords
        lower_text = text.lower()
        for keyword in self.PHONE_KEYWORDS:
            if keyword in lower_text:
                signals.append(ThreatSignal(
                    name="Phone Contact Request",
                    description=f"Phone-related keyword '{keyword}' found in the message.",
                    severity=ThreatSeverity.MEDIUM,
                    confidence=0.7,
                    evidence=keyword
                ))

        # Check for phone number patterns
        for pattern in self.PHONE_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    signals.append(ThreatSignal(
                        name="Phone Number Detected",
                        description=f"Phone number pattern '{match}' found in the message.",
                        severity=ThreatSeverity.HIGH,
                        confidence=0.85,
                        evidence=match
                    ))
        return signals