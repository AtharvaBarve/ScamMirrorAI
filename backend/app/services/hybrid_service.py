"""
Hybrid Service for ScamMirror AI.
Orchestrates the threat detection pipeline: feature extraction -> rule-based engine -> NIM explanation.
"""
import logging
import time
from typing import Any, Dict, Optional

from app.services.claude_service import ClaudeService
from app.services.detectors.authority_detector import AuthorityDetector
from app.services.detectors.fear_detector import FearDetector
from app.services.detectors.government_detector import GovernmentDetector
from app.services.detectors.money_detector import MoneyDetector
from app.services.detectors.otp_detector import OTPDetector
from app.services.detectors.phone_detector import PhoneDetector
from app.services.detectors.urgency_detector import UrgencyDetector
from app.services.detectors.url_detector import URLDetector
from app.services.risk_engine import RuleBasedThreatEngine, ThreatEngineOutput

logger = logging.getLogger(__name__)


class HybridService:
    """
    Main service that orchestrates the hybrid analysis pipeline.
    """

    def __init__(self):
        self.engine = RuleBasedThreatEngine()
        self._register_detectors()
        logger.debug("HybridService initialized with all detectors")

    def _register_detectors(self):
        """Register all available detectors with the engine."""
        detectors = [
            UrgencyDetector(),
            AuthorityDetector(),
            MoneyDetector(),
            OTPDetector(),
            GovernmentDetector(),
            PhoneDetector(),
            URLDetector(),
            FearDetector(),
        ]
        for detector in detectors:
            self.engine.add_detector(detector)
        logger.debug(f"Registered {len(detectors)} detectors with the engine")

    async def analyze(self, input_type: str, input_content: str, original_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze the input and return a dictionary matching the existing API schema.
        """
        start_time = time.time()
        logger.debug(f"Starting analysis for {input_type} input (length: {len(input_content)} chars)")

        features: Dict[str, Any] = {"text": input_content}
        if original_url is not None:
            features["url"] = original_url

        try:
            logger.debug("Running threat detection engine")
            threat_engine_output: ThreatEngineOutput = self.engine.analyze(features)
            logger.debug(
                f"Threat detection completed: {threat_engine_output.verdict} "
                f"(confidence: {threat_engine_output.confidence:.2f})"
            )
        except Exception as e:
            logger.error(f"Error during threat detection: {str(e)}", exc_info=True)
            return {
                "verdict": "Error",
                "explanation": "An error occurred during threat analysis. Please try again.",
                "confidence": 0.0,
                "category": None,
                "risk_factors": [],
                "recommended_actions": ["Please try again later."],
                "processing_time": time.time() - start_time,
            }

        threat_assessment = {
            "verdict": threat_engine_output.verdict,
            "confidence": threat_engine_output.confidence,
            "category": threat_engine_output.category,
            "risk_factors": threat_engine_output.risk_factors,
            "processing_time": threat_engine_output.processing_time,
            "signals": [
                {
                    "name": s.name,
                    "description": s.description,
                    "severity": s.severity.value if hasattr(s.severity, "value") else str(s.severity),
                    "confidence": s.confidence,
                    "evidence": s.evidence,
                }
                for s in threat_engine_output.signals
            ],
        }

        try:
            logger.debug("Getting explanation and recommendations from ClaudeService")
            explanation_result = await ClaudeService.get_explanation_and_actions(
                threat_assessment,
                input_content,
            )
            logger.debug("Explanation and recommendations received")
            explanation = explanation_result.get("explanation", "")
            recommended_actions = explanation_result.get("recommended_actions", [])
        except Exception as e:
            logger.error(f"Error getting explanation from ClaudeService: {str(e)}", exc_info=True)
            explanation = "Classification based on detected threat signals."
            recommended_actions = ["Review the message carefully."]

        total_processing_time = time.time() - start_time
        result = {
            "verdict": threat_assessment["verdict"],
            "explanation": explanation,
            "confidence": float(threat_assessment["confidence"]),
            "category": threat_assessment["category"],
            "risk_factors": threat_assessment["risk_factors"],
            "recommended_actions": recommended_actions,
            "processing_time": total_processing_time,
        }

        logger.info(
            f"Analysis completed: {result['verdict']} "
            f"(confidence: {result['confidence']:.2f}) in {total_processing_time:.3f}s"
        )
        return result


hybrid_service = HybridService()
