import json
import logging
from collections import Counter
from datasets import load_dataset
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_FILE = "data/processed/scammirror_dataset_v1.jsonl"

import urllib.request
import zipfile
import os

def normalize_uci_sms() -> list[dict]:
    """
    Load and normalize UCI SMS Spam Collection directly from UCI.
    """
    logger.info("Downloading UCI SMS Spam Collection from UCI Archive...")
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
    zip_path = "data/raw/smsspamcollection.zip"
    os.makedirs("data/raw", exist_ok=True)
    
    urllib.request.urlretrieve(url, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("data/raw/")
        
    normalized = []
    with open("data/raw/SMSSpamCollection", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                raw_label, sms = parts
                label = "safe" if raw_label == "ham" else "scam"
                category = "Safe Communication" if label == "safe" else "General Scam/Spam"
                
                normalized.append({
                    "text": sms,
                    "label": label,
                    "category": category,
                    "source": "uci/sms_spam"
                })
    
    logger.info(f"Loaded {len(normalized)} records from UCI SMS Spam.")
    return normalized

def deduplicate_and_balance(data: list[dict]) -> list[dict]:
    """
    Remove exact duplicates by text, then balance the classes.
    """
    logger.info(f"Starting deduplication (Total: {len(data)})...")
    
    # Deduplicate
    unique_map = {}
    for item in data:
        text = item["text"].strip()
        if text and text not in unique_map:
            unique_map[text] = item
            
    unique_data = list(unique_map.values())
    logger.info(f"After deduplication: {len(unique_data)} records remaining.")
    
    # Balance
    safe_items = [x for x in unique_data if x["label"] == "safe"]
    scam_items = [x for x in unique_data if x["label"] == "scam"]
    
    min_class_size = min(len(safe_items), len(scam_items))
    logger.info(f"Balancing dataset to {min_class_size} records per class...")
    
    # Simple random undersampling of majority class
    import random
    random.seed(42)
    
    balanced_data = random.sample(safe_items, min_class_size) + random.sample(scam_items, min_class_size)
    random.shuffle(balanced_data)
    
    return balanced_data

def generate_statistics(data: list[dict]):
    """
    Print basic statistics about the dataset.
    """
    df = pd.DataFrame(data)
    logger.info("\n=== DATASET STATISTICS ===")
    logger.info(f"Total Records: {len(df)}")
    
    logger.info("\nClass Distribution:")
    for label, count in df["label"].value_counts().items():
        logger.info(f" - {label}: {count}")
        
    logger.info("\nSource Distribution:")
    for source, count in df["source"].value_counts().items():
        logger.info(f" - {source}: {count}")
        
    logger.info("==========================\n")

def main():
    logger.info("Initializing ScamMirror AI Dataset Pipeline...")
    
    # 1. Collect
    data = []
    data.extend(normalize_uci_sms())
    
    # Note: In a true production run, we would add PhishTank, OpenPhish, etc. here.
    
    # 2. Clean & Balance
    final_dataset = deduplicate_and_balance(data)
    
    # 3. Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for record in final_dataset:
            f.write(json.dumps(record) + "\n")
            
    logger.info(f"Saved normalized dataset to {OUTPUT_FILE}")
    
    # 4. Report
    generate_statistics(final_dataset)

if __name__ == "__main__":
    main()
