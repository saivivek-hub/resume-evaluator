import random
import re


def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

    stopwords = {
        "and", "the", "for", "with", "you", "are", "this",
        "that", "will", "have", "job", "looking", "role",
        "responsibilities", "requirements"
    }

    return list(set([w for w in words if w not in stopwords]))


def evaluate_with_llm(candidate, job_desc):

    skills = candidate["skills"].lower()
    experience = candidate["experience"]
    education = candidate["education"].lower()
    project = candidate["project"].lower()

    score = 0

    # 🔥 extract JD keywords
    jd_keywords = extract_keywords(job_desc)

    # SKILL MATCH (MAJOR WEIGHT)
    match_count = 0

    for k in jd_keywords:
        if k in skills:
            score += 8   # increased weight
            match_count += 1

    # boost if many matches
    score += match_count * 2

    #  EXPERIENCE (IMPORTANT)
    score += experience * 8   # increased weight

    #  EDUCATION BOOST
    if "bachelor" in education:
        score += 10
    if "master" in education:
        score += 20
    if "phd" in education:
        score += 25

    #  PROJECT MATCHING
    project_matches = 0
    for k in jd_keywords:
        if k in project:
            score += 5
            project_matches += 1

    score += project_matches * 2

    # BONUS FOR STRONG MATCH
    if match_count >= 5:
        score += 15

    if match_count >= 8:
        score += 20

    # SMALL RANDOM VARIATION
    score += random.randint(0, 3)

    # NORMALIZE
    score = max(0, min(score, 100))

    # RECOMMENDATION LOGIC
    if score >= 80:
        rec = "Strong Hire"
    elif score >= 60:
        rec = "Consider"
    else:
        rec = "Reject"

    explanation = f"""
Matched Keywords: {match_count}
Project Matches: {project_matches}
Experience: {experience}

Final Score: {score}
"""

    return {
        "score": score,
        "recommendation": rec,
        "explanation": explanation
    }