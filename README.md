AI-Powered Application Screening System


An intelligent AI-powered recruitment automation platform that streamlines candidate screening using resume parsing, NLP-based skill matching, and automated ranking.


The system helps recruiters efficiently shortlist candidates by analyzing resumes against job descriptions and generating intelligent suitability scores with explanations.


Project Overview


This project automates the initial hiring workflow by:



Parsing resumes from uploaded PDF files

Extracting candidate information automatically

Analyzing job descriptions using NLP

Matching candidate skills with job requirements

Generating AI-based evaluation scores

Ranking candidates automatically

Providing recruiter-friendly analytics dashboards

Features
Candidate Module

Upload resume directly (PDF)

Automatic extraction of:

Name, Email, Skills, Education, Projects
Submit applications without manual data entry

AI-driven profile evaluation

Admin Module

Secure admin login

Create and manage job descriptions

View ranked candidate dashboard

AI-based candidate scoring

Recommendation system

Candidate summary analytics

Best candidate highlighting

AI / NLP Evaluation Logic


The system uses a lightweight AI-inspired NLP evaluation pipeline.


NLP Processing,  Resume text extraction from PDFs, Tokenization and normalization, Technical skill extraction,  Job-description keyword matching, Resume-project-skill aggregation


Intelligent Scoring System

The scoring engine evaluates candidates based on:

Technical Skill Matching

Matches important technical keywords such as:

Python, SQL, Machine Learning, TensorFlow, AWS, NLP, APIs, Pandas, NumPy


Experience Weighting

Experience contributes dynamically to the final score:

Fresher, Junior, Mid-level, Senior

Project Relevance


Projects relevant to the job description receive additional scoring boosts.


Education Relevance


Technical education backgrounds receive bonus weighting.


Output Format

Each candidate receives:


Score (0–100)

Recommendation

Strong Hire

Shortlisted

Needs Review

Not Shortlisted

AI Explanation

Missing Skills Analysis

Tech Stack

Python

Streamlit

SQLite

Pandas

PyPDF

NLP-based token processing

Project Structure

Application-Screening-System/


│

├── app.py                # Main Streamlit application

├── evaluator.py          # AI/NLP scoring engine

├── parser.py             # Resume parser and information extractor

├── database.py           # SQLite database operations

├── applications.db       # Auto-generated SQLite database

├── requirements.txt      # Dependencies

└── README.md             # Project documentation

Installation & Setup
1. Clone Repository


git clone https://github.com/saivivek-hub/application-screening.git


cd application-screening

2. Install Dependencies

pip install -r requirements.txt


Or manually:


pip install streamlit pandas pypdf

3. Run Application

streamlit run app.py

Admin Access

Default Admin Credentials:


Username: admin

Password: 1234

Sample Workflow

Candidate Side

Upload resume PDF

System extracts candidate information

Candidate submits application

Resume gets evaluated automatically

Recruiter Side

Login as admin

Add job description

View ranked candidates

Analyze recommendations

Shortlist top candidates

Example Output
Rank	Candidate	Score	Recommendation

1	Arjun Mehta	91	Strong Hire

2	Rahul Verma	78	Shortlisted

3	Neha Singh	58	Needs Review

4	Sneha Kapoor	26	Not Shortlisted

Key Highlights

Resume-aware ATS system

Automated PDF parsing

Lightweight NLP architecture

AI-style candidate ranking

Real-time recruiter dashboard

Fully local database support

Deployable on Streamlit Cloud

Deployment

You can deploy this project using:

Streamlit Cloud


This project is open-source and available for educational and learning purposes.
