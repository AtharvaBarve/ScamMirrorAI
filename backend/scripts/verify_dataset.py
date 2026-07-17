import json
import random
import hashlib
import logging
import os
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

PROCESSED_DIR = "data/processed"

def get_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def verify_and_split():
    dataset_path = os.path.join(PROCESSED_DIR, "final_hybrid_dataset.jsonl")
    records = []
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
            
    # Shuffle predictably
    random.seed(42)
    random.shuffle(records)
    
    total = len(records)
    train_idx = int(0.8 * total)
    val_idx = int(0.9 * total)
    
    train_set = records[:train_idx]
    val_set = records[train_idx:val_idx]
    test_set = records[val_idx:]
    
    logger.info("=== DATASET SPLIT RESULTS ===")
    logger.info(f"Total: {total}")
    logger.info(f"Train: {len(train_set)} ({len(train_set)/total:.1%})")
    logger.info(f"Validation: {len(val_set)} ({len(val_set)/total:.1%})")
    logger.info(f"Test: {len(test_set)} ({len(test_set)/total:.1%})")
    
    # Verify Leakage
    train_hashes = {get_hash(r["text"]) for r in train_set}
    val_hashes = {get_hash(r["text"]) for r in val_set}
    test_hashes = {get_hash(r["text"]) for r in test_set}
    
    val_leakage = train_hashes.intersection(val_hashes)
    test_leakage = train_hashes.intersection(test_hashes)
    
    if val_leakage or test_leakage:
        logger.error(f"LEAKAGE DETECTED! {len(val_leakage)} in Val, {len(test_leakage)} in Test.")
        # Strict removal of leakage
        val_set = [r for r in val_set if get_hash(r["text"]) not in val_leakage]
        test_set = [r for r in test_set if get_hash(r["text"]) not in test_leakage]
        logger.info(f"Leakage removed. New Val: {len(val_set)}, New Test: {len(test_set)}")
    else:
        logger.info("Leakage Check: PASSED. Zero exact text leakage between splits.")
        
    # Class distribution in training
    cat_counts = Counter(r["category"] for r in train_set)
    logger.info("\n=== TRAINING CATEGORY DISTRIBUTION ===")
    for cat, count in cat_counts.most_common():
        logger.info(f"{cat}: {count}")
        
    # Language distribution
    lang_counts = Counter(r["language"] for r in train_set)
    logger.info("\n=== TRAINING LANGUAGE DISTRIBUTION ===")
    for lang, count in lang_counts.most_common():
        logger.info(f"{lang}: {count}")
        
    # Save splits
    with open(os.path.join(PROCESSED_DIR, "train.jsonl"), "w") as f:
        for r in train_set: f.write(json.dumps(r)+"\n")
    with open(os.path.join(PROCESSED_DIR, "val.jsonl"), "w") as f:
        for r in val_set: f.write(json.dumps(r)+"\n")
    with open(os.path.join(PROCESSED_DIR, "test.jsonl"), "w") as f:
        for r in test_set: f.write(json.dumps(r)+"\n")
        
    logger.info("\nSplits saved successfully.")
    
if __name__ == "__main__":
    verify_and_split()
