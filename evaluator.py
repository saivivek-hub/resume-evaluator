def simple_tokens(text):
    return set(text.lower().split())


def evaluate_with_llm(candidate, job_desc):

    skills = simple_tokens(candidate.get("skills", ""))
    project = simple_tokens(candidate.get("project", ""))
    job_tokens = simple_tokens(job_desc)

    factors = []

    #  FLEXIBLE MATCH SCORE 
    if len(job_tokens) == 0:
        job_tokens = {"general"}

    overlap = len(job_tokens & (skills | project))
    overlap_ratio = overlap / len(job_tokens)

    # smoother curve (IMPORTANT FIX)
    score = overlap_ratio * 70

    factors.append(f"{overlap} keyword matches")

    #  SOFT SKILL BOOST 
    skill_match = len(skills & job_tokens)
    score += skill_match * 3
    if skill_match:
        factors.append("Skill relevance detected")

    #  EXPERIENCE 
    exp = candidate.get("experience", 0)

    exp_bonus = min(exp * 3, 15)  # capped so it doesn't dominate
    score += exp_bonus

    if exp > 0:
        factors.append(f"{exp} years experience considered")

    #  PROJECT QUALITY 
    project_score = len(project & job_tokens)
    score += project_score * 2

    if project_score:
        factors.append("Relevant project keywords found")

    #  FINAL NORMALIZATION 
    score = max(0, min(100, round(score)))

    #  EXPLANATION
    explanation_parts = []

    if overlap_ratio > 0.5:
        explanation_parts.append("Strong job match based on skills alignment")
    elif overlap_ratio > 0.2:
        explanation_parts.append("Moderate job relevance")
    else:
        explanation_parts.append("Low keyword alignment with job description")

    if exp >= 5:
        explanation_parts.append("Strong experience level")
    elif exp >= 2:
        explanation_parts.append("Moderate experience level")
    else:
        explanation_parts.append("Entry level experience considered")

    explanation = ", ".join(explanation_parts)

    #  DECISION 
    if score >= 75:
        rec = "Strong Hire"
    elif score >= 55:
        rec = "Shortlisted"
    elif score >= 40:
        rec = "Needs Review"
    else:
        rec = "Not Shortlisted"

    return {
        "score": score,
        "recommendation": rec,
        "explanation": explanation,
        "top_factors": factors[:4]
    }
