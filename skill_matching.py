import sqlite3

DB_NAME = "skill_assessment.db"


def exact_skill_match(candidate_id, job_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.skill_name,
            js.importance
        FROM CandidateSkill cs
        JOIN Skill s
            ON cs.skill_id = s.skill_id
        JOIN JobSkill js
            ON s.skill_id = js.skill_id
        WHERE cs.candidate_id = ?
        AND js.job_id = ?
    """, (candidate_id, job_id))

    matches = cursor.fetchall()

    conn.close()

    return matches


if __name__ == "__main__":

    candidate_id = 1
    job_id = 1

    matches = exact_skill_match(candidate_id, job_id)

    print("Exact skill matches:")

    for skill, importance in matches:
        print(f"{skill} -> {importance}")