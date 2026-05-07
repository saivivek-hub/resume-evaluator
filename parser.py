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


def parse_resume(uploaded_file):

    reader = PdfReader(uploaded_file)

    full_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text + "\n"

    lines = full_text.split("\n")

    name = ""

    if len(lines) > 0:
        name = lines[0].strip()

    email = extract_email(full_text)

    skills = extract_skills(full_text)

    return {
        "name": name,
        "email": email,
        "skills": skills,
        "resume_text": full_text
    }
