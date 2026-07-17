import os
import json
import torch
import numpy as np
import evaluate
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

PROCESSED_DIR = "data/processed"
MODEL_OUTPUT_DIR = "data/models/scammirror-deberta-v1"

# Load categories dynamically to map ID <-> Label
def load_datasets():
    train_data, val_data, test_data = [], [], []
    with open(os.path.join(PROCESSED_DIR, "train.jsonl")) as f: train_data = [json.loads(l) for l in f]
    with open(os.path.join(PROCESSED_DIR, "val.jsonl")) as f: val_data = [json.loads(l) for l in f]
    with open(os.path.join(PROCESSED_DIR, "test.jsonl")) as f: test_data = [json.loads(l) for l in f]
    
    unique_categories = sorted(list(set([x["category"] for x in train_data])))
    id2label = {i: cat for i, cat in enumerate(unique_categories)}
    label2id = {cat: i for i, cat in enumerate(unique_categories)}
    
    return train_data, val_data, test_data, id2label, label2id

# Custom Dataset
class ScamDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Custom Trainer for Class Weights
from torch import nn
class WeightedTrainer(Trainer):
    def __init__(self, class_weights, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = torch.tensor(class_weights, dtype=torch.float).to(self.args.device)

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")
        
        # Cast class_weights to the same dtype as logits to prevent Half vs Float errors
        class_weights = self.class_weights.to(logits.dtype)
        
        loss_fct = nn.CrossEntropyLoss(weight=class_weights)
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

def compute_metrics(eval_pred):
    accuracy_metric = evaluate.load("accuracy")
    precision_metric = evaluate.load("precision")
    recall_metric = evaluate.load("recall")
    f1_metric = evaluate.load("f1")
    
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    
    acc = accuracy_metric.compute(predictions=predictions, references=labels)
    # Using weighted average because it is a multi-class problem
    prec = precision_metric.compute(predictions=predictions, references=labels, average="weighted")
    rec = recall_metric.compute(predictions=predictions, references=labels, average="weighted")
    f1 = f1_metric.compute(predictions=predictions, references=labels, average="weighted")
    
    return {
        "accuracy": acc["accuracy"],
        "precision": prec["precision"],
        "recall": rec["recall"],
        "f1": f1["f1"],
    }

def train():
    logger.info("Initializing Fine-Tuning Pipeline...")
    train_data, val_data, test_data, id2label, label2id = load_datasets()
    
    logger.info(f"Loaded {len(train_data)} train, {len(val_data)} val, {len(test_data)} test samples.")
    logger.info(f"Categories: {id2label}")
    
    model_name = "microsoft/deberta-v3-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    train_texts = [x["text"] for x in train_data]
    train_labels = [label2id[x["category"]] for x in train_data]
    
    val_texts = [x["text"] for x in val_data]
    val_labels = [label2id[x["category"]] for x in val_data]
    
    # Calculate Class Weights
    from collections import Counter
    counts = Counter(train_labels)
    total = sum(counts.values())
    num_classes = len(id2label)
    class_weights = [total / (num_classes * counts.get(i, 1)) for i in range(num_classes)]
    
    logger.info("Tokenizing data...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=256)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=256)
    
    train_dataset = ScamDataset(train_encodings, train_labels)
    val_dataset = ScamDataset(val_encodings, val_labels)
    
    logger.info("Loading model...")
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(id2label),
        id2label=id2label,
        label2id=label2id
    )
    
    # Very fast prototype training config
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        max_steps=5,  # Added to prevent 5-hour CPU hang in this environment
        per_device_train_batch_size=16,  
        per_device_eval_batch_size=16,   
        warmup_steps=2,                
        weight_decay=0.01,               
        logging_dir='./logs',            
        logging_steps=1,
        eval_strategy="steps",
        eval_steps=2,
        save_strategy="steps",
        save_steps=2,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        seed=42
    )

    trainer = WeightedTrainer(
        class_weights=class_weights,
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    logger.info("Starting Training...")
    trainer.train()
    
    logger.info("Saving Best Model...")
    trainer.save_model(MODEL_OUTPUT_DIR)
    tokenizer.save_pretrained(MODEL_OUTPUT_DIR)
    
    logger.info("Evaluating on Validation Set...")
    eval_results = trainer.evaluate()
    logger.info(f"Final Eval Results: {eval_results}")
    
    # Save a quick JSON of metrics
    with open(os.path.join(MODEL_OUTPUT_DIR, "eval_metrics.json"), "w") as f:
        json.dump(eval_results, f, indent=2)
        
if __name__ == "__main__":
    train()
