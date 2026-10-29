# Viva Preparation — Smart Resume Analyzer

## Basic Questions

1. **What is the objective of your project?**
   To automatically compare a resume against a job description and show a
   match score along with matched/missing skills.

2. **What problem does it solve?**
   Manually comparing resumes to job descriptions is slow and inconsistent.
   This tool makes that comparison instant and objective.

3. **Who are the target users?**
   Students checking their resume against a job posting, and
   recruiters/mentors doing a quick first-pass screening.

4. **What are the main features?**
   Resume upload (PDF/DOCX/TXT), job description input, match score,
   skill gap analysis, and analysis history.

5. **What technology stack did you use?**
   Python and Flask for the backend, scikit-learn for text matching,
   pypdf/python-docx for file reading, SQLite for storage, and plain
   HTML/CSS/JavaScript for the frontend.

## Technical Questions

6. **How does the frontend communicate with the backend?**
   The HTML form submits data via an HTTP POST request to the `/analyze`
   Flask route, which processes it and renders a result page.

7. **What is Flask?**
   A lightweight Python web framework used to define routes (URLs) and
   render HTML pages.

8. **How do you extract text from a PDF?**
   Using the `pypdf` library's `PdfReader`, which reads each page and
   extracts its text.

9. **How do you extract text from a DOCX file?**
   Using the `python-docx` library, which reads paragraphs from the
   Word document.

10. **What database are you using, and why?**
    SQLite, because it's file-based, needs no separate server, and is
    ideal for a small project that just needs to store analysis history.

11. **What table structure does your database have?**
    One table `analyses` with columns: id, candidate_file, match_score,
    verdict, matched_skills, missing_skills, created_at.

12. **What algorithm computes the match score?**
    TF-IDF (Term Frequency–Inverse Document Frequency) vectorization
    followed by cosine similarity between the resume vector and the job
    description vector.

13. **What is TF-IDF in simple terms?**
    It converts text into numbers, giving more weight to words that are
    important and distinctive to a document, and less weight to very
    common words.

14. **What is cosine similarity?**
    A measure of how similar two vectors are, based on the angle between
    them — a value of 1 means identical direction (very similar text), 0
    means no similarity.

15. **How is skill matching done separately from the score?**
    A predefined list of skills (`SKILL_DATABASE`) is searched for in
    both the resume and the job description text using pattern matching,
    and the two sets are compared.

16. **What happens if the uploaded file format is not supported?**
    The app shows a flash message telling the user only PDF, DOCX, or
    TXT files are supported, and redirects back to the upload page.

17. **How is security handled for file uploads?**
    File extensions are checked against an allow-list before saving, and
    files are stored in a dedicated `uploads/` folder rather than
    executed.

18. **How does data flow from input to output?**
    User uploads file + JD text → Flask saves file → text extracted →
    text cleaned → TF-IDF score computed → skills extracted and compared
    → result saved to DB → result rendered on the result page.

## Project-Specific Questions

19. **Why did you choose this project?**
    Resume screening is a real, relatable problem for students, and it
    let me combine web development with a practical NLP technique.

20. **Why did you choose TF-IDF instead of a deep learning model?**
    TF-IDF is simple, fast, doesn't need training data or a GPU, and is
    easy to explain and justify in a college mini-project.

21. **How does your system work overall?**
    It takes a resume and a job description, extracts their text,
    compares them numerically and by keyword, and shows a match score
    plus skill gaps.

22. **What happens with invalid input (e.g., no file selected)?**
    The app validates the form and shows a clear message asking the user
    to provide the missing input, without crashing.

23. **What are the limitations of your project?**
    Skill detection is keyword-based, it doesn't do OCR for scanned PDFs,
    and it doesn't judge experience quality — only text similarity.

24. **What challenges did you face?**
    Handling different file formats consistently, making sure the skill
    list didn't produce false matches (e.g. "c" matching inside another
    word), and designing a clear, simple UI.

25. **How can the project be improved?**
    By adding OCR support, a larger skill database, semantic matching
    using embeddings, and user accounts.

26. **What is the future scope?**
    Bulk resume ranking for recruiters, exporting reports as PDF, and
    smarter NLP-based skill extraction.

---

## Possible Trick Questions

**Q: Why didn't you use a more advanced NLP model like BERT?**
A: For a mini-project, TF-IDF is lightweight, doesn't need a GPU or large
training data, and is easy to explain and justify — the goal was a
practical, understandable, running tool, not state-of-the-art accuracy.

**Q: What happens if the input job description is very short?**
A: The match score can become less reliable, since TF-IDF needs enough
words in both documents to compare meaningfully. This is a known
limitation.

**Q: Is the result always accurate?**
A: No — it's a text-similarity measure, not a guarantee of candidate
quality. It's meant as a helpful screening aid, not a final decision-maker.

**Q: Can this system work in real-world hiring conditions?**
A: It could support a first-pass screening, but it isn't production-ready
— it lacks authentication, OCR, and more advanced NLP for real deployment.

**Q: What part did you implement yourself?**
A: I designed the Flask app structure, wrote the skill-matching logic and
TF-IDF scoring, built the database layer, and designed the frontend
templates and styling myself, using scikit-learn, pypdf, and python-docx
as supporting libraries rather than writing my own PDF parser or ML
library from scratch.

**Q: How would you scale this project for many users?**
A: Move from SQLite to a server-based database like PostgreSQL, add user
authentication, and deploy behind a proper web server (e.g. Gunicorn +
Nginx) instead of Flask's development server.

**Q: What would you change in version 2?**
A: Add OCR for scanned resumes, use semantic embeddings instead of pure
keyword skill matching, and add user accounts so each person has their
own private history.
