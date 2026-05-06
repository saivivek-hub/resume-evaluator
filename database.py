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
            project TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_application(name, email, skills, experience, education, project):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO applications (name, email, skills, experience, education, project)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, skills, experience, education, project))

    conn.commit()
    conn.close()


def get_all_applications():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM applications")
    data = c.fetchall()

    conn.close()
    return data


def save_job(job_desc):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS job (id INTEGER PRIMARY KEY, description TEXT)")
    c.execute("DELETE FROM job")
    c.execute("INSERT INTO job (id, description) VALUES (1, ?)", (job_desc,))

    conn.commit()
    conn.close()


def get_job():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT description FROM job WHERE id=1")
    row = c.fetchone()

    conn.close()

    return row[0] if row else ""
