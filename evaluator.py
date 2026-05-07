import re


def tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))


IMPORTANT_SKILLS = {
    "python",
    "sql",
    "machine",
    "learning",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "flask",
    "django",
    "api",
    "aws",
    "nlp",
    "data",
    "analysis"
}


def evaluate_with_llm(candidate, job_desc):

    skills = tokenize(candidate.get("skills", ""))
    project = tokenize(candidate.get("project", ""))
    resume = tokenize(candidate.get("resume", ""))

    candidate_tokens = skills | project | resume

    experience = candidate.get("experience", 0)

    # ONLY IMPORTANT WORDS FROM JD
    jd_tokens = tokenize(job_desc)
    required_skills = jd_tokens & IMPORTANT_SKILLS

    # MATCHES
    matched_skills = candidate_tokens & required_skills
    missing_skills = required_skills - candidate_tokens

    match_count = len(matched_skills)

    # ---------------- SCORE ----------------
    score = 0

    # SKILL MATCH SCORE
    score += match_count * 12

    # EXPERIENCE SCORE
    if experience >= 5:
        score += 20
    elif experience >= 3:
        score += 15
    elif experience >= 1:
        score += 8
    else:
        score += 2

    # PROJECT BONUS
    project_matches = len(project & IMPORTANT_SKILLS)
    score += project_matches * 5

    # RESUME BONUS
    resume_matches = len(resume & IMPORTANT_SKILLS)
    score += resume_matches * 2

    # PENALTY
    if match_count <= 1:
        score -= 20

    # LIMIT SCORE
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
        explanation = "Excellent technical match with strong experience."
    elif score >= 70:
        explanation = "Good alignment with required skills."
    elif score >= 50:
        explanation = "Some relevant skills matched."
    else:
        explanation = "Low match with required skills."

    return {
        "score": score,
        "recommendation": recommendation,
        "explanation": explanation,
        "missing_skills": list(missing_skills)
    }
