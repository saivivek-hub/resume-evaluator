import sqlite3

DB_NAME = "applications.db"


#  INIT DATABASE 
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Applications table
    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            skills TEXT,
            experience INTEGER,
            education TEXT,
            project TEXT,
            resume TEXT
        )
    """)

    # Job description table (single active job)
    c.execute("""
        CREATE TABLE IF NOT EXISTS job (
            id INTEGER PRIMARY KEY,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


#  INSERT APPLICATION 
def insert_application(name, email, skills, experience, education, project, resume):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO applications 
            (name, email, skills, experience, education, project, resume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, skills, experience, education, project, resume))

        conn.commit()

    except sqlite3.IntegrityError:
        # prevents duplicate email crash
        pass

    conn.close()


#  GET ALL APPLICATIONS 
def get_all_applications():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM applications")
    data = c.fetchall()

    conn.close()
    return data


#  SAVE JOB DESCRIPTION 
def save_job(job_description):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # keep only one active job
    c.execute("DELETE FROM job")

    c.execute("""
        INSERT INTO job (id, description)
        VALUES (1, ?)
    """, (job_description,))

    conn.commit()
    conn.close()


#  GET JOB DESCRIPTION 
def get_job():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT description FROM job WHERE id = 1")
    row = c.fetchone()

    conn.close()

    return row[0] if row else ""
