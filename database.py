"""
database.py
------------
Handles all SQLite database operations for storing and
retrieving resume analysis history.
"""

import sqlite3
import os
from datetime import datetime

DB_FOLDER = os.path.join(os.path.dirname(__file__), "database")
DB_PATH = os.path.join(DB_FOLDER, "resume_analyzer.db")


def init_db():
    """Create the database folder and analyses table if needed."""

    os.makedirs(DB_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the original table if it does not exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_file TEXT NOT NULL,
            match_score REAL NOT NULL,
            verdict TEXT NOT NULL,
            matched_skills TEXT,
            missing_skills TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # ---------------------------------------------------------
    # Add analysis_type column for old databases.
    # Existing records will be treated as Job Match.
    # ---------------------------------------------------------

    cursor.execute("PRAGMA table_info(analyses)")
    columns = [column[1] for column in cursor.fetchall()]

    if "analysis_type" not in columns:
        cursor.execute("""
            ALTER TABLE analyses
            ADD COLUMN analysis_type TEXT NOT NULL DEFAULT 'Job Match'
        """)

    conn.commit()
    conn.close()


def save_analysis(
    candidate_file,
    match_score,
    verdict,
    matched_skills,
    missing_skills,
    analysis_type="Job Match"
):
    """Insert one analysis record into the database."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyses (
            candidate_file,
            match_score,
            verdict,
            matched_skills,
            missing_skills,
            created_at,
            analysis_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_file,
        match_score,
        verdict,
        ", ".join(matched_skills),
        ", ".join(missing_skills),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        analysis_type,
    ))

    conn.commit()
    conn.close()


def get_history():
    """Return all past analyses, most recent first."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows