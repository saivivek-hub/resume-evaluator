import streamlit as st
import sqlite3
import pandas as pd
from pypdf import PdfReader

from evaluator import evaluate_with_llm
from database import init_db, insert_application, get_all_applications, save_job, get_job

# ---------------- INIT ----------------
init_db()

st.set_page_config(page_title="ATS System", layout="wide")
st.title("AI-Powered ATS System")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

page = st.sidebar.selectbox("Navigation", ["User", "Admin"])


# ---------------- DUPLICATE CHECK ----------------
def is_duplicate(email):
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()
    c.execute("SELECT email FROM applications WHERE email=?", (email,))
    exists = c.fetchone()
    conn.close()
    return exists is not None


# ---------------- USER PAGE ----------------
if page == "User":

    st.header("Candidate Application Form")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner("Parsing resume..."):
            parsed = parse_resume(uploaded_file)

        st.success("Resume parsed successfully")

        name = st.text_input(
            "Name",
            value=parsed.get("name", "")
        )

        email = st.text_input(
            "Email",
            value=parsed.get("email", "")
        )

        skills = st.text_area(
            "Skills",
            value=parsed.get("skills", "")
        )

        experience = st.slider(
            "Experience (years)",
            0,
            10,
            1
        )

        education = st.text_input("Education")

        project = st.text_area("Project Description")

        if st.button("Submit Application"):

            result = insert_application(
                name,
                email,
                skills,
                experience,
                education,
                project,
                parsed.get("resume_text", "")
            )

            if result is True:
                st.success("Application submitted successfully")
            else:
                st.error(result)

# ---------------- ADMIN PAGE ----------------
elif page == "Admin":

    st.header("Admin Panel")

    # LOGIN
    if not st.session_state.admin_logged_in:

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "1234":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:

        st.success("Logged in as admin")

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        job_desc = get_job()
        jd = st.text_area("Job Description", value=job_desc if job_desc else "")

        if st.button("Save Job"):
            save_job(jd)
            st.success("Job saved successfully")
            st.rerun()

        if st.button("Refresh Data"):
            st.rerun()

        data = get_all_applications()

        if data and jd:

            results = []

            for row in data:

                candidate = {
                    "name": row[1],
                    "email": row[2],
                    "skills": row[3],
                    "experience": row[4],
                    "education": row[5],
                    "project": row[6],
                    "resume": row[7]
                }

                result = evaluate_with_llm(candidate, jd)

                results.append({
                    "Name": candidate["name"],
                    "Email": candidate["email"],
                    "Score": result.get("score", 0),
                    "Recommendation": result.get("recommendation", "N/A"),
                    "Explanation": result.get("explanation", "N/A"),
                    "Missing Skills": ", ".join(result.get("missing_skills", []))
                })

            # TABLE 
            st.subheader("Ranked Candidates Summary")

            df = pd.DataFrame(results)
            df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
            df.insert(0, "Rank", df.index + 1)

            st.dataframe(df, use_container_width=True)

            #  SUMMARY 
            st.subheader("Final Result Summary")

            st.write(f"Total Candidates: {len(df)}")
            st.write(f"Strong Hire: {len(df[df['Recommendation'] == 'Strong Hire'])}")
            st.write(f"Shortlisted: {len(df[df['Recommendation'] == 'Shortlisted'])}")
            st.write(f"Needs Review: {len(df[df['Recommendation'] == 'Needs Review'])}")
            st.write(f"Not Shortlisted: {len(df[df['Recommendation'] == 'Not Shortlisted'])}")

            #  BEST CANDIDATE 
            st.subheader("Best Candidate")

            top = df.iloc[0]

            st.write(f"Name: {top['Name']}")
            st.write(f"Score: {top['Score']}")
            st.write(f"Recommendation: {top['Recommendation']}")
            st.write(f"Explanation: {top['Explanation']}")

        else:
            st.info("No data available")
