import sqlite3

DB_NAME = "applications.db"


# INITIALIZE DATABASE
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Applications table
    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            skills TEXT,
            experience INTEGER,
            education TEXT,
            project TEXT,
            score INTEGER,
            recommendation TEXT
        )
    """)

    # Job description table
    c.execute("""
        CREATE TABLE IF NOT EXISTS job (
            id INTEGER PRIMARY KEY,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


# SAVE APPLICATION
def insert_application(app, score, recommendation):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO applications (
            name, email, skills, experience,
            education, project, score, recommendation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        app["name"],
        app["email"],
        app["skills"],
        app["experience"],
        app["education"],
        app["project"],
        score,
        recommendation
    ))

    conn.commit()
    conn.close()


# GET ALL APPLICATIONS
def get_all_applications():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM applications")
    data = c.fetchall()

    conn.close()
    return data

# SAVE JOB DESCRIPTION
def save_job(description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Ensure table exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS job (
            id INTEGER PRIMARY KEY,
            description TEXT
        )
    """)

    # Replace old job
    c.execute("DELETE FROM job")
    c.execute("INSERT INTO job (id, description) VALUES (1, ?)", (description,))

    conn.commit()
    conn.close()



# GET JOB DESCRIPTION
def get_job():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT description FROM job WHERE id = 1")
    row = c.fetchone()

    conn.close()

    return row[0] if row else None