from pypdf import PdfReader

SKILLS = {
    "python",
    "flask",
    "sql",
    "mysql",
    "git",
    "github",
    "java",
    "html",
    "css",
    "javascript",
    "rest",
    "api"
    }

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text=""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text.lower()

    return text

def extract_skills(text):
    found = []

    for skill in sorted(SKILLS):
        if skill in text:
            found.append(skill)

    return found

def calculate_match(job_skills, resume_skills):
    if not job_skills:
        return 0

    required = [
        skill.strip().lower()
        for skill in job_skills.split(",")
        ]

    matched = [
        skill
        for skill in required
        if skill in resume_skills
        ]

    score = int(len(matched)/ len(required) * 100)

    return score




























    
