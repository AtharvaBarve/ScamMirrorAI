from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

messages = [
    "The electricity bill has been successfully paid.",
    "Your salary has been credited.",
    "URGENT: Your HDFC bank account is locked. Click here to verify your identity: http://hdfc-update-kyc.com",
    "Hello",
    "Can we meet at 4 PM?"
]

# Old Labels
old_labels = ["financial scam", "phishing attempt", "impersonation", "safe communication", "marketing spam"]

# New Labels (Intent based)
new_labels = ["fraudulent request", "malicious phishing", "impersonation scam", "normal conversation", "transaction notification", "marketing spam"]

print("=== TESTING OLD LABELS ===")
for msg in messages:
    res = classifier(msg, old_labels)
    print(f"[{msg}] -> {res['labels'][0]} ({res['scores'][0]:.2f})")

print("\n=== TESTING NEW LABELS ===")
for msg in messages:
    res = classifier(msg, new_labels)
    print(f"[{msg}] -> {res['labels'][0]} ({res['scores'][0]:.2f})")
