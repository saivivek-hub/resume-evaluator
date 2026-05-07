import re


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
    "aws",
    "nlp",
    "api",
    "data"
}


def tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))


def evaluate_with_llm(candidate, job_desc):

    skills = tokenize(candidate.get("skills", ""))
    project = tokenize(candidate.get("project", ""))
    education = tokenize(candidate.get("education", ""))
    resume = tokenize(candidate.get("resume", ""))

    candidate_tokens = (
        skills
        | project
        | education
        | resume
    )

    job_tokens = tokenize(job_desc)

    required_skills = job_tokens & IMPORTANT_SKILLS

    matched = candidate_tokens & required_skills

    missing = required_skills - candidate_tokens

    experience = candidate.get("experience", 0)

    # ---------------- MATCH SCORE ----------------
    if len(required_skills) == 0:
        skill_score = 0
    else:
        skill_score = (
            len(matched) / len(required_skills)
        ) * 60

    # ---------------- EXPERIENCE ----------------
    if experience >= 5:
        exp_score = 20
    elif experience >= 3:
        exp_score = 15
    elif experience >= 1:
        exp_score = 8
    else:
        exp_score = 2

    # ---------------- PROJECT BONUS ----------------
    project_matches = len(project & IMPORTANT_SKILLS)

    project_score = min(project_matches * 4, 10)

    # ---------------- EDUCATION BONUS ----------------
    education_bonus = 0

    if (
        "computer" in education
        or "engineering" in education
        or "science" in education
    ):
        education_bonus = 5

    # ---------------- FINAL SCORE ----------------
    score = (
        skill_score
        + exp_score
        + project_score
        + education_bonus
    )

    score = round(min(score, 100))

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
        explanation = "Excellent technical alignment with strong profile."
    elif score >= 70:
        explanation = "Good alignment with required skills."
    elif score >= 50:
        explanation = "Partial technical match."
    else:
        explanation = "Low alignment with job requirements."

    return {
        "score": score,
        "recommendation": recommendation,
        "explanation": explanation,
        "missing_skills": list(missing)
    }
