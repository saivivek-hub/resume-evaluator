import sqlite3

DB_NAME = "applications.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            skills TEXT,
            experience INTEGER,
            education TEXT,
            project TEXT,
            resume TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS job (
            id INTEGER PRIMARY KEY,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_application(name, email, skills, experience, education, project, resume):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        name = str(name or "").strip()
        email = str(email or "").strip()
        skills = str(skills or "").strip()
        education = str(education or "").strip()
        project = str(project or "").strip()
        resume = str(resume or "").strip()

        try:
            experience = int(experience)
        except:
            experience = 0

        if not name or not email:
            raise ValueError("Name and email are required")

        c.execute("""
            INSERT INTO applications 
            (name, email, skills, experience, education, project, resume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, skills, experience, education, project, resume))

        conn.commit()
        return True

    except Exception as e:
        return str(e)

    finally:
        conn.close()


def get_all_applications():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM applications")
    data = c.fetchall()

    conn.close()
    return data


def save_job(job_description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM job")

    c.execute("""
        INSERT INTO job (id, description)
        VALUES (1, ?)
    """, (job_description,))

    conn.commit()
    conn.close()


def get_job():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT description FROM job WHERE id = 1")
    row = c.fetchone()

    conn.close()

    return row[0] if row else ""
