import re


def tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))


def evaluate_with_llm(candidate, job_desc):

    skills = tokenize(candidate.get("skills", ""))
    project = tokenize(candidate.get("project", ""))
    resume = tokenize(candidate.get("resume", ""))

    candidate_tokens = skills | project | resume

    job_tokens = tokenize(job_desc)

    experience = candidate.get("experience", 0)

    # ---------------- MATCHING ----------------
    matched_skills = candidate_tokens & job_tokens
    missing_skills = job_tokens - candidate_tokens

    match_count = len(matched_skills)

    if len(job_tokens) == 0:
        match_ratio = 0
    else:
        match_ratio = match_count / len(job_tokens)

    # ---------------- BASE SCORE ----------------
    score = match_ratio * 70

    # ---------------- IMPORTANT TECH SKILLS ----------------
    important_skills = {
        "python", "sql", "machine", "learning",
        "tensorflow", "pytorch", "pandas",
        "numpy", "aws", "flask", "api"
    }

    strong_matches = len(candidate_tokens & important_skills)
    score += strong_matches * 5

    # ---------------- EXPERIENCE ----------------
    if experience >= 5:
        score += 20
    elif experience >= 3:
        score += 15
    elif experience >= 1:
        score += 8
    else:
        score += 2

    # ---------------- PROJECT BONUS ----------------
    project_bonus = len(project & important_skills)
    score += project_bonus * 3

    # ---------------- PENALTY ----------------
    if match_count <= 2:
        score -= 15

    # ---------------- NORMALIZE ----------------
    score = max(0, min(100, round(score)))

    # ---------------- RECOMMENDATION ----------------
    if score >= 85:
        recommendation = "Strong Hire"
    elif score >= 70:
        recommendation = "Shortlisted"
    elif score >= 50:
        recommendation = "Needs Review"
    else:
        recommendation = "Not Shortlisted"

    # ---------------- EXPLANATION ----------------
    if score >= 85:
        explanation = "Excellent technical alignment with strong relevant experience."
    elif score >= 70:
        explanation = "Good match with required technical skills and project background."
    elif score >= 50:
        explanation = "Partial alignment with some relevant skills present."
    else:
        explanation = "Limited alignment with required job skills."

    return {
        "score": score,
        "recommendation": recommendation,
        "explanation": explanation,
        "missing_skills": list(missing_skills)[:5]
    }
