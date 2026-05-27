# AI-Augmented Resume Screening and Scheduling System (Prototype)

## What this project does
- Upload PDF resumes (via web UI)
- Extracts text (pdfminer.six) and performs a simple hybrid scoring (technical + soft skills)
- Shortlists candidates based on score and allows scheduling interviews for shortlisted candidates
- Simple dashboard to view candidates and trigger scheduling

## Run locally
1. Create a virtualenv: `python -m venv .venv` and activate it
2. Install: `pip install -r requirements.txt`
3. Run: `python app.py`
4. Open: http://127.0.0.1:5001

## Notes
- This is a prototype: scoring is explainable and rule-based. Replace with ML model as needed.
- For scanned PDFs, add OCR (tesseract) fallback.
