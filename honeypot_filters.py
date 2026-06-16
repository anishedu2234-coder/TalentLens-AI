import json
from datetime import datetime

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def is_honeypot(candidate):
    """
    Evaluates a candidate profile and returns (is_honeypot, reason)
    """
    try:
        profile = candidate.get("profile", {})
        
        # Rule 1: Expert skill with 0 duration
        skills = candidate.get("skills", [])
        for skill in skills:
            if skill.get("proficiency") == "expert" and skill.get("duration_months", 0) == 0:
                return True, "Expert skill with 0 duration"
                
        # Rule 2: Years of Experience Contradiction
        claimed_yoe = profile.get("years_of_experience", 0)
        career = candidate.get("career_history", [])
        
        total_days = 0
        for job in career:
            start = parse_date(job.get("start_date"))
            end_str = job.get("end_date")
            if not end_str:
                end = datetime.now().date()
            else:
                end = parse_date(end_str)
            
            if start and end and end > start:
                total_days += (end - start).days
                
        calculated_yoe = total_days / 365.25
        
        if claimed_yoe > 0 and calculated_yoe > 0:
            if claimed_yoe - calculated_yoe > 3.0:
                return True, f"Claimed {claimed_yoe} YoE but only has {calculated_yoe:.1f} in career history"
                
        # Rule 3: Signup date before last active date logically
        # A candidate cannot be active before they signed up
        redrob = candidate.get("redrob_signals", {})
        signup_date = parse_date(redrob.get("signup_date"))
        last_active = parse_date(redrob.get("last_active_date"))
        
        if signup_date and last_active:
            if last_active < signup_date:
                # Some slight drift might be allowed due to timezone, but if it's more than a day:
                if (signup_date - last_active).days > 1:
                    return True, "Last active date is before signup date"
        
        # Rule 4: Notice period days abnormally high (e.g. over 180 days is physically impossible according to schema limit, 
        # but the schema limit says max is 180. If it's over 180, it's invalid anyway, but what about exactly 180? It's fine).
        # Let's check for impossible career history (e.g. working before they were born, but we only have education start year)
        edu = candidate.get("education", [])
        earliest_edu_year = 2030
        for e in edu:
            start_year = e.get("start_year")
            if start_year and start_year < earliest_edu_year:
                earliest_edu_year = start_year
                
        earliest_job_date = None
        for job in career:
            start = parse_date(job.get("start_date"))
            if start:
                if not earliest_job_date or start < earliest_job_date:
                    earliest_job_date = start
                    
        # If they started a professional job 10 years before they started their first degree, 
        # that might be a flag, but it happens. We will stick to the very strong signals.
        
        return False, "Candidate is valid"
        
    except Exception as e:
        # If parsing fails on an expected field, they are a honeypot or invalid format
        return True, f"Parsing error: {str(e)}"
