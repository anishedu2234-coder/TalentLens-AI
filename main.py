import json
import csv
from extract_jd import extract_jd_requirements
from honeypot_filters import is_honeypot
from rank_candidates import calculate_score

def process_candidates(candidates_path, output_path):
    print("Extracting JD requirements...")
    jd_reqs = extract_jd_requirements("job_description.txt")
    
    print("Processing candidates...")
    results = []
    
    with open(candidates_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
                
            try:
                candidate = json.loads(line)
                candidate_id = candidate.get("candidate_id")
                
                honeypot_flag, honeypot_reason = is_honeypot(candidate)
                
                if honeypot_flag:
                    results.append({
                        "candidate_id": candidate_id,
                        "score": 0.0,
                        "is_honeypot": "True",
                        "reasoning": honeypot_reason
                    })
                else:
                    score, reasoning = calculate_score(candidate, jd_reqs)
                    results.append({
                        "candidate_id": candidate_id,
                        "score": score,
                        "is_honeypot": "False",
                        "reasoning": reasoning
                    })
            except Exception as e:
                pass
                
    # Sort results: First by score (descending), then by candidate_id to ensure determinism
    # Honeypots will naturally be at the bottom since their score is 0.0
    print("Sorting candidates...")
    results.sort(key=lambda x: (-x["score"], x["candidate_id"]))
    
    # We only need the top 100 candidates for the submission
    valid_candidates = [r for r in results if r["is_honeypot"] == "False"]
    top_100 = valid_candidates[:100]
    
    print(f"Writing {len(top_100)} results to {output_path}...")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate_id", "rank", "score", "reasoning"])
        writer.writeheader()
        for i, row in enumerate(top_100):
            writer.writerow({
                "candidate_id": row["candidate_id"],
                "rank": i + 1,
                "score": float(row["score"]),
                "reasoning": row["reasoning"]
            })
        
    print("Done! Submission generated.")

if __name__ == "__main__":
    candidates_file = "candidates.csv" # It is a JSONL file in reality
    output_file = "submission.csv"
    process_candidates(candidates_file, output_file)
