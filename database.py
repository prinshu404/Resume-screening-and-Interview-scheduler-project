import sqlite3
DB_NAME = "ats.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        skills TEXT,
        shortlisted INTEGER,
        resume_filename TEXT,
        score REAL,
        interview_date TEXT,
        interview_time TEXT,
        interviewer TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_candidate(name, email, skills, shortlisted, resume_filename, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # insert or replace to update by email
    c.execute("""
    INSERT OR REPLACE INTO candidates (id, name, email, skills, shortlisted, resume_filename, score)
    VALUES (
        COALESCE((SELECT id FROM candidates WHERE email = ?), NULL),
        ?, ?, ?, ?, ?, ?
    )
    """, (email, name, email, skills, shortlisted, resume_filename, score))
    conn.commit()
    conn.close()

def get_candidate_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM candidates WHERE email=?", (email,))
    r = c.fetchone()
    conn.close()
    return r

def update_interview(email, date, time, interviewer):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    UPDATE candidates
    SET interview_date=?, interview_time=?, interviewer=?
    WHERE email=?
    """, (date, time, interviewer, email))
    conn.commit()
    conn.close()

def list_candidates():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM candidates ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows
