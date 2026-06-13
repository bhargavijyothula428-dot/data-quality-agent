import os
import google.generativeai as genai
import streamlit as st

# This checks your Streamlit Secrets FIRST, then falls back to local environment
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

genai.configure(api_key=api_key)

def generate_remediation(failed_reports):
    """Sends bad data profiles to Gemini to build code fixes and text logs."""
    prompt = f"""
    You are an expert Data Quality Engineer.
    An automated data pipeline validation check has failed. Review the failure context and sample rows:
    
    {failed_reports}
    
    Expected Deliverables:
    1. LLM Explainer: Clearly diagnose why the data records failed the check parameters.
    2. Remediation Drafter: Provide an explicit Pandas Python snippet AND an executable SQL statement to clear or filter out these bad entries.
    
    Organize your answer cleanly using clear Markdown headers.
    """

    # Using gemini-1.5-flash which is extremely fast and entirely free for hobby projects
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    return response.text