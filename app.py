"""
app.py
------
Main Flask application for the Smart Resume Analyzer.

Routes:
    GET  /          -> Upload form (resume + job description)
    POST /analyze   -> Processes the upload, runs analysis, shows result
    GET  /history    -> Shows all past analyses from the database
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash

from resume_parser import extract_resume_text, clean_text
from analyzer import analyze_resume
from database import init_db, save_analysis, get_history

app = Flask(__name__)
app.secret_key = "smart-resume-analyzer-secret-key"

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the database (creates table if it doesn't exist)
init_db()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    # --- Basic validation ---
    if not resume_file or resume_file.filename == "":
        flash("Please upload a resume file.")
        return redirect(url_for("index"))

    if not allowed_file(resume_file.filename):
        flash("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
        return redirect(url_for("index"))

    if not job_description:
        flash("Please paste a job description.")
        return redirect(url_for("index"))

    # --- Save uploaded file ---
    filename = resume_file.filename
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    resume_file.save(save_path)

    # --- Extract & clean text ---
    try:
        raw_resume_text = extract_resume_text(save_path)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("index"))

    resume_text = clean_text(raw_resume_text)
    jd_text = clean_text(job_description)

    if len(resume_text.strip()) == 0:
        flash("Could not extract any text from the uploaded resume. Try a different file.")
        return redirect(url_for("index"))

    # --- Run analysis ---
    result = analyze_resume(resume_text, jd_text)

    # --- Save to database ---
    save_analysis(
        candidate_file=filename,
        match_score=result["match_score"],
        verdict=result["verdict"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
    )

    return render_template("result.html", filename=filename, result=result)


@app.route("/history")
def history():
    records = get_history()
    return render_template("history.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)
