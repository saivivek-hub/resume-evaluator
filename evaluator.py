from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def simple_tokenize(text):
    return [w.lower() for w in text.split() if len(w) > 2]


def evaluate_with_llm(candidate, job_desc):

    skills = candidate.get("skills", "").lower()
    project = candidate.get("project", "").lower()
    experience = candidate.get("experience", 0)

    candidate_text = f"{skills} {project}"

    #  BASE SIMILARITY (STRICTER) 
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([job_desc, candidate_text])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    # Reduce impact (more strict)
    score = similarity * 50   # was 40 → now tighter distribution

    factors = []

    #  JOB TOKEN MATCHING 
    job_tokens = simple_tokenize(job_desc)

    if not job_tokens:
        job_tokens = []

    matches = 0
    for token in job_tokens:
        if token in skills or token in project:
            matches += 1

    token_ratio = matches / max(len(job_tokens), 1)

    # STRONGER PENALTY IF LOW MATCH
    if token_ratio < 0.2:
        score -= 15
        factors.append("Low keyword match penalty")
    else:
        score += token_ratio * 30

    factors.append(f"{matches}/{len(job_tokens)} keyword matches")

    #  STRICT SKILL CHECK 
    required_skills = [
        "python", "machine learning", "nlp",
        "tensorflow", "pytorch", "data"
    ]

    skill_match = 0
    for skill in required_skills:
        if skill in job_desc.lower() and skill in skills:
            skill_match += 1

    score += skill_match * 5
    factors.append(f"{skill_match} required skills matched")

    #  EXPERIENCE SCORING (STRICT) 
    if experience < 1:
        score -= 10
        factors.append("Very low experience penalty")
    elif experience < 3:
        score += 5
        factors.append("Junior level")
    elif experience < 5:
        score += 8
        factors.append("Mid-level experience")
    else:
        score += 10
        factors.append("Senior experience")

    #  PROJECT QUALITY CHECK 
    if len(project.split()) < 10:
        score -= 10
        factors.append("Weak project description penalty")

    if "nlp" in job_desc.lower() and "nlp" in project:
        score += 8
        factors.append("Relevant NLP project")

    #  FINAL NORMALIZATION 
    score = max(0, min(100, int(score)))

    # STRICT DECISION LOGIC 
    if score >= 80:
        rec = "Strong Hire"
    elif score >= 60:
        rec = "Shortlisted"
    elif score >= 40:
        rec = "Needs Review"
    else:
        rec = "Not Shortlisted"

    return {
        "score": score,
        "recommendation": rec,
        "explanation": "Score computed using strict TF-IDF similarity + keyword weighting + penalties.",
        "top_factors": factors[:4]
    }
