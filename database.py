import sqlite3

DB_NAME = "skill_assessment.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Candidate
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Candidate (
            candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            linkedin TEXT,
            github TEXT,
            location TEXT
        )
    """)

    # 2. Education
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Education (
            education_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            degree TEXT,
            institution TEXT,
            field_of_study TEXT,
            start_date TEXT,
            end_date TEXT,
            cgpa REAL,

            FOREIGN KEY (candidate_id)
                REFERENCES Candidate(candidate_id)
        )
    """)

    # 3. Experience
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Experience (
            experience_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            company TEXT,
            role TEXT,
            start_date TEXT,
            end_date TEXT,
            description TEXT,

            FOREIGN KEY (candidate_id)
                REFERENCES Candidate(candidate_id)
        )
    """)

    # 4. Project
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            project_name TEXT,
            description TEXT,

            FOREIGN KEY (candidate_id)
                REFERENCES Candidate(candidate_id)
        )
    """)

    # 5. Skill
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Skill (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT UNIQUE NOT NULL,
            category TEXT
        )
    """)

    # 6. CandidateSkill
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CandidateSkill (
            candidate_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,

            PRIMARY KEY (candidate_id, skill_id),

            FOREIGN KEY (candidate_id)
                REFERENCES Candidate(candidate_id),

            FOREIGN KEY (skill_id)
                REFERENCES Skill(skill_id)
        )
    """)

    # 7. Job
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Job (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            location TEXT,
            description TEXT
        )
    """)

    # 8. JobSkill
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS JobSkill (
            job_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            importance TEXT,

            PRIMARY KEY (job_id, skill_id),

            FOREIGN KEY (job_id)
                REFERENCES Job(job_id),

            FOREIGN KEY (skill_id)
                REFERENCES Skill(skill_id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")