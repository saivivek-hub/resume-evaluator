import streamlit as st
import sqlite3
from pypdf import PdfReader

from evaluator import evaluate_with_llm
from database import init_db, insert_application, get_all_applications, save_job, get_job

# ---------------- INIT ----------------
init_db()

st.set_page_config(page_title="AI ATS System", layout="wide")

st.title(" AI-Powered ATS Recruiter Screening System")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

page = st.sidebar.selectbox("Navigation", ["User", "Admin"])


# ================= DUPLICATE CHECK =================
def is_duplicate(email):
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()

    c.execute("SELECT email FROM applications WHERE email=?", (email,))
    exists = c.fetchone()

    conn.close()

    return exists is not None


# ================= USER PAGE =================
if page == "User":

   st.header(" Candidate Application Form")

with st.form("application_form", clear_on_submit=True):

    name = st.text_input("Name")
    email = st.text_input("Email")

    skills = st.text_area("Skills (Paste full content)", height=150)

    experience = st.slider("Experience (years)", 0, 10)

    education = st.text_input("Education")
    project = st.text_area("Project Description")

    st.subheader("📎 Resume Upload (PDF optional)")
    uploaded_file = st.file_uploader("Upload CV", type=["pdf"])

    resume_text = ""

    if uploaded_file is not None:
        try:
            from pypdf import PdfReader

            reader = PdfReader(uploaded_file)

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text

        except Exception as e:
            st.error("PDF reading error: " + str(e))

    submitted = st.form_submit_button("🚀 Submit Application")

    if submitted:

        # ---------------- VALIDATION ----------------
        if not name.strip() or not email.strip():
            st.error("Name and Email are required!")
        elif len(skills.strip()) < 10:
            st.error("Please enter more skill details (too short input)")
        else:
            insert_application(
                name,
                email,
                skills,
                experience,
                education,
                project,
                resume_text
            )

            st.success("Application submitted successfully!")
            st.rerun()

# ================= ADMIN PAGE =================
elif page == "Admin":

    st.header("🧑‍💼 Admin Panel")

    # ---------------- LOGIN ----------------
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

        st.success("Welcome Admin")

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        # ---------------- JOB ----------------
        job_desc = get_job()

        jd = st.text_area("Job Description", value=job_desc if job_desc else "")

        if st.button("Save Job"):
            save_job(jd)
            st.success("Job saved successfully")
            st.rerun()

        st.markdown("---")

        # 🔄 Refresh button
        if st.button("🔄 Refresh Candidates"):
            st.rerun()

        # ================= DATA =================
        data = get_all_applications()

        if data and job_desc:

            # ================= RAW VIEW =================
            st.subheader("📋 All Candidates (Raw Data)")

            for row in data:

                st.markdown("---")
                st.write(" Name:", row[1])
                st.write(" Email:", row[2])
                st.write(" Skills:", row[3])
                st.write(" Experience:", row[4])
                st.write(" Education:", row[5])
                st.write(" Project:", row[6])

            # ================= RANKED VIEW =================
            st.markdown("---")
            st.subheader(" Ranked Candidates (AI Evaluation)")

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

                result = evaluate_with_llm(candidate, job_desc)

                results.append({
                    "Name": candidate["name"],
                    "Email": candidate["email"],
                    "Score": result.get("score", 0),
                    "Recommendation": result.get("recommendation", "N/A"),
                    "Explanation": result.get("explanation", "N/A"),
                    "Missing Skills": ", ".join(result.get("missing_skills", []))
                })

            results = sorted(results, key=lambda x: x["Score"], reverse=True)

            for r in results:

                st.markdown("---")
                st.subheader(f" {r['Name']}")

                st.write(" Email:", r["Email"])
                st.write(" Score:", r["Score"])
                st.write(" Recommendation:", r["Recommendation"])
                st.write(" Explanation:", r["Explanation"])
                st.write(" Missing Skills:", r["Missing Skills"])

        else:
            st.info("No applications or job description found")
