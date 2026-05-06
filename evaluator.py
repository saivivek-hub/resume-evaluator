def simple_tokenize(text):
    return set(text.lower().split())


def evaluate_with_llm(candidate, job_desc):

    skills = simple_tokenize(candidate.get("skills", ""))
    project = simple_tokenize(candidate.get("project", ""))
    job_tokens = simple_tokenize(job_desc)

    #  BASE MATCH 
    total_tokens = len(job_tokens)
    if total_tokens == 0:
        total_tokens = 1

    match = len(job_tokens & (skills | project))

    # softer scoring (IMPORTANT CHANGE)
    score = (match / total_tokens) * 60   # was too harsh before

    factors = []
    factors.append(f"{match}/{len(job_tokens)} keyword match")

    #  SKILLS BONUS
    skill_overlap = len(skills & job_tokens)
    score += skill_overlap * 4

    if skill_overlap > 0:
        factors.append("Skill relevance detected")

    #  EXPERIENCE (BALANCED) 
    exp = candidate.get("experience", 0)

    if exp >= 5:
        score += 20
        factors.append("Strong experience")
    elif exp >= 2:
        score += 12
        factors.append("Moderate experience")
    elif exp >= 1:
        score += 6
        factors.append("Basic experience")
    else:
        score += 2
        factors.append("Fresher")

    #  PROJECT BOOST 
    project_match = len(project & job_tokens)

    if project_match > 0:
        score += project_match * 3
        factors.append("Project relevance")

    #  FINAL NORMALIZATION 
    score = max(0, min(100, int(score)))

    #  DECISION 
    if score >= 75:
        rec = "Strong Hire"
    elif score >= 55:
        rec = "Shortlisted"
    elif score >= 35:
        rec = "Needs Review"
    else:
        rec = "Not Shortlisted"

    return {
        "score": score,
        "recommendation": rec,
        "explanation": "Balanced scoring using keyword overlap + experience + project relevance.",
        "top_factors": factors[:4]
    }
