# detectors/money_detector.py
import logging
import re
from typing import Dict, List, Any
from app.services.risk_engine import Detector, ThreatSignal, ThreatSeverity

logger = logging.getLogger(__name__)


class MoneyDetector(Detector):
    """Detects mentions of money, prizes, or financial gain with improved thresholding."""

    # Keywords that indicate financial lures
    MONEY_KEYWORDS = [
        "free", "prize", "winner", "won", "cash", "money", "reward", "gift",
        "lottery", "jackpot", "bonus", "discount", "offer", "sale",
        "cash prize", "free money", "instant cash", "guaranteed winner",
        "claim your prize", "you've won", "you won", "collect your winnings"
    ]

    # Patterns that indicate strong financial scam indicators
    SCAM_PATTERNS = [
        r'\b(?:claim|collect|get|receive)\s+(?:your\s+)?(?:prize|winnings?|money|cash)\b',
        r'\b(?:you\s+(?:have|won)|you\'re\s+(?:a\s+)?winner|congratulations?)\s+(?:you\s+)?(?:have|won)\s+(?:a\s+)?(?:prize|reward|\$\d+(?:,\d{3})*(?:\.\d{2})?)\b',
        r'\b(?:free|complimentary|complimentary)\s+(?:money|cash|prize|gift|reward)\b',
        r'\b(?:limited\s+time|urgent|act\s+now|don\'t\s+miss\s+out)\s+(?:offer|deal|prize|prize\s+money)\b',
        r'\b(?:wire|transfer|send)\s+(?:money|funds)\s+(?:to\s+claim|to\s+receive|to\s+unlock)\b',
        r'\b(?:pay\s+?(?:a\s+)?fee|processing\s+fee|handling\s+fee|taxes?)\s+(?:to\s+receive|to\s+claim|to\s+unlock)\b',
        r'\b(?:bank\s+account|credit\s+card|debit\s+card)\s+(?:info|information|details|number)\s+(?:needed|required|required\s+to\s+proceed)\b',
    ]

    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        text = features.get("text", "").lower()
        signals = []

        logger.debug(f"MoneyDetector analyzing text (length: {len(text)} chars)")

        # Count money-related keywords
        money_keyword_count = sum(1 for keyword in self.MONEY_KEYWORDS if keyword in text)

        # Check for scam patterns
        scam_pattern_matches = []
        for pattern in self.SCAM_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                scam_pattern_matches.extend(matches)
                logger.debug(f"Money pattern '{pattern}' matched {len(matches)} times")

        # Determine severity and confidence based on findings
        if scam_pattern_matches:
            # Strong indicators of scam - multiple patterns or specific scam patterns
            signals.append(ThreatSignal(
                name="Financial Scam Pattern",
                description=f"Financial scam pattern detected: '{scam_pattern_matches[0]}'",
                severity=ThreatSeverity.HIGH,
                confidence=0.85 + min(0.1, len(scam_pattern_matches) * 0.05),  # Increase confidence with more patterns
                evidence=scam_pattern_matches[0]
            ))
            logger.info(f"MoneyDetector found {len(scam_pattern_matches)} financial scam patterns")
        elif money_keyword_count >= 3:
            # Multiple money-related keywords - likely promotional/spam
            signals.append(ThreatSignal(
                name="Multiple Financial Keywords",
                description=f"Multiple financial keywords detected ({money_keyword_count} found)",
                severity=ThreatSeverity.MEDIUM,
                confidence=0.6 + min(0.2, (money_keyword_count - 3) * 0.05),  # Increase confidence with more keywords
                evidence=f"{money_keyword_count} financial keywords"
            ))
            logger.info(f"MoneyDetector found {money_keyword_count} financial keywords (>=3 threshold)")
        elif money_keyword_count >= 1:
            # Single money keyword - lower confidence, could be legitimate
            # Only flag if combined with other suspicious words or context
            suspicious_context_words = ["urgent", "act now", "limited time", "don't miss", "expires soon", "winner", "won"]
            has_suspicious_context = any(word in text for word in suspicious_context_words)

            if has_suspicious_context:
                signals.append(ThreatSignal(
                    name="Financial Keyword with Suspicious Context",
                    description=f"Financial keyword found with suspicious context",
                    severity=ThreatSeverity.MEDIUM,
                    confidence=0.65,
                    evidence="financial keyword + suspicious context"
                ))
                logger.info("MoneyDetector found financial keyword with suspicious context")
            else:
                logger.debug(f"MoneyDetector found {money_keyword_count} financial keywords but no suspicious context")
        else:
            logger.debug("MoneyDetector found no financial keywords")

        return signals