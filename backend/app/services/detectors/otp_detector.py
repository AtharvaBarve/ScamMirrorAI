# detectors/otp_detector.py
import logging
import re
from typing import Dict, List, Any
from app.services.risk_engine import Detector, ThreatSignal, ThreatSeverity

logger = logging.getLogger(__name__)


class OTPDetector(Detector):
    """Detects requests for OTP, PIN, or passwords."""

    # Patterns for OTP, PIN, password requests - made more specific to reduce false positives
    OTP_PATTERNS = [
        r'\b(?:enter|provide|share|give|type|input|enter your|provide your|share your|give your|type your|input your)\s+(?:otp|pin|password|ssn|social security|bank account|credit card|debit card|verification code|security code)\b',
        r'\b(?:otp|pin|password|ssn|social security|bank account|credit card|debit card|verification code|security code)\s+(?:is|was|has been|will be)\s+\d+\b',
        r'\b(?:otp|pin|password|ssn|social security|bank account|credit card|debit card|verification code|security code):\s*\d+\b',
        r'\b(?:otp|pin|password|ssn|social security|bank account|credit card|debit card|verification code|security code)\s*[:=]\s*\d+\b',
        r'\b(?:otp|pin|password|ssn|social security|bank account|credit card|debit card|verification code|security code)\s+is\s+\d{4,6}\b',
        r'\byour\s+(?:otp|pin|password|ssn|social security|bank account|credit card|debit card|verification code|security code)\s+is\s+\d+\b',
        r'\bplease\s+(?:enter|provide|share|give|type|input)\s+(?:your\s+)?(?:otp|pin|password|ssn|social security|bank account|credit card|debit card|verification code|security code)\b',
        r'\b(?:otp|pin|password|ssn|social security|bank account|credit card|debit card|verification code|security code)\s+(?:for\s+verification|to\s+verify|to\s+confirm)\b',
        r'\b\d{6}\b\s*(?:is\s+your\s+otp|is\s+your\s+pin|is\s+your\s+verification\s+code|is\s+your\s+security\s+code)\b',
    ]

    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        text = features.get("text", "").lower()
        signals = []

        logger.debug(f"OTPDetector analyzing text (length: {len(text)} chars)")

        for pattern in self.OTP_PATTERNS:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            if matches:
                for match in matches:
                    matched_text = match.group()
                    signals.append(ThreatSignal(
                        name="Sensitive Information Request",
                        description=f"Request for sensitive information: '{matched_text}' found.",
                        severity=ThreatSeverity.HIGH,
                        confidence=0.9,
                        evidence=matched_text
                    ))
                logger.debug(f"Pattern '{pattern}' matched {len(matches)} times")

        if signals:
            logger.info(f"OTPDetector found {len(signals)} sensitive information requests")
        else:
            logger.debug("OTPDetector found no matches")

        return signals