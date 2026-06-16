import streamlit as st
import pandas as pd
import json
import tempfile
import os
from extract_jd import extract_jd_requirements
from honeypot_filters import is_honeypot
from rank_candidates import calculate_score
import csv

st.set_page_config(page_title="TalentLens AI", page_icon="🎯", layout="wide")

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Global Fonts & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Gradient */
    h1 {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem !important;
        margin-bottom: 0rem;
        padding-bottom: 0rem;
    }
    
    h3 {
        color: #a0aec0;
        font-weight: 400;
        margin-top: 0rem;
        margin-bottom: 2rem;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.5);
    }
    
    /* Download Button Specific */
    .stDownloadButton>button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.3);
    }
    .stDownloadButton>button:hover {
        box-shadow: 0 6px 20px rgba(56, 239, 125, 0.5);
    }

    /* File Uploader styling */
    .stFileUploader {
        border-radius: 12px;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.2);
    }

    /* DataFrame Container */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("TalentLens AI")
st.markdown("### Intelligent Candidate Discovery & Ranking Engine")

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### Data Ingestion")
    st.write("Upload candidate profiles (JSONL format) to rank them instantly against the **Senior AI Engineer** requirements.")
    uploaded_file = st.file_uploader("", type=["jsonl", "csv", "txt"], help="Limit: 500MB")
    run_engine = st.button("🚀 Run Ranking Engine")

with col2:
    if run_engine and uploaded_file is not None:
        with st.spinner("Analyzing semantics and detecting honeypots..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
                
            try:
                jd_reqs = extract_jd_requirements("")
                results = []
                honeypot_count = 0
                total_count = 0
                
                with open(tmp_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            total_count += 1
                            candidate = json.loads(line)
                            candidate_id = candidate.get("candidate_id")
                            honeypot_flag, honeypot_reason = is_honeypot(candidate)
                            
                            profile = candidate.get("profile", {})
                            
                            if honeypot_flag:
                                honeypot_count += 1
                                results.append({
                                    "candidate_id": candidate_id,
                                    "name": profile.get("anonymized_name", "N/A"),
                                    "title": profile.get("current_title", "N/A"),
                                    "yoe": profile.get("years_of_experience", 0),
                                    "score": 0.0,
                                    "is_honeypot": "True",
                                    "reasoning": honeypot_reason
                                })
                            else:
                                score, reasoning = calculate_score(candidate, jd_reqs)
                                results.append({
                                    "candidate_id": candidate_id,
                                    "name": profile.get("anonymized_name", "N/A"),
                                    "title": profile.get("current_title", "N/A"),
                                    "yoe": profile.get("years_of_experience", 0),
                                    "score": score,
                                    "is_honeypot": "False",
                                    "reasoning": reasoning
                                })
                        except Exception:
                            pass
                
                # Sort results
                results.sort(key=lambda x: (-x["score"], x["candidate_id"]))
                valid_candidates = [r for r in results if r["is_honeypot"] == "False"]
                top_candidates = valid_candidates[:100]
                
                # Dashboard Metrics
                st.markdown("#### Processing Complete")
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Analyzed", f"{total_count:,}")
                m2.metric("Valid Candidates", f"{len(valid_candidates):,}")
                m3.metric("Honeypots Blocked", f"{honeypot_count:,}", delta="- Fraud Detected", delta_color="inverse")
                
                st.markdown("---")
                
                # Format Data
                display_data = []
                submission_data = []
                
                for i, row in enumerate(top_candidates):
                    rank = i + 1
                    display_data.append({
                        "Rank": rank,
                        "Candidate ID": row["candidate_id"],
                        "Name": row["name"],
                        "Current Title": row["title"],
                        "YoE": row["yoe"],
                        "Score": float(row["score"]),
                        "Reasoning": row["reasoning"]
                    })
                    submission_data.append({
                        "candidate_id": row["candidate_id"],
                        "rank": rank,
                        "score": float(row["score"]),
                        "reasoning": row["reasoning"]
                    })
                
                df_display = pd.DataFrame(display_data)
                df_submission = pd.DataFrame(submission_data)
                
                st.markdown("#### Top Recommended Candidates")
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                csv_data = df_submission.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download submission.csv",
                    data=csv_data,
                    file_name='submission.csv',
                    mime='text/csv',
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                os.unlink(tmp_path)
                
    elif not run_engine:
        st.info("👈 Upload your dataset and run the engine to view the dashboard.")
