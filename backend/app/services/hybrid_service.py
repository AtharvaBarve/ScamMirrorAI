"""
AI-Driven Threat Intelligence Service (Phase 2 Migration).
Orchestrates the threat detection pipeline: 
Entity extraction (regex) -> Transformer Classification (DeBERTa/Zero-Shot) -> NIM explanation.
"""
import logging
import time
from typing import Any, Dict, Optional

from app.services.claude_service import ClaudeService
from app.services.ai_classifier import ai_classifier
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
    Main service that orchestrates the AI analysis pipeline.
    """

    def __init__(self):
        # We retain the rule engine strictly for Entity Extraction and IOC flagging
        self.entity_extractor = RuleBasedThreatEngine()
        self._register_detectors()
        logger.debug("HybridService initialized with entity extractors")

    def _register_detectors(self):
        """Register all available detectors with the entity extractor."""
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
            self.entity_extractor.add_detector(detector)

    async def analyze(self, input_type: str, input_content: str, original_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze the input using the new ML pipeline and return a dictionary matching the API schema.
        """
        start_time = time.time()
        logger.debug(f"Starting AI analysis for {input_type} input (length: {len(input_content)} chars)")

        features: Dict[str, Any] = {"text": input_content}
        if original_url is not None:
            features["url"] = original_url

        try:
            # 1. Entity Extraction (IOCs)
            logger.debug("Running entity extraction")
            extraction_output: ThreatEngineOutput = self.entity_extractor.analyze(features)
            
            # 2. ML Classification (Phase 2)
            logger.debug("Running Transformer classification")
            classification_result = ai_classifier.classify_text(input_content)
            
            # Merge results: use ML verdict, but keep extracted risk factors
            threat_assessment = {
                "verdict": classification_result["verdict"],
                "confidence": classification_result["confidence"],
                "category": classification_result["category"] or extraction_output.category,
                "risk_factors": extraction_output.risk_factors,
                "signals": [
                    {
                        "name": s.name,
                        "description": s.description,
                        "severity": str(getattr(s, 'severity', 'Unknown')),
                        "evidence": s.evidence,
                    }
                    for s in extraction_output.signals
                ],
            }
            logger.debug(f"Classification completed: {threat_assessment['verdict']} ({threat_assessment['confidence']:.2f})")
            
        except Exception as e:
            logger.error(f"Error during threat detection: {str(e)}", exc_info=True)
            return {
                "verdict": "Error",
                "explanation": "An error occurred during AI analysis. Please try again.",
                "confidence": 0.0,
                "category": None,
                "risk_factors": [],
                "recommended_actions": ["Please try again later."],
                "processing_time": time.time() - start_time,
            }

        try:
            # 3. Retrieval-Augmented Generation (RAG)
            logger.debug("Retrieving threat intelligence context from ChromaDB")
            from app.services.retrieval_service import retrieval_service
            
            rag_context = retrieval_service.retrieve_context(
                text=input_content,
                classification={"verdict": threat_assessment["verdict"], "category": threat_assessment["category"]},
                extracted_entities=threat_assessment["signals"]
            )
            
            logger.debug(f"Retrieved Context: {rag_context}")

            # 4. LLM Explanation (NVIDIA NIM / Claude) with RAG Context
            logger.debug("Getting explanation and recommendations from LLM")
            explanation_result = await ClaudeService.get_explanation_and_actions(
                threat_assessment,
                input_content,
                rag_context=rag_context
            )
            explanation = explanation_result.get("explanation", "")
            recommended_actions = explanation_result.get("recommended_actions", [])
        except Exception as e:
            logger.error(f"Error getting explanation from LLM: {str(e)}", exc_info=True)
            explanation = "Classification based on AI semantic analysis."
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
            f"AI Analysis completed: {result['verdict']} "
            f"(confidence: {result['confidence']:.2f}) in {total_processing_time:.3f}s"
        )
        return result


hybrid_service = HybridService()
