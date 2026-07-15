from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional
import time
import logging

logger = logging.getLogger(__name__)


class ThreatSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class ThreatSignal:
    """Represents a single threat signal detected by a detector."""
    name: str
    description: str
    severity: ThreatSeverity
    confidence: float  # 0.0 to 1.0
    evidence: str  # The actual evidence found in the input


@dataclass
class ThreatEngineOutput:
    """Output from a threat engine (rule-based or ML)."""
    verdict: str  # e.g., "Likely Scam", "Likely Safe", "Uncertain"
    confidence: float  # Overall confidence in the verdict
    category: Optional[str]  # e.g., "Financial Scam", "Phishing"
    risk_factors: List[str]  # List of risk factor descriptions
    processing_time: float  # Time taken to compute in seconds
    signals: List[ThreatSignal]  # Individual signals that contributed


class ThreatEngine(ABC):
    """Abstract base class for threat detection engines."""

    @abstractmethod
    def analyze(self, features: Dict[str, Any]) -> ThreatEngineOutput:
        """
        Analyze the input features and return a threat assessment.

        Args:
            features: A dictionary of features extracted from the input.
                      Expected keys may include: 'text', 'url', 'domain', etc.

        Returns:
            ThreatEngineOutput: The result of the threat analysis.
        """
        pass


class Detector(ABC):
    """Interface for a threat detector."""

    @abstractmethod
    def detect(self, features: Dict[str, Any]) -> List[ThreatSignal]:
        """
        Detect threats in the given features.

        Args:
            features: A dictionary of features extracted from the input.

        Returns:
            List of ThreatSignal objects. Empty list if no threats detected.
        """
        pass


class RuleBasedThreatEngine(ThreatEngine):
    """
    Rule-based threat detection engine.
    Uses a collection of detectors to collect signals and then makes a final verdict.
    """

    def __init__(self, detectors: Optional[List[Detector]] = None):
        self.detectors: List[Detector] = detectors or []
        # We'll add detectors via a method or constructor

    def add_detector(self, detector: Detector):
        self.detectors.append(detector)

    def analyze(self, features: Dict[str, Any]) -> ThreatEngineOutput:
        start_time = time.time()
        all_signals: List[ThreatSignal] = []

        logger.debug(f"Starting threat detection with {len(self.detectors)} detectors")
        logger.debug(f"Input features keys: {list(features.keys())}")

        # Collect signals from all detectors
        for detector in self.detectors:
            signals = detector.detect(features)
            all_signals.extend(signals)
            if signals:
                logger.debug(f"Detector {detector.__class__.__name__} found {len(signals)} signals")

        logger.info(f"Total signals detected: {len(all_signals)}")

        # If no signals, return safe
        if not all_signals:
            logger.info("No threats detected - returning 'Likely Safe'")
            return ThreatEngineOutput(
                verdict="Likely Safe",
                confidence=0.0,
                category=None,
                risk_factors=[],
                processing_time=time.time() - start_time,
                signals=[]
            )

        # Simple aggregation logic:
        # - If any HIGH severity signal -> Likely Scam
        # - Else if any MEDIUM severity signal -> Likely Scam (with lower confidence) or Uncertain? We'll use MEDIUM as scam too for now.
        # - Else (only LOW) -> Uncertain or Likely Safe? We'll treat LOW as suspicious but not enough for scam.
        # We'll also compute an overall confidence as the max confidence of signals? Or average? Let's use max for now.

        # Determine if we have any HIGH or MEDIUM signals
        has_high = any(s.severity == ThreatSeverity.HIGH for s in all_signals)
        has_medium = any(s.severity == ThreatSeverity.MEDIUM for s in all_signals)

        if has_high:
            verdict = "Likely Scam"
            # Confidence: max confidence of HIGH signals, or at least 0.8
            high_confidences = [s.confidence for s in all_signals if s.severity == ThreatSeverity.HIGH]
            confidence = max(high_confidences) if high_confidences else 0.8
            logger.info(f"High severity threat detected - verdict: {verdict} (confidence: {confidence:.2f})")
        elif has_medium:
            verdict = "Likely Scam"
            medium_confidences = [s.confidence for s in all_signals if s.severity == ThreatSeverity.MEDIUM]
            confidence = max(medium_confidences) if medium_confidences else 0.6
            logger.info(f"Medium severity threat detected - verdict: {verdict} (confidence: {confidence:.2f})")
        else:
            # Only LOW signals
            verdict = "Uncertain"
            low_confidences = [s.confidence for s in all_signals if s.severity == ThreatSeverity.LOW]
            confidence = max(low_confidences) if low_confidences else 0.5
            logger.info(f"Only low severity signals detected - verdict: {verdict} (confidence: {confidence:.2f})")

        # Category: we can set based on the signals? For now, we'll set a generic category.
        # We can improve by having detectors contribute to category.
        category = "Financial Scam" if verdict == "Likely Scam" else None

        # Risk factors: we can use the signal names or descriptions
        risk_factors = list(set([s.name for s in all_signals]))  # unique signal names
        logger.debug(f"Risk factors identified: {risk_factors}")

        result = ThreatEngineOutput(
            verdict=verdict,
            confidence=confidence,
            category=category,
            risk_factors=risk_factors,
            processing_time=time.time() - start_time,
            signals=all_signals
        )

        logger.debug(f"Returning ThreatEngineOutput: {result.__dict__}")
        return result


# We'll keep the ThreatEngineOutput and ThreatSignal as defined above.