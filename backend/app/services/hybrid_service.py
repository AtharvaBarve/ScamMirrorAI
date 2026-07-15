"""
Hybrid Service for ScamMirror AI.
Orchestrates the threat detection pipeline: feature extraction -> rule-based engine -> NIM explanation.
"""
import time
import logging
from typing import Dict, Any, Optional
from app.services.url_service import fetch_text
from app.services.risk_engine import RuleBasedThreatEngine, ThreatEngineOutput
from app.services.claude_service import ClaudeService
from app.services.detectors import (
    UrgencyDetector,
    AuthorityDetector,
    MoneyDetector,
    OTPDetector,
    GovernmentDetector,
    PhoneDetector,
    URLDetector,
    FearDetector,
)

# Set up logger
logger = logging.getLogger(__name__)


class HybridService:
    """
    Main service that orchestrates the hybrid analysis pipeline.
    """

    def __init__(self):
        # Initialize the rule-based engine with all detectors
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

        Args:
            input_type: Either "text" or "url".
            input_content: The text to analyze (for "text") or the extracted text from URL (for "url").
            original_url: The original URL string if input_type is "url", otherwise None.

        Returns:
            Dictionary with keys: verdict, explanation, confidence, category, risk_factors, recommended_actions, processing_time.
        """
        start_time = time.time()
        logger.debug(f"Starting analysis for {input_type} input (length: {len(input_content)} chars)")

        # Step 1: Build features dictionary
        features: dict
        features: Dict[str, Any] = {"text": input_content}
        if original_url is not None:
            features["url"] = original_url

        # Step 2: Run threat detection engine
        logger.debug("Running threat detection engine")
        threat_engine_output: ThreatEngineOutput = self.engine.analyze(features)

        # Step 2: Run threat detection engine
            logger.debug("Running threat detection engine")
            threat_engine_output: ThreatEngineOutput = self.engine.analyze(features)
            logger.debug(f"Threat detection completed: {threat_engine_output.verdict} (confidence: {threat_engine_output.confidence:.2f})")
        except Exception as e:
            logger.error(f"Error during threat detection: {str(e)}", exc_info=True)
            # Return a safe fallback result
            return {
                "verdict": "Error",
                "explanation": "An error occurred during threat analysis. Please try again.",
                "confidence": 0.0,
                "category": None,
                "risk_factors": [],
                "recommended_actions": ["Please try again later."],
                "processing_time": time.time() - start_time
            }

        # Step 3: Convert threat engine output to dict for internal use
        # We'll convert the dataclass to a dict, but we need to handle nested dataclasses (signals).
        # Since we don't expose signals in the final output, we can keep them internal.
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
                    "severity": s.severity.value if hasattr(s.severity, 'value') else str(s.severity),
                    "confidence": s.confidence,
                    "evidence": s.evidence,
                }
                for s in threat_engine_output.signals
            ],
        }

        # Step 4: Get explanation and recommended actions from NIM
        try:
            logger.debug("Getting explanation and recommendations from ClaudeService")
            explanation_result = await ClaudeService.get_explanation_and_actions(
                "
                        awaited awaited                ]
                    "                "            and                    "                        "            "                        "                        "
"
                <                                      "                    "                "            "                    "                        "                    "            "            " "                "                " "                        "                "                ""        "            " "                "            "            " "                "            "            " "                "            " " "                "                "                "                "                "                "       "                                "                            "            "            "                    "            "            "                    "            "            "                                    "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            "            ""es.

                                                                                        logger.debug("Explanation and recommendations received")
            explanation = explanation_result.get("explanation", "")
            recommended_actions = explanation_result.get("recommended_actions", [])
        except Exception as e:
            logger.error(f"Error getting explanation from ClaudeService: {str(e)}", exc_info=True)
            # Fallback explanation if NIM fails
            explanation = "Classification based on detected threat signals."
            recommended_actions = ["Review the message carefully."]

        # Step 5: Build final response dictionary
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

        logger.info(f"Analysis completed: {result['verdict']} (confidence: {result['confidence']:.2f}) in {total_processing_time:.3f}s")
        return result


# Create a singleton instance for use in the router
hybrid_service = HybridService()