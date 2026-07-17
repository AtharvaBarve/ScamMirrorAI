import json
import logging
import os
import urllib.request
import zipfile
import re
import random
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

TARGET_CATEGORIES = {
    "Financial Scam": 1000,
    "Phishing Attempt": 1000,
    "Marketing Spam": 500,
    "Safe Communication": 2000,
    "Safe Financial Notification": 500,
    "Business Email Compromise": 200,
    "Enterprise Credential Phishing": 200,
    "Fake HR / Payroll": 200,
    "Corporate Login Scams": 200,
    "Hinglish Scams": 200,
    "Marathi-English Scams": 100,
    "QR/UPI Scams": 200,
    "Government Impersonation": 200,
    "Tech Support Scam": 200
}

def load_uci_sms() -> list:
    logger.info("Downloading UCI SMS Spam Collection...")
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
    zip_path = os.path.join(DATA_DIR, "smsspamcollection.zip")
    
    if not os.path.exists(zip_path):
        urllib.request.urlretrieve(url, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
        
    records = []
    with open(os.path.join(DATA_DIR, "SMSSpamCollection"), "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                raw_label, sms = parts
                
                label = "Safe" if raw_label == "ham" else "Likely Scam"
                
                # Simple heuristic categorization for public datasets
                category = "Safe Communication"
                if label == "Likely Scam":
                    text_lower = sms.lower()
                    if any(w in text_lower for w in ["bank", "account", "money", "cash", "pay", "rupee"]):
                        category = "Financial Scam"
                    elif any(w in text_lower for w in ["http", "www", "click", "link"]):
                        category = "Phishing Attempt"
                    else:
                        category = "Marketing Spam"
                else:
                    text_lower = sms.lower()
                    if any(w in text_lower for w in ["paid", "credited", "debited", "balance", "txn"]):
                        category = "Safe Financial Notification"
                        
                records.append({
                    "text": sms,
                    "label": label,
                    "category": category,
                    "source": "uci/sms_spam",
                    "language": "en"
                })
    return records

def perform_gap_analysis(data: list):
    logger.info("\n=== DATASET GAP ANALYSIS ===")
    
    counts = defaultdict(int)
    for row in data:
        counts[row["category"]] += 1
        
    print(f"{'Category':<35} | {'Current':<8} | {'Target':<8} | {'Missing':<8}")
    print("-" * 65)
    
    total_missing = 0
    missing_report = {}
    
    for cat, target in TARGET_CATEGORIES.items():
        current = counts[cat]
        missing = max(0, target - current)
        total_missing += missing
        missing_report[cat] = missing
        
        status = "OK" if missing == 0 else f"-{missing}"
        print(f"{cat:<35} | {current:<8} | {target:<8} | {status:<8}")
        
    print("-" * 65)
    logger.info(f"Total Synthetic Augmentation Required: {total_missing} samples")
    return missing_report

def main():
    logger.info("Initializing Dataset Builder v2...")
    
    # 1. Collect Real World Data
    dataset = []
    dataset.extend(load_uci_sms())
    
    # 2. Clean
    # Deduplicate
    unique_data = {row["text"]: row for row in dataset}.values()
    dataset = list(unique_data)
    
    # Remove empty
    dataset = [row for row in dataset if len(row["text"].strip()) > 5]
    
    logger.info(f"Cleaned Real-World Dataset Size: {len(dataset)}")
    
    # 3. Gap Analysis
    missing = perform_gap_analysis(dataset)
    
    # Save the missing requirements to JSON for the synthetic generator to pick up
    with open(os.path.join(PROCESSED_DIR, "gap_analysis.json"), "w") as f:
        json.dump(missing, f, indent=2)
        
    # Save base real dataset
    with open(os.path.join(PROCESSED_DIR, "base_real_dataset.jsonl"), "w", encoding="utf-8") as f:
        for row in dataset:
            f.write(json.dumps(row) + "\n")

if __name__ == "__main__":
    main()
