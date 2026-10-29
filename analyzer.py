"""
analyzer.py
-----------
Core logic of the Smart Resume Analyzer.

1. Maintains a list of known skills.
2. Extracts skills from resumes and job descriptions.
3. Uses TF-IDF + Cosine Similarity for text similarity.
4. Calculates skill match and requirement coverage.
5. Combines these components into an overall match score.
6. Provides resume-only analysis with possible relevant roles.
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# A moderate-sized list of common technical and soft skills.
# This acts as our "skill dictionary" for keyword matching.
SKILL_DATABASE = [
    "python", "java", "c++", "c", "javascript", "typescript", "html", "css",
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "nosql",

    "flask", "django", "fastapi", "react", "angular", "vue", "node.js",
    "express.js", "bootstrap", "tailwind",

    "machine learning", "deep learning", "data science", "data analysis",
    "artificial intelligence", "computer vision", "nlp",
    "natural language processing",

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
    "ios development",

    "cybersecurity", "networking", "cloud computing",

    "data structures", "algorithms", "oop",
    "object oriented programming",

    "operating systems", "dbms", "software testing", "unit testing",
]


def extract_skills(text):
    """
    Search the given text for any skill from SKILL_DATABASE.

    Returns:
        A sorted list of detected skills.
    """

    text_lower = text.lower()
    found_skills = set()

    for skill in SKILL_DATABASE:

        # Word-boundary-safe search prevents short skills
        # such as "c" from matching inside unrelated words.
        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(skill)
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return sorted(found_skills)


def compute_text_similarity(resume_text, job_description_text):
    """
    Calculate text similarity between the resume and job description.

    TF-IDF converts the text into numerical vectors.
    Cosine Similarity measures how similar those vectors are.

    Returns:
        Similarity score from 0 to 100.
    """

    documents = [
        resume_text,
        job_description_text
    ]

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def compute_skill_match(resume_skills, jd_skills):
    """
    Calculate how many skills required by the job description
    are present in the resume.

    Example:
        JD skills = 10
        Resume contains 7 of them

        Skill Match = 70%
    """

    if not jd_skills:
        return 0.0

    matched_skills = set(resume_skills) & set(jd_skills)

    skill_match = (
        len(matched_skills) /
        len(set(jd_skills))
    ) * 100

    return round(skill_match, 2)


def compute_requirement_coverage(resume_text, job_description_text):
    """
    Estimate requirement coverage by checking how many
    words from the job description also appear in the resume.

    This provides an additional text-based coverage signal.
    """

    jd_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            job_description_text.lower()
        )
    )

    resume_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            resume_text.lower()
        )
    )

    if not jd_words:
        return 0.0

    common_words = jd_words & resume_words

    coverage = (
        len(common_words) /
        len(jd_words)
    ) * 100

    return round(coverage, 2)


def compute_match_score(
    resume_text,
    job_description_text,
    resume_skills,
    jd_skills
):
    """
    Calculate the overall resume-JD match score.

    Components:
        Skill Match          = 50%
        Text Similarity      = 30%
        Requirement Coverage = 20%

    The final score is a project-defined compatibility metric.
    It should not be interpreted as a probability of getting hired.
    """

    # Calculate skill overlap.
    skill_match = compute_skill_match(
        resume_skills,
        jd_skills
    )

    # Calculate overall text similarity.
    text_similarity = compute_text_similarity(
        resume_text,
        job_description_text
    )

    # Calculate requirement keyword coverage.
    requirement_coverage = compute_requirement_coverage(
        resume_text,
        job_description_text
    )

    # Combine the three components using project-defined weights.
    overall_score = (
        (skill_match * 0.50)
        + (text_similarity * 0.30)
        + (requirement_coverage * 0.20)
    )

    return {
        "overall_score": round(overall_score, 2),
        "skill_match": skill_match,
        "text_similarity": text_similarity,
        "requirement_coverage": requirement_coverage
    }


def analyze_resume(resume_text, job_description_text):
    """
    Analyze a resume against a specific job description.

    This function:
        1. Extracts skills from both texts.
        2. Finds matched, missing and extra skills.
        3. Calculates the overall match score.
        4. Determines a simple match verdict.
    """

    # Extract skills from the resume.
    resume_skills = extract_skills(resume_text)

    # Extract skills from the job description.
    jd_skills = extract_skills(job_description_text)

    # Skills appearing in both resume and job description.
    matched_skills = sorted(
        set(resume_skills) & set(jd_skills)
    )

    # Skills required by the JD but not found in resume.
    missing_skills = sorted(
        set(jd_skills) - set(resume_skills)
    )

    # Skills present in resume but not detected in JD.
    extra_skills = sorted(
        set(resume_skills) - set(jd_skills)
    )

    # Calculate the combined score.
    score_details = compute_match_score(
        resume_text,
        job_description_text,
        resume_skills,
        jd_skills
    )

    match_score = score_details["overall_score"]

    # Count words in the resume.
    word_count = len(resume_text.split())

    # Generate a simple verdict based on the overall score.
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

        # Individual score components.
        "skill_match": score_details["skill_match"],
        "text_similarity": score_details["text_similarity"],
        "requirement_coverage": score_details["requirement_coverage"],

        "verdict": verdict,

        # Skill information.
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,

        # Basic resume information.
        "word_count": word_count,
    }


# ============================================================
# ROLE MAPPING FOR RESUME-ONLY ANALYSIS
# ============================================================

# Each role is mapped to a predefined set of related skills.
# These roles are possible relevant roles, not guaranteed
# job recommendations.
ROLE_SKILLS = {

    "Python Developer": [
        "python",
        "flask",
        "django",
        "fastapi",
        "sql",
        "git"
    ],

    "Backend Developer": [
        "python",
        "java",
        "node.js",
        "sql",
        "rest api",
        "api development",
        "git"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "pandas",
        "numpy",
        "excel",
        "power bi",
        "tableau",
        "data analysis"
    ],

    "Machine Learning Intern": [
        "python",
        "machine learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "data science"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "bootstrap",
        "react",
        "node.js"
    ],

    "Software Developer": [
        "python",
        "java",
        "c++",
        "data structures",
        "algorithms",
        "oop",
        "git"
    ],

    "DevOps / Cloud Intern": [
        "linux",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "git",
        "ci/cd"
    ]
}


def analyze_resume_only(resume_text):
    """
    Analyze a resume without requiring a job description.

    The system detects skills and compares them against
    predefined skill-role mappings.
    """

    # Detect skills from the resume.
    resume_skills = extract_skills(resume_text)

    possible_roles = []

    # Check each predefined role.
    for role, required_skills in ROLE_SKILLS.items():

        # Find skills that match the current role.
        matched = sorted(
            set(resume_skills) & set(required_skills)
        )

        # Only show roles where at least one skill matches.
        if matched:

            role_match_percentage = round(
                (
                    len(matched) /
                    len(required_skills)
                ) * 100,
                2
            )

            possible_roles.append({
                "role": role,
                "match_percentage": role_match_percentage,
                "matched_skills": matched
            })

    # Show roles with higher skill overlap first.
    possible_roles.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    # Count words in the resume.
    word_count = len(resume_text.split())

    return {
        "resume_skills": resume_skills,
        "possible_roles": possible_roles,
        "word_count": word_count
    }