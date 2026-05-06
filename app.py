import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from database import (
    init_db, save_job, get_job,
    insert_application, get_all_applications
)

from evaluator import evaluate_with_llm

# Load env
load_dotenv(dotenv_path=".env")

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

init_db()

# Session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.title("AI Application Screening System")

page = st.sidebar.selectbox("Select Page", ["User", "Admin"])

#  USER PAGE 
if page == "User":

    st.header("Apply for Job")

    job_desc = get_job()

    if not job_desc:
        st.warning("No job description available. Contact admin.")
    else:
        st.info(job_desc)

        name = st.text_input("Name")
        email = st.text_input("Email")
        skills = st.text_area("Skills")
        experience = st.slider("Experience", 0, 10)
        education = st.text_input("Education")
        project = st.text_area("Project")

        if st.button("Submit Application"):

            candidate = {
                "name": name,
                "email": email,
                "skills": skills,
                "experience": experience,
                "education": education,
                "project": project
            }

            result = evaluate_with_llm(candidate, job_desc)

            # 🔥 USER ONLY SEE SUMMARY (NO EXPLANATION HERE)
            st.success(f"Score: {result['score']}")
            st.info(f"Recommendation: {result['recommendation']}")

            insert_application(candidate, result["score"], result["recommendation"])

            st.rerun()

# ADMIN PAGE 
elif page == "Admin":

    if not st.session_state.admin_logged_in:

        st.subheader("Admin Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == ADMIN_USER and password == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        st.header("Admin Panel")

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        # Job Description
        st.subheader("Set Job Description")

        jd = st.text_area("Job Description", value=get_job() or "")

        if st.button("Save Job"):
            save_job(jd)
            st.success("Saved")

        # Applications Table
        st.subheader("Applications")

        data = get_all_applications()

        if data:
            df = pd.DataFrame(data, columns=[
                "ID", "Name", "Email", "Skills", "Experience",
                "Education", "Project", "Score", "Recommendation"
            ])

            st.dataframe(df, use_container_width=True)

            # Optional download
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "applications.csv", "text/csv")

        else:
            st.info("No applications yet.")