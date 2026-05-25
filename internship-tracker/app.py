from flask import Flask, render_template, request
import sqlite3
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

def init_db():
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            deadline TEXT,
            notes TEXT
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        title TEXT NOT NULL,
        job_text TEXT NOT NULL
    )
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        resume_text TEXT NOT NULL
    )
""")

    conn.commit()
    conn.close()

def get_words(text):
    words = text.lower().split()
    cleaned_words = []

    for word in words:
        cleaned_word = word.strip(".,!?;:()[]{}\"'")
        if len(cleaned_word) > 2:
            cleaned_words.append(cleaned_word)

    return set(cleaned_words)

@app.route("/")
def home():
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE LOWER(status) = 'applied'")
    applied = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE LOWER(status) = 'interview'")
    interview = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE LOWER(status) = 'rejected'")
    rejected = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE LOWER(status) = 'offer'")
    offer = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "home.html",
        total=total,
        applied=applied,
        interview=interview,
        rejected=rejected,
        offer=offer
    )

@app.route("/applications")
def applications():
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, company, role, status, deadline, notes FROM applications")
    applications_list = cursor.fetchall()

    conn.close()

    return render_template("applications.html", applications=applications_list)

@app.route("/applications/new", methods=["GET", "POST"])
def new_application():
    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        deadline = request.form["deadline"]
        notes = request.form["notes"]

        conn = sqlite3.connect("applications.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO applications (company, role, status, deadline, notes) VALUES (?, ?, ?, ?, ?)",
            (company, role, status, deadline, notes)
        )

        conn.commit()
        conn.close()

        return """
        <h1>Application Saved</h1>
        <p>Your application was saved to the database.</p>
        <a href="/applications">View Applications</a><br>
        <a href="/applications/new">Add Another Application</a><br>
        <a href="/">Back to Home</a>
        """

    return render_template("new_application.html")

@app.route("/applications/delete/<int:app_id>")
def delete_application(app_id):
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))

    conn.commit()
    conn.close()

    return """
    <h1>Application Deleted</h1>
    <p>The application was deleted.</p>
    <a href="/applications">Back to Applications</a><br>
    <a href="/">Back to Home</a>
    """

@app.route("/applications/edit/<int:app_id>", methods=["GET", "POST"])
def edit_application(app_id):
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        deadline = request.form["deadline"]
        notes = request.form["notes"]

        cursor.execute(
            "UPDATE applications SET company = ?, role = ?, status = ?, deadline = ?, notes = ? WHERE id = ?",
            (company, role, status, deadline, notes, app_id)
        )

        conn.commit()
        conn.close()

        return """
        <h1>Application Updated</h1>
        <p>The application was updated.</p>
        <a href="/applications">Back to Applications</a><br>
        <a href="/">Back to Home</a>
        """

    cursor.execute(
        "SELECT id, company, role, status, deadline, notes FROM applications WHERE id = ?",
        (app_id,)
    )
    application = cursor.fetchone()

    conn.close()

    return render_template("edit_application.html", application=application)

@app.route("/jobs")
def jobs():
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, company, title, job_text FROM job_posts")
    jobs_list = cursor.fetchall()

    conn.close()

    return render_template("jobs.html", jobs=jobs_list)


@app.route("/jobs/new", methods=["GET", "POST"])
def new_job():
    if request.method == "POST":
        company = request.form["company"]
        title = request.form["title"]
        job_text = request.form["job_text"]

        conn = sqlite3.connect("applications.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO job_posts (company, title, job_text) VALUES (?, ?, ?)",
            (company, title, job_text)
        )

        conn.commit()
        conn.close()

        return """
        <h1>Job Saved</h1>
        <p>The job description was saved.</p>
        <a href="/jobs">View Jobs</a><br>
        <a href="/jobs/new">Add Another Job</a><br>
        <a href="/">Back to Home</a>
        """

    return render_template("new_job.html")

@app.route("/resumes")
def resumes():
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, resume_text FROM resumes")
    resumes_list = cursor.fetchall()

    conn.close()

    return render_template("resumes.html", resumes=resumes_list)


@app.route("/resumes/new", methods=["GET", "POST"])
def new_resume():
    if request.method == "POST":
        name = request.form["name"]
        resume_text = request.form["resume_text"]

        conn = sqlite3.connect("applications.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO resumes (name, resume_text) VALUES (?, ?)",
            (name, resume_text)
        )

        conn.commit()
        conn.close()

        return """
        <h1>Resume Saved</h1>
        <p>The resume text was saved.</p>
        <a href="/resumes">View Resumes</a><br>
        <a href="/resumes/new">Add Another Resume</a><br>
        <a href="/">Back to Home</a>
        """

    return render_template("new_resume.html")

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM resumes")
    resumes_list = cursor.fetchall()

    cursor.execute("SELECT id, company, title FROM job_posts")
    jobs_list = cursor.fetchall()

    result = None

    if request.method == "POST":
        resume_id = request.form["resume_id"]
        job_id = request.form["job_id"]

        cursor.execute("SELECT name, resume_text FROM resumes WHERE id = ?", (resume_id,))
        resume = cursor.fetchone()

        cursor.execute("SELECT company, title, job_text FROM job_posts WHERE id = ?", (job_id,))
        job = cursor.fetchone()

        prompt = f"""
You are helping analyze a resume against a job description.

Resume name: {resume[0]}

Resume text:
{resume[1]}

Job company: {job[0]}
Job title: {job[1]}

Job description:
{job[2]}

Please give:
1. A match score out of 100
2. 3 strongest matches between the resume and the job
3. 5 important missing keywords or skills
4. 3 improved resume bullet suggestions tailored to this job
5. A short final summary

Keep the response clear and easy to read.
"""

        response = client.responses.create(
            model="gpt-5.5",
            input=prompt
        )

        result = {
            "resume_name": resume[0],
            "job_company": job[0],
            "job_title": job[1],
            "ai_text": response.output_text
        }

    conn.close()

    return render_template(
        "analyze.html",
        resumes=resumes_list,
        jobs=jobs_list,
        result=result
    )

if __name__ == "__main__":
    init_db()
    
    app.run(debug=True)