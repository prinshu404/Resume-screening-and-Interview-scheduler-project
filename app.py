from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
from database import init_db, insert_candidate, get_candidate_by_email, update_interview, list_candidates
from model import hybrid_score_from_text, extract_skills_from_text
from pdfminer.high_level import extract_text

# -------------------------
# CONFIGURATION
# -------------------------
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.secret_key = "dev-secret"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if missing
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize database
init_db()

# -------------------------
# UTILITY
# -------------------------
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()

    # Resume exists?
    if "resume" not in request.files:
        flash("No resume uploaded")
        return redirect(url_for("index"))

    file = request.files["resume"]

    if file.filename == "":
        flash("No file selected")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Only PDF files are allowed")
        return redirect(url_for("index"))

    # Save file
    filename = secure_filename(email + "_" + file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    # Extract text from PDF
    try:
        text = extract_text(save_path) or ""
    except Exception as e:
        app.logger.error("PDF extraction error: %s", e)
        text = ""

    # AI Skill Extraction + Scoring
    skills = extract_skills_from_text(text)
    score = hybrid_score_from_text(text, skills)

    # shortlisted = 1 if score >= 0.5 else 0
    shortlisted = 1 if score >= 0.25 else 0


    # Save to DB
    insert_candidate(name, email, skills, shortlisted, filename, score)

    if shortlisted:
        return redirect(url_for("schedule", email=email))
    else:
        return render_template("result.html", shortlisted=False, name=name, score=score)


@app.route("/schedule/<email>", methods=["GET", "POST"])
def schedule(email):
    candidate = get_candidate_by_email(email)

    if not candidate:
        flash("Candidate not found")
        return redirect(url_for("index"))

    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]
        interviewer = request.form["interviewer"]

        update_interview(email, date, time, interviewer)

        return render_template(
            "result.html",
            shortlisted=True,
            name=candidate[1],
            date=date,
            time=time,
            interviewer=interviewer,
        )

    return render_template("schedule.html", candidate=candidate)


@app.route("/dashboard")
def dashboard():
    candidates = list_candidates()
    return render_template("dashboard.html", candidates=candidates)


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
