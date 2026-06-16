# 🎯 TalentLens AI: Intelligent Candidate Discovery Engine

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)

Welcome to the **TalentLens AI** repository! This project is our official submission for the **Redrob Intelligent Candidate Discovery & Ranking Hackathon**. 

We have built a deterministic, blazing-fast semantic ranking engine that processes candidate profiles, eliminates AI-generated honeypots through strict logical validation, and ranks candidates based on their contextual fit for the **Senior AI Engineer** role.

---

## ✨ Key Features

- **🛡️ Ironclad Honeypot Detection**: Automatically flags synthetic trap candidates using temporal contradictions (e.g., active before signup) and logical impossibilities (zero-duration expert skills).
- **🧠 Semantic Skill Matching**: Evaluates core backend technologies (Python, Java, Go) alongside modern AI competencies (LLM, RAG, Prompt Engineering).
- **⚡ High-Performance Pipeline**: Processes a 100,000-candidate JSONL dataset deterministically under the 5-minute CPU constraint without requiring any external LLM APIs or GPU acceleration.
- **🎨 Premium UI Dashboard**: Features a glassmorphism-inspired Streamlit web app with dynamic metrics and visual data validation.

---

## 🏗️ Architecture Overview

Our scoring algorithm evaluates valid candidates across four rigorous pillars to output a normalized score (0.000 to 1.000):

1. **Skill Match (40%)**: Jaccard-style similarity weighted heavily towards advanced/expert AI proficiencies.
2. **Experience Match (30%)**: A Gaussian distribution scoring model perfectly tailored for the 5-9 Years of Experience sweet spot.
3. **Role Relevance (10%)**: Contextual bonuses for relevant current/past titles (e.g., "Machine Learning Engineer").
4. **Platform Signals (20%)**: A composite score evaluating profile completeness, GitHub activity, interview attendance, and recruiter responsiveness.

---

## 🚀 Setup & Installation

This project is built using standard Python and requires no external API keys.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anishedu2234-coder/TalentLens-AI.git
   cd TalentLens-AI
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Reproducing the Submission

To generate the exact `submission.csv` from the 100,000 candidate pool used for our final hackathon evaluation:

```bash
python main.py
```

*Note: The `candidates.csv` (JSONL format) and `job_description.txt` must be located in the root directory. The pipeline is heavily optimized for CPU execution.*

---

## 🌐 Live Sandbox Demo

We have deployed a live, interactive version of the ranking engine for evaluation purposes.

👉 **[Launch the TalentLens AI Dashboard](https://talent-lens-ai.streamlit.app/)**

- Upload a candidate JSONL dataset (up to 500 MB).
- View real-time analytics on honeypot detection.
- Export the strict, hackathon-compliant `submission.csv` directly from the web interface.

---

*Built with ❤️ by Team **STRIVERS***
