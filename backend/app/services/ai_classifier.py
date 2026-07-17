import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AIClassifierService:
    def __init__(self):
        self.model_name = "typeform/distilbert-base-uncased-mnli"
        self.classifier = None
        self._initialize_pipeline()

    def _initialize_pipeline(self):
        try:
            from transformers import pipeline
            # Using a fast distilbert model for zero-shot classification 
            # In production, this would point to our locally fine-tuned DeBERTa model
            logger.info(f"Loading HuggingFace zero-shot classification pipeline: {self.model_name}")
            self.classifier = pipeline("zero-shot-classification", model=self.model_name)
            logger.info("Pipeline loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load HuggingFace pipeline. Using fallback mode. Error: {str(e)}")
            self.classifier = None

    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Classifies the text as Scam or Safe and attempts to categorize it.
        """
        if not self.classifier:
            return {
                "verdict": "Unknown",
                "confidence": 0.5,
                "category": "Unclassified"
            }

        try:
            if USE_FINE_TUNED_MODEL:
                result = self.classifier(text)
                predicted_class = result[0]['label']
                confidence = result[0]['score']
                
                # Map Multi-Class back to API Contract
                verdict = "Safe" if "Safe" in predicted_class else "Likely Scam"
                
                return {
                    "verdict": verdict,
                    "confidence": float(confidence),
                    "category": predicted_class
                }
            else:
                result = self.classifier(text, self.candidate_labels)
                top_label = result['labels'][0]
                confidence = result['scores'][0]
                
                # Action-Based Logic for Zero-Shot
                if top_label in ["routine account notification", "friendly chat", "promotional offer"]:
                    verdict = "Safe"
                    category = "Safe Communication"
                else:
                    verdict = "Likely Scam"
                    category = "General Scam/Spam"
                    
                return {
                    "verdict": verdict,
                    "confidence": float(confidence),
                    "category": category
                }
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            return {
                "verdict": "Unknown",
                "confidence": 0.5,
                "category": "Error"
            }

ai_classifier = AIClassifierService()
