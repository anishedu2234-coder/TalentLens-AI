import math
from extract_jd import extract_jd_requirements

def calculate_score(candidate, jd_requirements=None):
    """
    Calculates a score from 0 to 100 based on JD fit.
    """
    if jd_requirements is None:
        jd_requirements = extract_jd_requirements("")
        
    score = 0.0
    reasoning_parts = []
    
    # --- 1. Skill Match (40 points) ---
    skill_score = 0
    candidate_skills = {s.get("name").lower(): s for s in candidate.get("skills", [])}
    
    core_skills = [s.lower() for s in jd_requirements["core_skills"]]
    ai_skills = [s.lower() for s in jd_requirements["ai_ml_skills"]]
    
    # Evaluate AI skills (max 25 points)
    ai_points = 0
    for s in ai_skills:
        if s in candidate_skills:
            prof = candidate_skills[s].get("proficiency", "beginner")
            if prof == "expert":
                ai_points += 8
            elif prof == "advanced":
                ai_points += 6
            elif prof == "intermediate":
                ai_points += 3
            else:
                ai_points += 1
    ai_points = min(ai_points, 25)
    
    # Evaluate Core skills (max 15 points)
    core_points = 0
    for s in core_skills:
        if s in candidate_skills:
            prof = candidate_skills[s].get("proficiency", "beginner")
            if prof == "expert":
                core_points += 4
            elif prof == "advanced":
                core_points += 3
            elif prof == "intermediate":
                core_points += 2
            else:
                core_points += 1
    core_points = min(core_points, 15)
    
    skill_score = ai_points + core_points
    score += skill_score
    reasoning_parts.append(f"Skills: {skill_score:.1f}/40")
    
    # --- 2. Experience Match (30 points) ---
    yoe = candidate.get("profile", {}).get("years_of_experience", 0)
    yoe_score = 0
    if 5 <= yoe <= 9:
        yoe_score = 30
    elif 3 <= yoe < 5:
        yoe_score = 30 - ((5 - yoe) * 10)
    elif 9 < yoe <= 15:
        yoe_score = 30 - ((yoe - 9) * 3)
    else:
        yoe_score = 0
        
    yoe_score = max(0, min(yoe_score, 30))
    score += yoe_score
    reasoning_parts.append(f"Experience: {yoe_score:.1f}/30")
    
    # --- 3. Role/Industry Relevance (10 points) ---
    role_score = 0
    career = candidate.get("career_history", [])
    relevant_titles = [t.lower() for t in jd_requirements["relevant_titles"]]
    
    for job in career:
        title = job.get("title", "").lower()
        if any(rt in title for rt in relevant_titles):
            if job.get("is_current", False):
                role_score += 10
            else:
                role_score += 5
                
    role_score = min(role_score, 10)
    score += role_score
    reasoning_parts.append(f"Role/Title: {role_score:.1f}/10")
    
    # --- 4. Redrob Platform Signals (20 points) ---
    redrob = candidate.get("redrob_signals", {})
    platform_score = 0
    
    # Completeness (5 pts)
    comp_score = redrob.get("profile_completeness_score", 0)
    platform_score += (comp_score / 100.0) * 5
    
    # GitHub (5 pts)
    gh_score = redrob.get("github_activity_score", -1)
    if gh_score > 0:
        platform_score += (gh_score / 100.0) * 5
        
    # Interview / Recruiter Interaction (10 pts)
    int_rate = redrob.get("interview_completion_rate", 0)
    platform_score += int_rate * 5
    
    resp_rate = redrob.get("recruiter_response_rate", 0)
    platform_score += resp_rate * 5
    
    platform_score = min(platform_score, 20)
    score += platform_score
    reasoning_parts.append(f"Platform: {platform_score:.1f}/20")
    
    # Build a plain-language reasoning string
    title = candidate.get("profile", {}).get("current_title", "Engineer")
    location = candidate.get("profile", {}).get("location", "Unknown")
    
    # Get top AI skills
    candidate_skills_list = [s.get("name") for s in candidate.get("skills", [])]
    ai_skills_present = [s for s in jd_requirements["ai_ml_skills"] if s.lower() in [cs.lower() for cs in candidate_skills_list]]
    
    if ai_skills_present:
        skills_str = f"building {', '.join(ai_skills_present[:2])} systems"
    else:
        skills_str = "with core backend skills"
        
    engagement_str = "strong recent engagement" if platform_score > 10 else "moderate engagement"
    
    reasoning = f"{title} with {yoe} years {skills_str}; {engagement_str} and {location}-based."
    
    final_score = round(score / 100.0, 3)
    return final_score, reasoning
