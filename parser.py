import re
from pypdf import PdfReader


IMPORTANT_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "flask",
    "django",
    "aws",
    "nlp",
    "api"
]


def extract_email(text):

    pattern = r'[\w\.-]+@[\w\.-]+'

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return ""


def extract_skills(text):

    found = []

    lower = text.lower()

    for skill in IMPORTANT_SKILLS:
        if skill.lower() in lower:
            found.append(skill)

    return ", ".join(found)


def extract_section(text, keywords):

    lines = text.split("\n")

    collected = []

    capture = False

    for line in lines:

        lower = line.lower().strip()

        if any(k in lower for k in keywords):
            capture = True
            continue

        # stop at next heading
        if capture and (
            "experience" in lower
            or "education" in lower
            or "project" in lower
            or "skills" in lower
            or "summary" in lower
        ):
            break

        if capture:
            collected.append(line)

    return " ".join(collected).strip()


def parse_resume(uploaded_file):

    reader = PdfReader(uploaded_file)

    full_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            full_text += text + "\n"

    lines = full_text.split("\n")

    name = lines[0].strip() if lines else ""

    email = extract_email(full_text)

    skills = extract_skills(full_text)

    education = extract_section(
        full_text,
        ["education", "academic"]
    )

    project = extract_section(
        full_text,
        ["project", "projects"]
    )

    return {
        "name": name,
        "email": email,
        "skills": skills,
        "education": education,
        "project": project,
        "resume_text": full_text
    }
