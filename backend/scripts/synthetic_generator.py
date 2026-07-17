import json
import random
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

PROCESSED_DIR = "data/processed"

# Generation Data
COMPANIES = ["TCS", "Infosys", "HDFC", "SBI", "ICICI", "Amazon", "Flipkart", "Microsoft", "Google", "Okta", "Workday"]
PEOPLE = ["Rajesh", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Suresh", "Ramesh", "John", "Sarah"]
URL_DOMAINS = ["update-kyc.com", "secure-login-portal.in", "verify-account-now.net", "hr-payroll-update.com", "microsoft-auth-365.com"]
AMOUNTS = ["₹5,000", "₹10,000", "₹50,000", "$100", "$500", "Rs 20,000"]

def generate_bec() -> str:
    templates = [
        "Hi {name}, I'm stuck in a meeting. I need you to process a wire transfer of {amount} to our new vendor immediately. Please confirm when ready.",
        "URGENT: {name}, please initiate a confidential payment of {amount} for the Q3 acquisition. Do not tell anyone. I will explain later. - CEO",
        "Hello {name}, I am traveling and my corporate card was declined. Send {amount} via Apple Pay to this number so I can pay the client dinner.",
        "Please update the payroll direct deposit for my account. My new routing number is attached. Do this before tomorrow's payout.",
    ]
    return random.choice(templates).format(name=random.choice(PEOPLE), amount=random.choice(AMOUNTS))

def generate_enterprise_phishing() -> str:
    templates = [
        "IT Alert: Your {company} Office365 password expires in 2 hours. Click here to retain your current password: http://{url}",
        "Security update required. Okta detected unusual login attempts to your {company} account. Verify here: https://{url}",
        "Your VPN access will be revoked tonight. Install the new Cisco AnyConnect certificate here: http://{url}",
        "Mandatory Security Awareness Training. Due today. Log in at http://{url} to complete."
    ]
    return random.choice(templates).format(company=random.choice(COMPANIES), url=random.choice(URL_DOMAINS))

def generate_hr_payroll() -> str:
    templates = [
        "HR Notice: {company} Annual Appraisal documents are ready. View your revised salary slip here: http://{url}",
        "Your September salary of {amount} has been held due to tax discrepancies. Please update your PAN details at http://{url}",
        "Employee Benefits Update: You are eligible for a {amount} Diwali bonus. Claim it at http://{url}",
    ]
    return random.choice(templates).format(company=random.choice(COMPANIES), url=random.choice(URL_DOMAINS), amount=random.choice(AMOUNTS))

def generate_hinglish() -> str:
    templates = [
        "Bhai urgent {amount} GPay kar de, mera card chal nahi raha hai hospital me. Mai sham ko de dunga.",
        "Sir, aapka HDFC bank account block ho gaya hai. KYC update karne ke liye is link par click karein: http://{url}",
        "Congratulations! Aapko {company} ki taraf se {amount} ka gift voucher mila hai. Claim karne ke liye call karein.",
        "Hello {name}, kal meeting hai na? Mujhe location bhej de bhai.",  # Safe
    ]
    return random.choice(templates).format(amount=random.choice(AMOUNTS), url=random.choice(URL_DOMAINS), company=random.choice(COMPANIES), name=random.choice(PEOPLE))

def generate_marathi_english() -> str:
    templates = [
        "Namaskar, tumcha SBI account block zala ahe. KYC update sathi link var click kara: http://{url}",
        "Mitra, urgent {amount} transfer kar. Mi nantar deto.",
        "Aapla {amount} cha EMI due ahe. Payment sathi ithe click kara.",
    ]
    return random.choice(templates).format(url=random.choice(URL_DOMAINS), amount=random.choice(AMOUNTS))

def generate_qr_upi() -> str:
    templates = [
        "Scan this QR code to receive your refund of {amount} from {company}.",
        "Dear customer, your UPI payment of {amount} failed. Click here to claim refund: http://{url}",
        "You have won a scratch card of {amount} on PhonePe. Click here and enter your UPI PIN to receive money in bank account."
    ]
    return random.choice(templates).format(amount=random.choice(AMOUNTS), company=random.choice(COMPANIES), url=random.choice(URL_DOMAINS))

def generate_financial_scam() -> str:
    templates = [
        "Dear customer, your credit card has been charged {amount}. If not authorized, click here: http://{url}",
        "Your loan of {amount} is approved. Pay processing fee of Rs 999 to get it.",
        "Urgent: Your tax refund of {amount} is pending. Update bank details here: http://{url}"
    ]
    return random.choice(templates).format(amount=random.choice(AMOUNTS), url=random.choice(URL_DOMAINS))
    
def generate_safe_financial() -> str:
    templates = [
        "Your account XX1234 has been credited with {amount} on 12-Oct. Available Bal: {amount}",
        "Payment of {amount} to {company} successful. Ref: 1294829.",
        "Your bill for Rs 1,200 is due on 15th. Pay via app."
    ]
    return random.choice(templates).format(amount=random.choice(AMOUNTS), company=random.choice(COMPANIES))

GENERATORS = {
    "Business Email Compromise": generate_bec,
    "Enterprise Credential Phishing": generate_enterprise_phishing,
    "Fake HR / Payroll": generate_hr_payroll,
    "Hinglish Scams": generate_hinglish,
    "Marathi-English Scams": generate_marathi_english,
    "QR/UPI Scams": generate_qr_upi,
    "Financial Scam": generate_financial_scam,
    "Safe Financial Notification": generate_safe_financial,
    "Phishing Attempt": lambda: f"Update your {random.choice(COMPANIES)} account immediately to avoid suspension: http://{random.choice(URL_DOMAINS)}",
    "Government Impersonation": lambda: f"Income Tax Department: Fined {random.choice(AMOUNTS)}. Pay here: http://{random.choice(URL_DOMAINS)}",
    "Tech Support Scam": lambda: f"Microsoft Alert: Call 1-800-FAKE-NUM to remove virus from your computer.",
    "Marketing Spam": lambda: f"Get 50% off on your next {random.choice(COMPANIES)} purchase! Buy now.",
    "Corporate Login Scams": lambda: f"Your remote access VPN token expired. Refresh here: http://{random.choice(URL_DOMAINS)}"
}

def generate_synthetic_samples(missing: dict):
    synthetic_data = []
    logger.info("Generating synthetic data based on Gap Analysis...")
    for category, count in missing.items():
        if count <= 0 or category not in GENERATORS:
            continue
            
        generator = GENERATORS[category]
        logger.info(f"Generating {count} samples for {category}...")
        
        # We use a set to ensure uniqueness if possible, though with limited templates it will repeat structure
        generated = set()
        attempts = 0
        while len(generated) < count and attempts < count * 5:
            text = generator()
            generated.add(text)
            attempts += 1
            
        # Determine base label
        label = "Safe" if "Safe" in category else "Likely Scam"
        if category == "Hinglish Scams":
            lang = "hi-en"
        elif category == "Marathi-English Scams":
            lang = "mr-en"
        else:
            lang = "en"
            
        for text in generated:
            synthetic_data.append({
                "text": text,
                "label": label,
                "category": category,
                "source": "synthetic_augmentation",
                "language": lang
            })
            
    logger.info(f"Generated {len(synthetic_data)} total synthetic samples.")
    return synthetic_data

def merge_and_export():
    # Load base real data
    real_data = []
    with open(os.path.join(PROCESSED_DIR, "base_real_dataset.jsonl"), "r") as f:
        for line in f:
            real_data.append(json.loads(line))
            
    # Load gap analysis
    with open(os.path.join(PROCESSED_DIR, "gap_analysis.json"), "r") as f:
        missing = json.load(f)
        
    synthetic_data = generate_synthetic_samples(missing)
    
    combined = real_data + synthetic_data
    random.shuffle(combined)
    
    final_path = os.path.join(PROCESSED_DIR, "final_hybrid_dataset.jsonl")
    with open(final_path, "w", encoding="utf-8") as f:
        for row in combined:
            f.write(json.dumps(row) + "\n")
            
    # Stats
    logger.info("\n=== FINAL DATASET STATISTICS ===")
    logger.info(f"Total Samples: {len(combined)}")
    real_count = len([x for x in combined if x["source"] != "synthetic_augmentation"])
    sync_count = len(combined) - real_count
    logger.info(f"Real Data: {real_count} ({real_count/len(combined):.1%})")
    logger.info(f"Synthetic Data: {sync_count} ({sync_count/len(combined):.1%})")
    
if __name__ == "__main__":
    merge_and_export()
