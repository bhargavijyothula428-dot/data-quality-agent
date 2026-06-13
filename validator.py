import pandas as pd
import yaml

def load_rules(yaml_path):
    print(f"🔍 Loading validation rules from: {yaml_path}...")
    """Loads validation constraints from our YAML configuration"""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)['validation_rules']

def run_validation(data_path, rules_path):
    print(f"📊 Ingesting dataset for scanning: {data_path}...")
    """Reads data and catches rows that violate any defined rule"""
    # Handle both CSV and Parquet file extensions seamlessly
    if data_path.endswith('.csv'):
        df = pd.read_csv(data_path)
    elif data_path.endswith('.parquet') or data_path.endswith('.pq'):
        df = pd.read_parquet(data_path)
    else:
        raise ValueError("Unsupported format!")

    failed_reports = []
    rules = load_rules(rules_path)
    
    print("⚙️ Running Great-Expectations-style constraint checks...")
    # Evaluate each rule on our dataset
    for rule in rules:
        col = rule['column']
        check_type = rule['check']
        
        if col not in df.columns:
            continue
            
        bad_df = pd.DataFrame()
        
        # Parse rule definitions
        if check_type == "not_null":
            bad_df = df[df[col].isna()]
        elif check_type == "min_max":
            bad_df = df[(df[col] < rule['min']) | (df[col] > rule['max'])]
        elif check_type == "contains":
            bad_df = df[~df[col].astype(str).str.contains(rule['value'])]
            
        # If failures are captured, isolate a sample of the bad data
        if not bad_df.empty:
            failed_reports.append({
                "column": col,
                "constraint_violated": rule,
                "sample_bad_rows": bad_df.head(3).to_dict(orient="records")
            })
            
    if failed_reports:
        print(f"❌ [VALIDATION FAILED]: Detected {len(failed_reports)} column constraint failures!")
    else:
        print("✅ [VALIDATION SUCCESS]: All dataset constraints passed smoothly.")

    return failed_reports