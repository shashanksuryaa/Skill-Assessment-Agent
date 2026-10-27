import sqlite3

DB_NAME = "skill_assessment.db"


def insert_resume(resume_data):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # -------------------------
    # Candidate
    # -------------------------

    candidate = resume_data["candidate"]

    cursor.execute("""
        INSERT INTO Candidate
        (name, email, phone, linkedin, github, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        candidate.get("name"),
        candidate.get("email"),
        candidate.get("phone"),
        candidate.get("linkedin"),
        candidate.get("github"),
        candidate.get("location")
    ))

    candidate_id = cursor.lastrowid

    print("Candidate inserted:", candidate_id)

    # -------------------------
    # Education
    # -------------------------

    for education in resume_data.get("education", []):

        cursor.execute("""
            INSERT INTO Education
            (candidate_id, degree, institution, field_of_study,
             start_date, end_date, cgpa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate_id,
            education.get("degree"),
            education.get("institution"),
            education.get("field_of_study"),
            education.get("start_date"),
            education.get("end_date"),
            education.get("cgpa")
        ))

    # -------------------------
    # Experience
    # -------------------------

    for experience in resume_data.get("experience", []):

        cursor.execute("""
            INSERT INTO Experience
            (candidate_id, company, role, start_date,
             end_date, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            candidate_id,
            experience.get("company"),
            experience.get("role"),
            experience.get("start_date"),
            experience.get("end_date"),
            experience.get("description")
        ))

    # -------------------------
    # Projects
    # -------------------------

    for project in resume_data.get("projects", []):

        cursor.execute("""
            INSERT INTO Project
            (candidate_id, project_name, description)
            VALUES (?, ?, ?)
        """, (
            candidate_id,
            project.get("project_name"),
            project.get("description")
        ))

    # -------------------------
    # Skills
    # -------------------------

    for skill in resume_data.get("skills", []):

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

        # Find its ID
        cursor.execute("""
            SELECT skill_id
            FROM Skill
            WHERE skill_name = ?
        """, (skill_name,))

        skill_id = cursor.fetchone()[0]

        # Connect candidate to skill
        cursor.execute("""
            INSERT OR IGNORE INTO CandidateSkill
            (candidate_id, skill_id)
            VALUES (?, ?)
        """, (
            candidate_id,
            skill_id
        ))

    conn.commit()
    conn.close()



if __name__ == "__main__":

    resume_data = {
        "candidate": {
            "name": "Rahul Sharma",
            "email": "rahul.sharma@email.com",
            "phone": "+91 98765 43210",
            "linkedin": "linkedin.com/in/rahulsharma",
            "github": None,
            "location": None
        },

        "education": [
            {
                "degree": "B.Tech",
                "institution": "ABC Institute of Technology",
                "field_of_study": "Computer Science",
                "start_date": "2022",
                "end_date": "2026",
                "cgpa": 8.2
            }
        ],

        "experience": [
            {
                "company": "DataTech Solutions",
                "role": "Data Science Intern",
                "start_date": "Jan 2026",
                "end_date": "Jun 2026",
                "description": "Analyzed customer data using Python and SQL and built machine learning models for customer churn prediction."
            }
        ],

        "projects": [
            {
                "project_name": "Customer Churn Prediction",
                "description": "Built a classification model using Python and Scikit-learn to predict customer churn."
            }
        ],

        "skills": [
            {
                "skill": "Python",
                "category": "Programming"
            },
            {
                "skill": "SQL",
                "category": "Database"
            },
            {
                "skill": "Machine Learning",
                "category": "ML"
            },
            {
                "skill": "Scikit-learn",
                "category": "ML"
            }
        ]
    }

    insert_resume(resume_data)