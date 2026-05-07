from llama_parse import LlamaParse
from dotenv import load_dotenv
import os
import re

load_dotenv()


parser = LlamaParse(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    result_type="markdown"
)


def extract_email(text):
    pattern = r'[\w\.-]+@[\w\.-]+'
    match = re.search(pattern, text)
    return match.group(0) if match else ""


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


def extract_skills(text):
    found = []

    lower = text.lower()

    for skill in IMPORTANT_SKILLS:
        if skill.lower() in lower:
            found.append(skill)

    return ", ".join(found)


def parse_resume(uploaded_file):

    documents = parser.load_data(uploaded_file)

    full_text = "\n".join([doc.text for doc in documents])

    lines = full_text.split("\n")

    # Basic name extraction
    name = lines[0].strip() if lines else ""

    email = extract_email(full_text)

    }
