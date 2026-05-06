import streamlit as st
import pandas as pd

from evaluator import evaluate_with_llm
from database import init_db, insert_application, get_all_applications, save_job, get_job

#  INIT 
init_db()

st.set_page_config(page_title="AI Screening System", layout="wide")

st.title("🤖 AI-Powered Application Screening System")

page = st.sidebar.selectbox("Navigation", ["User", "Admin"])

#  USER PAGE 
if page == "User":

    st.header("📄 Candidate Application Form")

    name = st.text_input("Name")
    email = st.text_input("Email")
    skills = st.text_area("Skills")
    experience = st.slider("Experience (years)", 0, 10)
    education = st.text_input("Education")
    project = st.text_area("Project Description")

    submitted = st.button("🚀 Submit Application")

    if submitted:

        candidate = {
            "name": name,
            "email": email,
            "skills": skills,
            "experience": experience,
            "education": education,
            "project": project
        }

        # ONLY SAVE DATA (NO AI HERE)
        insert_application(candidate)

        st.success("✅ Application submitted successfully!")
        st.info("Your application will be evaluated by admin.")

#  ADMIN PAGE 
elif page == "Admin":

    st.header("🧑‍💼 Admin Dashboard")

    job_desc = get_job()

    #  JOB DESCRIPTION 
    st.subheader("📌 Job Description")

    jd = st.text_area("Set / Edit Job Description", value=job_desc if job_desc else "")

    if st.button("💾 Save Job Description"):
        save_job(jd)
        st.success("Job description saved!")

    st.markdown("---")

    #  APPLICATIONS 
    data = get_all_applications()

    if data and job_desc:

        results = []

        for row in data:

            candidate = {
                "name": row[1],
                "email": row[2],
                "skills": row[3],
                "experience": row[4],
                "education": row[5],
                "project": row[6]
            }

            result = evaluate_with_llm(candidate, job_desc)

            results.append([
                candidate["name"],
                candidate["email"],
                result.get("score", 0),
                result.get("recommendation", "N/A"),
                result.get("explanation", "N/A")
            ])

        df = pd.DataFrame(results, columns=[
            "Name", "Email", "Score", "Recommendation", "Explanation"
        ])

        df = df.sort_values(by="Score", ascending=False)

        st.subheader("🏆 Evaluated Candidates")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Score Distribution")
        st.bar_chart(df["Score"])

        st.subheader("📌 Recommendation Breakdown")
        st.bar_chart(df["Recommendation"].value_counts())

    elif not job_desc:
        st.warning("⚠️ Please set job description first")

    else:
        st.info("No applications submitted yet.")
