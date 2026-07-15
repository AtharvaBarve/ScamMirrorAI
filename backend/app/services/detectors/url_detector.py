# detectors/url_detector.py
from typing import Dict, List, Any
from app.services.risk_engine import Detector, ThreatSignal, ThreatSeverity
import re


class URLDetector(Detector):
    """Detects suspicious URLs or URL shorteners."""

    # Suspicious URL patterns
    SUSPICIOUS_TLDS = [".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top"]
    URL_SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd"]

    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        # We expect features to have 'url' or maybe 'text' that contains URLs
        url = features.get("url", "")
        text = features.get("text", "")
        # Combine text and url to search for URLs
        combined = f"{url} {text}"
        signals = []

        # Check for URL shorteners
        for shortener in self.URL_SHORTENERS:
            if shortener in combined.lower():
                signals.append(ThreatSignal(
                    name="URL Shortener Detected",
                    description=f"URL shortener '{shortener}' found in the message.",
                    severity=ThreatSeverity.HIGH,
                    confidence=0.9,
                    evidence=shortener
                ))

        # Check for suspicious TLDs
        # Simple approach: look for the TLD in the string
        for tld in self.SUSPICIOUS_TLDS:
            if tld in combined.lower():
                signals.append(ThreatSignal(
                    name="Suspicious TLD",
                    description=f"Suspicious top-level domain '{tld}' found in the message.",
                    severity=ThreatSeverity.HIGH,
                    confidence=0.85,
                    evidence=tld
                ))

        # Optional: detect IP addresses in URLs (sometimes used in phishing)
        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        if re.search(ip_pattern, combined):
            signals.append(ThreatSignal(
                name="IP Address in URL",
                description="IP address found in URL (often used in phishing).",
                severity=ThreatSeverity.HIGH,
                confidence=0.8,
                evidence="IP address"
            ))

        return signals