---
title: TalentLens AI
emoji: 🎯
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.32.0"
python_version: "3.11.4"
app_file: app.py
pinned: false
---

# TalentLens AI - Intelligent Candidate Discovery Engine

This repository contains our submission for the Redrob Intelligent Candidate Discovery & Ranking Hackathon. It processes candidate profiles, eliminates AI-generated honeypots through strict logical validation, and ranks candidates based on semantic fit for the Senior AI Engineer role.

## Setup Instructions

This project is built using standard Python and requires no external LLM API keys.

1. Clone the repository.
2. Install the requirements (optional for ranking, required for the Streamlit demo):
   ```bash
   pip install -r requirements.txt
   ```

## Reproducing the Submission

To generate the exact `submission.csv` from the 100,000 candidate pool, simply run:

```bash
python main.py
```

*Note: The `candidates.csv` (JSONL) file and `job_description.txt` must be in the same directory as the script. The script operates well under the 5-minute CPU constraint.*

## Architecture Overview

1. **`extract_jd.py`**: Parses the hardcoded job description rules (5-9 YoE, AI/ML skills, etc.).
2. **`honeypot_filters.py`**: Identifies the ~80 trap candidates using strict logical contradictions (e.g., zero-duration experts, temporal contradictions between signup and last active dates).
3. **`rank_candidates.py`**: A deterministic scoring engine that ranks valid candidates from 0 to 100 based on Skill Match (40%), Experience Match (30%), Role Relevance (10%), and Platform Signals (20%).
4. **`main.py`**: Orchestrates the streaming data ingestion and generation of the final CSV.
5. **`app.py`**: A Streamlit web application used for our Sandbox Demo link.
