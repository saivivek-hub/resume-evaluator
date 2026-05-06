def tokenize(text):
    return set(text.lower().split())


def evaluate_with_llm(candidate, job_desc):

    #  INPUTS 
    skills = tokenize(candidate.get("skills", ""))
    project = tokenize(candidate.get("project", ""))
    resume = tokenize(candidate.get("resume", ""))
    job_tokens = tokenize(job_desc)

    experience = candidate.get("experience", 0)

    factors = []

    #  SAFETY CHECK 
    if not job_tokens:
        job_tokens = {"general"}

    #  CORE MATCH 
    combined_profile = skills | project | resume

    match_count = len(job_tokens & combined_profile)
    match_ratio = match_count / len(job_tokens)

    # FAIR SCORING CURVE (FIXED HARSHNESS)
    score = match_ratio * 65
    factors.append(f"{match_count} keyword matches found")

    #  SKILL MATCH BOOST 
    skill_match = len(job_tokens & skills)
    score += skill_match * 4

    if skill_match:
        factors.append("Strong skill alignment")

    #  EXPERIENCE (BALANCED) 
    if experience <= 0:
        score += 5
        factors.append("Fresher considered fairly")
    elif experience <= 2:
        score += 10
        factors.append("Junior level experience")
    elif experience <= 5:
        score += 15
        factors.append("Mid-level experience")
    else:
        score += 20
        factors.append("Senior experience")

    #  PROJECT MATCH 
    project_match = len(job_tokens & project)
    score += project_match * 3

    if project_match:
        factors.append("Relevant project experience")

    #  RESUME MATCH 
    resume_match = len(job_tokens & resume)
    score += resume_match * 2

    #  BONUS LOGIC 
    if match_ratio > 0.6 and experience >= 2:
        score += 10
        factors.append("High-quality candidate profile")

    #  FINAL SCORE 
    score = max(0, min(100, round(score)))

    #  DECISION 
    if score >= 80:
        recommendation = "Strong Hire"
    elif score >= 60:
        recommendation = "Shortlisted"
    elif score >= 40:
        recommendation = "Needs Review"
    else:
        recommendation = "Not Shortlisted"

    #  EXPLANATION 
    explanation_parts = []

    if skill_match > 0:
        explanation_parts.append("Good skill-job alignment")
    else:
        explanation_parts.append("Limited skill match")

    if project_match > 0:
        explanation_parts.append("Relevant project experience")
    else:
        explanation_parts.append("Project relevance is weak")

    if experience > 2:
        explanation_parts.append("Good experience level")
    else:
        explanation_parts.append("Entry-level candidate")

    explanation = ", ".join(explanation_parts)

    #  MISSING SKILLS 
    missing_skills = list(job_tokens - skills)

    return {
        "score": score,
        "recommendation": recommendation,
        "explanation": explanation,
        "top_factors": factors[:4],
        "missing_skills": missing_skills[:6]
    }
