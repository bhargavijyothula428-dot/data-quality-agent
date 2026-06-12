# Data Quality Agent with Auto-Fix Suggestions

This repository contains a modular, production-ready AI Data Quality Agent designed to detect dataset anomalies and automatically engineer data repair strategies.

## 🚀 Key Features
- Decoupled data constraint validations driven entirely via YAML formatting.
- Native ingestion engines supporting both `.csv` and `.parquet` file configurations.
- Advanced log error analysis that mitigates opaque processing failures by routing structured error profiles to a custom AI agent.
- On-the-fly remediation code translation supplying valid data manipulation scripts across **SQL** and **Pandas Python**.

## 📂 Architecture Breakdown
- `rules.yaml`: Declares structural dataset health constraints.
- `sample_data.csv`: Houses testing anomalies (null keys, boundary failures).
- `validator.py`: The validation engine responsible for detecting dataset failures and extracting bad row records.
- `agent.py`: Bridges the pipeline anomalies with a Large Language Model to draft structural data fixes.
- `main.py`: The master execution script orchestrating the system pipeline.

## ⚙️ How to Run the Project
1. Install project dependencies:
```bash
   pip install pandas pyarrow google-generativeai pyyaml