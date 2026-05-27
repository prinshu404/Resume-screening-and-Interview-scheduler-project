# Simple hybrid scoring and skill extraction module.
# This is a lightweight, explainable version of the hybrid model from the pitch.
import re

REQUIRED_SKILLS = {'python','data','sql','flask','django','ml','machine learning','tensorflow','pandas','numpy','aws','docker','kubernetes','react','javascript','java','c++'}

SOFT_SKILL_KEYWORDS = {'communication','team','lead','leadership','collaborat','problem solv','adapt','organis','creative','initiative','ownership'}

def extract_skills_from_text(text):
    text_low = text.lower()
    found = set()
    for kw in REQUIRED_SKILLS:
        if kw in text_low:
            found.add(kw)
    return ', '.join(sorted(found))

def soft_skill_score(text):
    t = text.lower()
    count = 0
    for kw in SOFT_SKILL_KEYWORDS:
        if kw in t:
            count += 1
    # normalize
    return min(1.0, count / 5.0)

def technical_score(text):
    t = text.lower()
    count = 0
    for kw in REQUIRED_SKILLS:
        if kw in t:
            count += 1
    # rough normalization by number of required skills
    return min(1.0, count / max(1, len(REQUIRED_SKILLS)))

def hybrid_score_from_text(text, skills_str):
    # Combined weighted score: technical 0.7, soft 0.3
    ts = technical_score(text)
    ss = soft_skill_score(text)
    return 0.7 * ts + 0.3 * ss
