# Smart Resume Analyzer

A web application that compares a candidate's resume against a job
description, gives a match score, and highlights matched/missing skills.
Built as a college mini-project using Python, Flask, and scikit-learn.

---

## 1. Project Planning

**Title:** Smart Resume Analyzer

**Problem Statement:** Recruiters and students manually compare resumes
against job descriptions, which is slow and inconsistent. There's no quick
way to check how well a resume matches a specific job posting.

**Objective:** Build a web app where a user uploads a resume (PDF/DOCX/TXT)
and pastes a job description; the app returns a match score and a skill
gap analysis.

**Proposed Solution:** Extract text from the resume, extract text from the
job description, compare them using TF-IDF vectorization + cosine
similarity (a standard NLP text-matching technique), and separately detect
skills from a keyword dictionary to show matched/missing/extra skills.

**Main Features:**
- Upload resume as PDF, DOCX, or TXT
- Paste any job description
- Get a 0–100% match score
- See matched skills, missing skills, and extra skills
- View history of all past analyses (stored in SQLite)

**Target Users:** Students preparing resumes, and recruiters/mentors doing
quick resume screening.

**Technology Stack:**
| Layer | Technology | Why |
|---|---|---|
| Backend | Python + Flask | Lightweight, beginner-friendly, easy to explain |
| Resume parsing | pypdf, python-docx | Standard libraries for reading PDF/DOCX text |
| Text matching | scikit-learn (TF-IDF + cosine similarity) | Simple, well-known NLP technique, no heavy ML training needed |
| Database | SQLite | Zero-config, file-based, perfect for a mini project |
| Frontend | HTML, CSS, JavaScript (no framework) | Keeps things simple and fully understandable |

**Expected Output:** A match percentage, a verdict (Excellent/Good/Average/
Poor Match), a list of matched and missing skills, and a history table of
all analyses performed.

---

## 2. Project Structure

```text
Smart_Resume_Analyzer/
│
├── app.py                     # Main Flask application (routes)
├── analyzer.py                # Skill extraction + TF-IDF match scoring
├── resume_parser.py           # PDF/DOCX/TXT text extraction
├── database.py                # SQLite setup + save/read history
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html               # Shared layout (navbar, footer)
│   ├── index.html              # Upload form page
│   ├── result.html             # Analysis result page
│   └── history.html            # History table page
│
├── static/
│   ├── css/style.css
│   └── js/script.js
│
├── sample_data/
│   ├── sample_resume.txt        # Sample resume for demo
│   └── sample_job_description.txt
│
├── uploads/                    # Uploaded resumes are saved here (auto-created)
└── database/                   # resume_analyzer.db is auto-created here
```

---

## 3. Installation (Windows + VS Code + PowerShell)

1. **Create/extract the project folder**, e.g.:
   ```powershell
   cd C:\Users\YourName\Desktop
   ```
   Extract or copy `Smart_Resume_Analyzer` here, then:
   ```powershell
   cd Smart_Resume_Analyzer
   ```

2. **Create a virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
   (Your prompt should now show `(venv)`.)

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```powershell
   python app.py
   ```

5. **Open in browser:**
   ```
   http://127.0.0.1:5000
   ```

6. **Stop the server:** Press `CTRL + C` in the terminal.
   **Restart later:**
   ```powershell
   venv\Scripts\activate
   python app.py
   ```

---

## 4. Demonstration Flow

```text
1. Open http://127.0.0.1:5000 — the Analyze page loads.
2. Click the upload box and select sample_data/sample_resume.txt
   (or any real PDF/DOCX resume).
3. Paste the contents of sample_data/sample_job_description.txt
   into the Job Description box.
4. Click "Analyze Match".
5. The app extracts resume text, compares it with the job description,
   and shows: match score, verdict, matched skills, missing skills.
6. Click "View History" to show all past analyses stored in the database.
```

---

## 5. How the Project Works

1. **Input:** User uploads a resume file and pastes a job description.
2. **Text extraction:** `resume_parser.py` reads the file (PDF via `pypdf`,
   DOCX via `python-docx`, or plain text) and converts it into a single
   text string.
3. **Skill extraction:** `analyzer.py` scans both texts against a
   predefined list of ~70 common technical/soft skills and records which
   ones appear in each document.
4. **Similarity scoring:** The resume text and job description text are
   converted into TF-IDF vectors (numeric representations of word
   importance), and cosine similarity between the two vectors gives a
   score from 0 to 1, converted to a percentage.
5. **Output:** The match score, verdict, and skill comparison (matched /
   missing / extra) are shown on the result page and saved to the SQLite
   database.

---

## 6. Common Errors & Fixes

