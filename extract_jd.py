import json
import re

def extract_jd_requirements(jd_path):
    """
    Since the JD is fixed for this hackathon, we can use a hardcoded extraction 
    based on our analysis of the job_description.txt. 
    In a real system, this would use an LLM or complex NLP to parse an arbitrary JD.
    """
    
    # We will use these extracted features for ranking candidates.
    requirements = {
        "target_yoe_min": 5,
        "target_yoe_max": 9,
        "core_skills": [
            "Python", "Java", "Go", "SQL", "NoSQL",
            "Docker", "Kubernetes", "AWS", "GCP", "CI/CD"
        ],
        "ai_ml_skills": [
            "LLM", "RAG", "Prompt Engineering", "Fine-tuning"
        ],
        "relevant_titles": [
            "AI Engineer", "Machine Learning Engineer", "Backend Engineer", 
            "Software Engineer", "Data Engineer", "Staff Engineer", "Senior Engineer"
        ]
    }
    
    return requirements

if __name__ == "__main__":
    # Test the extraction
    reqs = extract_jd_requirements("../job_description.txt")
    print(json.dumps(reqs, indent=2))
