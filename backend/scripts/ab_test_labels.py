import logging
from transformers import pipeline
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# A small validation suite combining obvious scams, safe messages, and edge-case financial texts
TEST_SUITE = [
    # Safe - Financial
    {"text": "The electricity bill has been successfully paid.", "expected": "safe"},
    {"text": "Your salary has been credited to HDFC bank.", "expected": "safe"},
    {"text": "Amazon order #123 has been delivered.", "expected": "safe"},
    {"text": "Your monthly rent is due tomorrow.", "expected": "safe"},
    
    # Safe - Conversational
    {"text": "Hello, how are you?", "expected": "safe"},
    {"text": "Good morning! Can we meet at 4 PM?", "expected": "safe"},
    {"text": "Thank you for your help yesterday.", "expected": "safe"},
    
    # Scam - Financial
    {"text": "URGENT: Your HDFC bank account is locked. Click here to verify your identity: http://hdfc-update-kyc.com", "expected": "scam"},
    {"text": "Congratulations! You have won $1,000,000 in the WhatsApp Lucky Draw. Send $50 fee to claim.", "expected": "scam"},
    {"text": "Dear customer, your electricity connection will be cut tonight at 9 PM. Call the billing officer immediately at 9876543210.", "expected": "scam"},
    
    # Scam - Impersonation
    {"text": "Hi Mum, I lost my phone. I'm using a friend's phone. Can you send me some money for a taxi?", "expected": "scam"}
]

LABEL_SETS = {
    "Set 1 (Original Topic-Based)": ["financial scam", "phishing attempt", "impersonation", "safe communication", "marketing spam"],
    "Set 2 (Intent-Based)": ["fraudulent request", "malicious phishing", "impersonation scam", "normal conversation", "transaction notification", "marketing spam"],
    "Set 3 (Action-Based)": ["stealing money or credentials", "urgent threat or warning", "routine account notification", "friendly chat", "promotional offer"]
}

def map_to_binary(label: str, label_set_name: str, confidence: float) -> str:
    """Map the model's raw predicted label back to a binary safe/scam verdict."""
    if label_set_name == "Set 1 (Original Topic-Based)":
        return "safe" if label == "safe communication" else "scam"
    elif label_set_name == "Set 2 (Intent-Based)":
        return "safe" if label in ["normal conversation", "transaction notification"] else "scam"
    elif label_set_name == "Set 3 (Action-Based)":
        return "safe" if label in ["routine account notification", "friendly chat"] else "scam"
    return "unknown"

def run_benchmark():
    logger.info("Loading Zero-Shot Classifier...")
    classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
    
    results = {}
    
    for set_name, labels in LABEL_SETS.items():
        logger.info(f"\nEvaluating {set_name}...")
        
        correct = 0
        false_positives = 0
        false_negatives = 0
        
        for case in TEST_SUITE:
            res = classifier(case["text"], labels)
            predicted_label = res['labels'][0]
            confidence = res['scores'][0]
            
            binary_pred = map_to_binary(predicted_label, set_name, confidence)
            expected = case["expected"]
            
            if binary_pred == expected:
                correct += 1
            else:
                if expected == "safe" and binary_pred == "scam":
                    false_positives += 1
                    logger.warning(f"[False Positive] '{case['text']}' -> Predicted: {predicted_label} ({confidence:.2f})")
                elif expected == "scam" and binary_pred == "safe":
                    false_negatives += 1
                    logger.warning(f"[False Negative] '{case['text']}' -> Predicted: {predicted_label} ({confidence:.2f})")
                    
        total = len(TEST_SUITE)
        accuracy = (correct / total) * 100
        
        results[set_name] = {
            "Accuracy": f"{accuracy:.1f}%",
            "False Positives": false_positives,
            "False Negatives": false_negatives
        }
        
    logger.info("\n=== BENCHMARK RESULTS ===")
    for set_name, metrics in results.items():
        logger.info(f"{set_name}:")
        for k, v in metrics.items():
            logger.info(f"  - {k}: {v}")

if __name__ == "__main__":
    run_benchmark()
