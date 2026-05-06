import streamlit as st
import pandas as pd

from database import init_db, save_job, get_job, insert_application, get_all_applications
from evaluator import evaluate_with_llm

# 🔧 Init DB
init_db()

# 🎨 Page config
st.set_page_config(page_title="AI Screening System", layout="wide")

# 🏷️ Title
st.title("🤖 AI-Powered Application Screening System")
st.markdown("---")

# 📌 Sidebar navigation
page = st.sidebar.selectbox("Navigation", ["User", "Admin"])

#  USER PAGE 
if page == "User":

    st.header("📄 Apply for Job")

    job_desc = get_job()

    if not job_desc:
        st.warning("⚠️ No job description available. Please check back later.")
    else:
        st.subheader("📌 Job Description")
        st.info(job_desc)

        # 🧾 Form UI
        with st.form("application_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Name")
                email = st.text_input("Email")
                experience = st.slider("Experience (years)", 0, 10)

            with col2:
                education = st.text_input("Education")
                skills = st.text_area("Skills")
                project = st.text_area("Project Description")

            submitted = st.form_submit_button("🚀 Submit Application")

        if submitted:

            candidate = {
                "skills": skills,
                "experience": experience,
                "education": education,
                "project": project
            }

            result = evaluate_with_llm(candidate, job_desc)

            # 🎯 Output
            st.success(f"✅ Score: {result['score']}")
            st.write(f"📌 Recommendation: {result['recommendation']}")
            st.write(f"🧠 Explanation: {result['explanation']}")

            st.write("🔍 Top Factors:")
            for f in result["top_factors"]:
                st.write(f"- {f}")

            # 💾 Save to DB
            insert_application(
                {
                    "name": name,
                    "email": email,
                    "skills": skills,
                    "experience": experience,
                    "education": education,
                    "project": project
                },
                result["score"],
                result["recommendation"]
            )

# ADMIN PAGE
elif page == "Admin":

    st.header("🧑‍💼 Admin Dashboard")

    # 📝 Job description input
    st.subheader("📌 Set Job Description")

    jd = st.text_area("Enter Job Description", value=get_job(), height=200)

    if st.button("💾 Save Job Description"):
        save_job(jd)
        st.success("Job description saved successfully!")

    st.markdown("---")

    # 📊 Applications
    st.subheader("📂 Applications Data")

    data = get_all_applications()

    if data:
        df = pd.DataFrame(data, columns=[
            "ID", "Name", "Email", "Skills", "Experience",
            "Education", "Project", "Score", "Recommendation"
        ])

        # 🏆 Ranking
        df = df.sort_values(by="Score", ascending=False)

        st.write("### 🏆 Ranked Candidates")
        st.dataframe(df, use_container_width=True)

        # 📊 Charts
        st.subheader("📊 Analytics")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Score Distribution")
            st.bar_chart(df["Score"])

        with col2:
            st.write("### Recommendation Breakdown")
            st.bar_chart(df["Recommendation"].value_counts())

        # 📥 CSV download
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="applications.csv",
            mime="text/csv"
        )

    else:
        st.info("No applications submitted yet.")
