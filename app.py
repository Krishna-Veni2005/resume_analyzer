from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy

from src.components.resume_parser import ResumeParser
from src.components.skill_extraction import SkillExtractor
from src.components.resume_scorer import ResumeScorer
from src.components.job_matcher import JobMatcher
from src.components.skill_suggester import SkillSuggester

app = Flask(__name__)

# -------------------------------
# ✅ UPLOAD FOLDER FIX
# -------------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)   # 🔥 IMPORTANT
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------------------------------
# ✅ DATABASE CONFIG
# -------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)

# -------------------------------
# ✅ MODELS (MUST COME BEFORE create_all)
# -------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    score = db.Column(db.Float)
    skills = db.Column(db.String(500))


# -------------------------------
# ✅ CREATE TABLES (AFTER MODELS)
# -------------------------------
with app.app_context():
    db.create_all()

# -------------------------------
# ROUTES
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    file = request.files["resume"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    parser = ResumeParser()
    resume_text = parser.extract_text(filepath)

    extractor = SkillExtractor()
    skills = extractor.extract_skills(resume_text)

    scorer = ResumeScorer()
    score, matched_skills = scorer.calculate_score(skills)

    matcher = JobMatcher()
    ranked_jobs = matcher.match_jobs(resume_text)

    suggester = SkillSuggester()
    skill_suggestions = suggester.suggest_skills(skills)

    resume_record = Resume(
        filename=file.filename,
        score=score,
        skills=",".join(skills)
    )

    db.session.add(resume_record)
    db.session.commit()

    return render_template(
        "dashboard.html",
        score=score,
        skills=skills,
        jobs=ranked_jobs[:3],
        suggestions=skill_suggestions
    )


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    user = User(username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return "User registered successfully"


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        return "Login Successful"

    return "Invalid Credentials"


if __name__ == "__main__":
    app.run()