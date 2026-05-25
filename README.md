# AI Internship Resume Analyzer

A beginner-friendly Flask web app that helps users track internship applications and analyze resumes against job descriptions using AI.

## Project Description

AI Internship Resume Analyzer is a simple full-stack web application built with Flask, SQLite, HTML, and the OpenAI API.

The app allows users to:

- Track internship/job applications
- Save job descriptions
- Save resume text
- Compare a selected resume against a selected job description
- Generate an AI analysis with a match score, strongest matches, missing skills, and improved resume bullet suggestions

This project was created as a starter AI web application to practice backend development, database usage, CRUD operations, and AI API integration.

## Features

### Application Tracker

Users can:

- Add a new application
- View saved applications
- Edit existing applications
- Delete applications
- Track company, role, status, deadline, and notes

### Job Description Storage

Users can:

- Add job descriptions
- View saved job descriptions
- Store company name, job title, and full job description text

### Resume Storage

Users can:

- Add resume text
- View saved resumes
- Store multiple resume versions

### AI Resume Analysis

Users can select one saved resume and one saved job description. The app sends both to the AI model and returns:

1. A match score out of 100
2. The 3 strongest matches between the resume and job
3. 5 missing keywords or skills
4. 3 improved resume bullet suggestions
5. A short final summary

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- OpenAI API

## Project Structure

```text
ai-internship-resume-analyzer/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── templates/
    ├── analyze.html
    ├── applications.html
    ├── edit_application.html
    ├── home.html
    ├── jobs.html
    ├── new_application.html
    ├── new_job.html
    ├── new_resume.html
    └── resumes.html
