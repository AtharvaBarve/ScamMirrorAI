import asyncio
import json
from app.services.ai_classifier import ai_classifier
from app.services.hybrid_service import hybrid_service

TEST_MESSAGES = [
    "Hello",
    "Good morning!",
    "Thank you for your help.",
    "Can we meet at 4 PM?",
    "The electricity bill has been successfully paid.",
    "Your salary has been credited.",
    "Your Amazon order has been delivered."
]

async def run_investigation():
    print("=== ROOT CAUSE ANALYSIS: FALSE POSITIVES ===\n")
    
    # 1. Test AI Classifier Raw Output
    print("--- 1. RAW CLASSIFIER OUTPUT ---")
    candidate_labels = ["financial scam", "phishing attempt", "impersonation", "safe communication", "marketing spam"]
    
    for msg in TEST_MESSAGES:
        print(f"\nMessage: '{msg}'")
        try:
            # Bypass the wrapper to get raw output
            raw_result = ai_classifier.classifier(msg, candidate_labels)
            print(f"Candidate Labels: {raw_result['labels']}")
            print(f"Raw Scores: {[round(s, 4) for s in raw_result['scores']]}")
            print(f"Predicted Label: {raw_result['labels'][0]}")
            
            # Show wrapped output
            wrapped_result = ai_classifier.classify_text(msg)
            print(f"Mapped Verdict: {wrapped_result['verdict']}")
            print(f"Mapped Confidence: {wrapped_result['confidence']:.4f}")
            print(f"Mapped Category: {wrapped_result['category']}")
        except Exception as e:
            print(f"Error classifying: {e}")

    # 2. Test Full Pipeline (Hybrid Service)
    print("\n--- 2. FULL HYBRID PIPELINE OUTPUT ---")
    msg = "The electricity bill has been successfully paid."
    print(f"\nMessage: '{msg}'")
    result = await hybrid_service.analyze("text", msg)
    print(f"Final API Verdict: {result['verdict']}")
    print(f"Final API Confidence: {result['confidence']:.4f}")
    print(f"Final API Category: {result.get('category')}")
    print(f"Final Explanation: {result['explanation']}")

if __name__ == "__main__":
    asyncio.run(run_investigation())
