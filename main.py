# main.py - analysis engine

import pdfplumber
import docx
import json

def load_skills():
    with open("skills_database.json", "r") as f:
       return json.load(f)

SKILLS_DB = load_skills()

def extract_text(file_path):
    text = ""

    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    if not isinstance(file_path, str):
        raise ValueError("Invalid file path")

    elif file_path.lower().endswith(".docx"):
        doc = docx.Document(file_path)
        for p in doc.paragraphs:
            text += p.text + "\n"

    return text.strip()


def analyse_skills(text):
    found = []
    all_skills = [skill.lower() for skill in SKILLS_DB["technical_skills"] + SKILLS_DB["soft_skills"]]
    lower_text = text.lower()

    for skill in all_skills:
        if skill in lower_text:
           found.append(skill)

    return found

def calculate_resume_score(skills_found, text):
    score = 0

    # 1️⃣  SKills Match (40)
    max_skills = len(SKILLS_DB["technical_skills"]) + len(SKILLS_DB["soft_skills"])
    skill_score = min(len(skills_found) / max_skills, 1.0) * 40
    score += skill_score

    # 2️⃣  Resume Length (20)
    length = len(text)
    if 800 <= length <= 3000:
        score += 20
    elif 500 <= length < 800 or 3000 < length <= 4000:
        score += 10

    # 3️⃣  Skill Diversity (20)
    tech = set(skill.lower() for skill in SKILLS_DB["technical_skills"])
    soft = set(skill.lower() for skill in SKILLS_DB["soft_skills"])

    tech_found = len([s for s in skills_found if s in tech])
    soft_found = len([s for s in skills_found if s in soft])

    if tech_found >= 3 and soft_found >= 2:
        score += 20
    elif tech_found >= 2:
        score += 10

    # 4️⃣  Keyword Density (20)
    keyword_density = len(skills_found) / max(len(text.split()), 1)
    if keyword_density >= 0.02:
        score += 20
    elif keyword_density >= 0.01:
        score += 10

    return round(score)


def analyze_resume(file_path):

    print("ENGINE received:", file_path)
    # Extract text from the resume
    text = extract_text(file_path)

    # Analyze skills
    skills_found = analyse_skills(text)  # renamed to match return value

    # Calculate score
    score = calculate_resume_score(skills_found, text)
    score = min(score, 100)

    # Keywords to check structure sections
    structure_keywords = [
        "summary",
        "experience",
        "education",
        "skills",
        "projects",
        "certifications",
    ]

    # Count how many structure sections are present
    structure_hits = sum(
        1 for section in structure_keywords
        if section.lower() in text.lower()
    )

    # Optional: preview first 200 characters of resume
    preview = text[:200]

    analysis = (
        f"Resume Score: {score}/100\n\n"
        f"Skills Found ({len(skills_found)}): {', '.join(skills_found)}\n"
        f"Structure Matches: {structure_hits}\n\n"
        "suggestions:\n"
    )

    if score < 50:
        analysis += "- Improve formatting and add more relevant skills.\n"
    elif score < 75:
        analysis += "-Good resume, but consider adding measurable achievements.\n"
    else:
        analysis += "- Strong resume. Minor improvements could increase ATS and portfolio ranking.\n"

    # Return the result as a dictionary
    return {
        "score": score,
        "skills_found": skills_found,
        "length": len(text),
        "structure_hits": structure_hits,
        "text_preview_": preview,
        "full_text": text,
        "analysis": analysis
    }




