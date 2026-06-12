import sys
from validator import run_validation
from agent import generate_remediation

def main():
    DATA_FILE = "sample_data.csv" 
    RULES_FILE = "rules.yaml"

    print("🔍 Step 1: Evaluating Data Integrity Checks...")
    failures = run_validation(DATA_FILE, RULES_FILE)

    if not failures:
        print("✅ Clean Data! All data quality constraints passed verification successfully.")
        return

    print(f"⚠️ Anomalies Detected! Activating LLM Explainer + Remediation Engine...")
    print("-" * 65)
    
    # Ship failure payloads to the agent script
    ai_remediation = generate_remediation(failures)
    
    # Render final technical log outputs directly to stdout console
    print(ai_remediation)

if __name__ == "__main__":
    main()