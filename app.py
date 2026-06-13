import streamlit as st
import pandas as pd
import yaml
import os

# 🔄 IMPORTING THE EXACT FUNCTIONS FROM YOUR BACKEND:
from validator import run_validation
from agent import generate_remediation

# 1. Page Title Configuration
st.set_page_config(page_title="Data Quality Agent", layout="wide")
st.title("🛡️ Data Quality Agent with AI Auto-Fix Suggestions")
st.markdown("Upload a dataset and define your expectations to get instant, automated fixes from Gemini.")

# 2. Build the Two-Column Visual Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("1. Data & Configuration Input")
    
    # Drag-and-drop file uploader widget
    uploaded_file = st.file_uploader("Upload your Dataset (CSV)", type=["csv"])
    
    # Default rule template that populates the editable textbox
    default_rules = """rules:
  - column: user_id
    check: not_null
  - column: age
    check: min_max
    min: 0
    max: 120
  - column: email
    check: contains
    value: '@'"""
    
    # Dynamic textbox to let users type or change rules on the fly
    rules_text = st.text_area("Define Data Quality Rules (YAML format)", value=default_rules, height=250)

with col2:
    st.header("2. AI Remediation Engine")
    
    # The action trigger button
    if st.button("⚡ Run Diagnostics & Generate Fixes"):
        if uploaded_file is not None and rules_text:
            with st.spinner("Processing dataset and consulting Gemini API..."):
                
                # A. Save the uploaded browser file temporarily so your backend can read it
                data_path = "temp_upload.csv"
                with open(data_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                rules_path = "temp_rules.yaml"
                with open(rules_path, "w") as f:
                    f.write(rules_text)
                
                try:
                    # B. Load the interactive rules text box as a dictionary
                    rules_dict = yaml.safe_load(rules_text) or {}
# This looks for BOTH naming formats so your code never breaks:
                    rules = rules_dict.get('validation_rules', rules_dict.get('rules', []))
                    
                    # Read into dataframe to print the visual data table preview
                    df = pd.read_csv(data_path)
                    st.subheader("📋 Dataset Sample Preview")
                    st.dataframe(df.head(5))
                    
                    # C. Run your background validation checker
                    failed_reports = run_validation(data_path, rules_path)
                    
                    if failed_reports:
                        st.error(f"🚨 Flagged {len(failed_reports)} Data Quality Failures!")
                        
                        # D. CALLING YOUR FIXED FUNCTION NAME:
                        ai_report = generate_remediation(failed_reports)
                        
                        # E. Render the beautiful report formatting out onto the web panel
                        st.markdown(ai_report)
                    else:
                        st.success("🎉 Clean Bill of Health! All data constraints passed smoothly.")
                        
                except Exception as e:
                    st.error(f"Pipeline Execution Failed: {e}")
                
                finally:
                    # F. Safely delete the temporary file tracks
                    if os.path.exists(data_path): os.remove(data_path)
                    if os.path.exists(rules_path): os.remove(rules_path)
        else:
            st.warning("⚠️ Action required: Please upload a valid CSV file before initiating analysis.")