| # | Error | Fix |
|---|---|---|
| 1 | `ModuleNotFoundError: No module named 'flask'` | Activate the venv and run `pip install -r requirements.txt` again. |
| 2 | `'python' is not recognized` | Install Python from python.org and check "Add Python to PATH" during install. |
| 3 | Port 5000 already in use | Close other running Flask apps, or change `app.run(debug=True, port=5001)`. |
| 4 | Uploaded PDF gives empty text | The PDF may be a scanned image, not real text. Use a text-based resume PDF instead. |
| 5 | `TemplateNotFound: index.html` | Run `python app.py` from inside the `Smart_Resume_Analyzer` folder, not a parent folder. |
| 6 | `sqlite3.OperationalError: unable to open database file` | Make sure the `database/` folder exists (it is auto-created by `init_db()`); check folder write permissions. |
| 7 | CSS/JS not loading | Confirm files are inside `static/css/` and `static/js/`, and browser cache is refreshed (Ctrl+Shift+R). |
| 8 | `UnicodeDecodeError` reading a `.txt` resume | Save the text file with UTF-8 encoding, or re-upload as PDF/DOCX. |
| 9 | Score always very low even for a good resume | Job description text may be too short — TF-IDF needs enough words to compare meaningfully. |
| 10 | Virtual environment not activating | On PowerShell, if blocked by execution policy, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then retry `venv\Scripts\activate`. |

---

## 7. Limitations

- Skill detection is keyword-based (not true NLP understanding) — it won't
  catch skills phrased very differently than the dictionary entries.
- Match score reflects text similarity, not actual candidate quality or
  experience level.
- Scanned/image-based PDF resumes without selectable text won't extract
  properly (no OCR is included).
- No user authentication — anyone using the app can see the shared history.
- Not intended for production hiring decisions; it's a demonstration tool.

**To make it production-ready** you would add: OCR for scanned PDFs, a
larger/auto-updated skill database, user accounts and authentication, and
a more advanced NLP model (e.g. embeddings) instead of TF-IDF.

---

## 8. Explain This Project in 2 Minutes (Viva Script)

"My project is called Smart Resume Analyzer. The problem is that comparing
a resume to a job description manually is slow and inconsistent. My
solution is a web app built with Python and Flask where a user uploads a
resume and pastes a job description. The app extracts text from the
resume using `pypdf` or `python-docx`, and then uses a technique called
TF-IDF with cosine similarity from scikit-learn to measure how similar the
resume text is to the job description — this gives a match score out of
100. I also built a skill-matching feature that checks a list of common
skills and shows which ones are present in both documents, which ones are
missing, and which extra skills the resume has. All results are saved in
an SQLite database so I can show a history of past analyses. The main
limitation is that skill detection is keyword-based, so it won't catch
skills phrased differently. In the future, this could be improved using
more advanced NLP models like word embeddings, and by adding OCR support
for scanned resumes."

---

## 9. Cheat Sheet: Key Terms

| Term | Simple Meaning | Where Used |
|---|---|---|
| TF-IDF | A way to turn text into numbers based on how important each word is | `analyzer.py` — `compute_match_score()` |
| Cosine Similarity | Measures how similar two text vectors are (0 to 1) | `analyzer.py` — `compute_match_score()` |
| Flask | A lightweight Python web framework | `app.py` — defines routes |
| Route | A URL path the app responds to (e.g. `/analyze`) | `app.py` |
| SQLite | A file-based database needing no server setup | `database.py` |
| Skill Dictionary | Predefined list of skills to search for in text | `analyzer.py` — `SKILL_DATABASE` |
| Jinja2 Template | HTML files with `{{ }}` placeholders filled by Flask | `templates/*.html` |
| Virtual Environment (venv) | An isolated Python environment for a project's packages | Installation steps |

---

## 10. Testing

| Test Case | Input | Expected Output | Status |
|---|---|---|---|
| Upload valid TXT resume + JD | sample_resume.txt + sample JD | Match score and skill lists shown | Pass |
| Upload with no file | Submit form without selecting a file | Flash message: "Please upload a resume file." | Pass |
| Upload with empty job description | Resume file only, no JD text | Flash message: "Please paste a job description." | Pass |
| Upload unsupported file type (.png) | image file | Flash message about unsupported file type | Pass |
| View history after one analysis | Navigate to `/history` | Table shows the analysis just performed | Pass |
| View history with zero analyses | Fresh database | "No analyses yet" empty state shown | Pass |

---

## 11. Future Scope

- Add OCR (e.g. `pytesseract`) for scanned/image resumes.
- Use word embeddings (e.g. spaCy or Sentence-Transformers) for smarter
  semantic matching instead of pure keyword overlap.
- Add user login so each user only sees their own history.
- Allow bulk resume upload and ranking for recruiters.
- Export analysis results as a PDF report.
