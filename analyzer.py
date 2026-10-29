"""
analyzer.py
-----------
Core logic of the Smart Resume Analyzer.

1. Maintains a list of known skills.
2. Extracts skills found in resume text and job description text.
3. Uses TF-IDF + Cosine Similarity (scikit-learn) to compute a
   match score between the resume and the job description.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A moderate-sized list of common technical & soft skills.
# This acts as our "skill dictionary" for keyword matching.
SKILL_DATABASE = [
    "python", "java", "c++", "c", "javascript", "typescript", "html", "css",
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "nosql",
    "flask", "django", "fastapi", "react", "angular", "vue", "node.js",
    "express.js", "bootstrap", "tailwind",
    "machine learning", "deep learning", "data science", "data analysis",
    "artificial intelligence", "computer vision", "nlp", "natural language processing",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "opencv",
    "git", "github", "docker", "kubernetes", "linux", "aws", "azure",
    "google cloud", "ci/cd", "jenkins",
    "excel", "power bi", "tableau",
    "rest api", "api development", "microservices",
    "agile", "scrum", "project management",
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "time management", "presentation skills",
    "c#", ".net", "php", "swift", "kotlin", "android development",
    "ios development", "cybersecurity", "networking", "cloud computing",
    "data structures", "algorithms", "oop", "object oriented programming",
    "operating systems", "dbms", "software testing", "unit testing",
]


def extract_skills(text):
    """
    Search the given text for any skill from SKILL_DATABASE.
    Returns a sorted list of matched skills (case-insensitive).
    """
    text_lower = text.lower()
    found_skills = set()

    for skill in SKILL_DATABASE:
        # Use word-boundary-safe search so "c" doesn't match inside "career"
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return sorted(found_skills)


def compute_match_score(resume_text, job_description_text):
    """
    Compute a similarity score (0-100) between the resume and the
    job description using TF-IDF vectorization + cosine similarity.
    """
    documents = [resume_text, job_description_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    score = round(similarity * 100, 2)
    return score


def analyze_resume(resume_text, job_description_text):
    """
    Main analysis function. Combines skill extraction and score
    computation, and returns a dictionary with all results needed
    by the web page.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description_text)

    matched_skills = sorted(set(resume_skills) & set(jd_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))
    extra_skills = sorted(set(resume_skills) - set(jd_skills))

    match_score = compute_match_score(resume_text, job_description_text)

    # Simple word count as a basic resume-quality signal
    word_count = len(resume_text.split())

    if match_score >= 75:
        verdict = "Excellent Match"
    elif match_score >= 50:
        verdict = "Good Match"
    elif match_score >= 25:
        verdict = "Average Match"
    else:
        verdict = "Poor Match"

    return {
        "match_score": match_score,
        "verdict": verdict,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "word_count": word_count,
    }
