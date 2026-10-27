import sqlite3

DB_NAME = "skill_assessment.db"


def insert_job(jd_data):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # -------------------------
    # 1. Job
    # -------------------------

    cursor.execute("""
        INSERT INTO Job
        (company, role, location, description)
        VALUES (?, ?, ?, ?)
    """, (
        jd_data.get("company"),
        jd_data.get("job_title"),

        # Location is not currently present in your JD JSON
        None,

        # Store responsibilities + qualifications as description
        "\n".join(
            jd_data.get("responsibilities", [])
            + jd_data.get("qualifications", [])
            + jd_data.get("preferred_qualifications", [])
        )
    ))

    job_id = cursor.lastrowid

    print("Job inserted:", job_id)

    # -------------------------
    # 2. Required Skills
    # -------------------------

    for skill in jd_data.get("required_skills", []):

        skill_name = skill.get("skill")
        category = skill.get("category")

        if not skill_name:
            continue

        # Add skill to global Skill table
        cursor.execute("""
            INSERT OR IGNORE INTO Skill
            (skill_name, category)
            VALUES (?, ?)
        """, (
            skill_name,
            category
        ))

        # Get skill_id
        cursor.execute("""
            SELECT skill_id
            FROM Skill
            WHERE skill_name = ?
        """, (skill_name,))

        skill_id = cursor.fetchone()[0]

        # Connect Job → Skill
        cursor.execute("""
            INSERT OR IGNORE INTO JobSkill
            (job_id, skill_id, importance)
            VALUES (?, ?, ?)
        """, (
            job_id,
            skill_id,
            "Required"
        ))

    # -------------------------
    # 3. Preferred Skills
    # -------------------------

    for skill in jd_data.get("preferred_skills", []):

        skill_name = skill.get("skill")
        category = skill.get("category")

        if not skill_name:
            continue

        # Add skill to global Skill table
        cursor.execute("""
            INSERT OR IGNORE INTO Skill
            (skill_name, category)
            VALUES (?, ?)
        """, (
            skill_name,
            category
        ))

        # Get skill_id
        cursor.execute("""
            SELECT skill_id
            FROM Skill
            WHERE skill_name = ?
        """, (skill_name,))

        skill_id = cursor.fetchone()[0]

        # Connect Job → Skill
        cursor.execute("""
            INSERT OR IGNORE INTO JobSkill
            (job_id, skill_id, importance)
            VALUES (?, ?, ?)
        """, (
            job_id,
            skill_id,
            "Preferred"
        ))

    conn.commit()
    conn.close()


if __name__ == "__main__":

    jd_data = {
        "job_title": "Applied Scientist",
        "company": "Amazon",

        "required_skills": [
            {
                "skill": "machine learning technologies",
                "category": "Machine Learning",
                "minimum_experience": None
            },
            {
                "skill": "Reinforcement Learning",
                "category": "Machine Learning",
                "minimum_experience": None
            },
            {
                "skill": "Deep Learning",
                "category": "Machine Learning",
                "minimum_experience": None
            },
            {
                "skill": "Computer Vision",
                "category": "Machine Learning",
                "minimum_experience": None
            },
            {
                "skill": "Natural Language Processing (NLP)",
                "category": "Machine Learning",
                "minimum_experience": None
            }
        ],

        "preferred_skills": [
            {
                "skill": "AI/ML technologies",
                "category": "Machine Learning",
                "minimum_experience": None
            },
            {
                "skill": "Knowledge of large scale distributed systems (e.g., Spark, Hadoop)",
                "category": "System Architecture",
                "minimum_experience": None
            },
            {
                "skill": "Publications in top-tier conferences or journals in AI/ML",
                "category": "Research",
                "minimum_experience": None
            }
        ],

        "responsibilities": [
            "Help build industry-leading Speech and Language technology",
            "Push the envelope in ASR, NLU, ML and Computer Vision",
            "Develop novel algorithms and modeling techniques"
        ],

        "qualifications": [
            "Experience with machine learning technologies, Reinforcement Learning, Deep Learning, Computer Vision or NLP",
            "Experience programming with at least one software programming language"
        ],

        "preferred_qualifications": [
            "Experience with AI/ML technologies",
            "Knowledge of large scale distributed systems"
        ]
    }

    insert_job(jd_data)
    