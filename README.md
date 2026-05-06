AI-Powered Application Screening System

An intelligent web-based recruitment automation system that evaluates job applicants using NLP-driven job matching and rule-based AI scoring.
The system helps recruiters automatically shortlist candidates based on their relevance to a job description.

📌 Project Overview

This project automates the initial screening process of job applications by:

Parsing job descriptions
Evaluating candidate profiles
Matching skills and experience using NLP-based token analysis
Generating a suitability score (0–100) with explanations
Ranking candidates for faster decision-making
✨ Features
👤 User Module
Submit application details (name, email, skills, experience, education, project)
View job description
Receive automated evaluation results
🔐 Admin Module
Create and update job descriptions
View all submitted applications
Ranked candidate dashboard
Analytics (score distribution, recommendations)
Download applications as CSV
🧠 AI / NLP Evaluation Logic

The system uses a hybrid approach:

🔹 NLP Processing
Tokenization of job descriptions
Keyword extraction
Matching job tokens with candidate data
🔹 Scoring Mechanism
Job-driven token matching (primary factor)
Skill relevance scoring
Experience-based weighting
Project relevance boost
🔹 Output Format
Score: 0–100
Recommendation: Shortlisted / Needs Review / Not Shortlisted
Explanation: AI reasoning summary
Top Factors: Key matching indicators
🏗️ Tech Stack
Python
Streamlit (Web UI)
SQLite (Database)
Pandas (Data handling)
Custom NLP logic (token-based processing)
📁 Project Structure
Application Screening/
│
├── app.py                # Streamlit UI (User + Admin)
├── evaluator.py          # NLP-based scoring engine
├── database.py           # SQLite database operations
├── applications.db       # Database file (auto-created)
└── README.md             # Project documentation
🚀 How to Run the Project
1️⃣ Clone the repository
git clone https://github.com/your-username/application-screening.git
cd application-screening
2️⃣ Install dependencies
python -m pip install streamlit pandas
3️⃣ Run the application
streamlit run app.py
🔐 Admin Access
Go to Admin panel
Set job description
View ranked candidates and analytics
📊 Output Example
Score: 82
Recommendation: Shortlisted
Explanation: Score based on token match and job relevance
Top Factors:
- python match
- nlp match
- moderate experience
🎯 Key Highlights
Job-description-driven evaluation system
Lightweight NLP (no heavy ML dependencies)
Real-time candidate ranking
Clean admin-user separation
Fully functional recruitment automation workflow
⚠️ Limitations
  Uses rule-based NLP instead of deep learning models
  No authentication layer implemented (scope for extension)
  Does not use semantic embeddings for similarity
🔮 Future Improvements
  Integration with BERT / Sentence Transformers for semantic matching
  Resume parsing from PDF files
  Email notification system for recruiters and candidates
  Role-based authentication (Admin/User security layer)
  Cloud deployment using Streamlit Cloud or AWS

📄 License

This project is open-source and free to use for learning and academic purposes.
