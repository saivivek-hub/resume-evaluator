def tokenize(text):
    return set(text.lower().split())


def evaluate_with_llm(candidate, job_desc):

    #  INPUTS 
    skills = tokenize(candidate.get("skills", ""))
    project = tokenize(candidate.get("project", ""))
    job_tokens = tokenize(job_desc)

    experience = candidate.get("experience", 0)

    factors = []

    # CORE MATCH 
    if len(job_tokens) == 0:
        job_tokens = {"general"}

    skill_project_union = skills | project

    match_count = len(job_tokens & skill_project_union)
    match_ratio = match_count / len(job_tokens)

    # Balanced scoring curve (FIXED FAIRNESS)
    score = match_ratio * 65

    factors.append(f"{match_count} relevant keyword matches")

    #  SKILL STRENGTH BOOST 
    strong_skills = {
        "python", "machine", "learning", "nlp",
        "tensorflow", "pytorch", "sql", "aws", "data"
    }

    strong_match = len(job_tokens & strong_skills & skills)
    score += strong_match * 4

    if strong_match > 0:
        factors.append("Strong technical skill alignment")

    # EXPERIENCE (FAIR SCALING) 
    if experience <= 0:
        score += 5
        factors.append("Fresher level considered (no penalty)")
    elif experience <= 2:
        score += 10
        factors.append("Junior experience")
    elif experience <= 5:
        score += 15
        factors.append("Mid-level experience")
    else:
        score += 20
        factors.append("Senior experience")

    # PROJECT QUALITY 
    project_overlap = len(project & job_tokens)
    score += project_overlap * 3

    if project_overlap > 0:
        factors.append("Relevant project experience")

    #  BONUS FOR STRONG CANDIDATES 
    if match_ratio > 0.6 and experience >= 2:
        score += 10
        factors.append("High overall profile strength")

    #  FINAL NORMALIZATION 
    score = max(0, min(100, round(score)))

    #   DECISION 
    if score >= 80:
        recommendation = "Strong Hire"
    elif score >= 65:
        recommendation = "Shortlisted"
    elif score >= 45:
        recommendation = "Needs Review"
    else:
        recommendation = "Not Shortlisted"

    #   EXPLANATION 
    if score >= 80:
        explanation = "Excellent match with job requirements and strong technical alignment."
    elif score >= 65:
        explanation = "Good alignment with job requirements and relevant skill set."
    elif score >= 45:
        explanation = "Partial match with job requirements, some key skills missing."
    else:
        explanation = "Low alignment with job requirements and limited relevant skills."

    return {
        "score": score,
        "recommendation": recommendation,
        "explanation": explanation,
        "top_factors": factors[:4]
    }
