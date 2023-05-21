import sqlite3


sql_query = """
SELECT students.full_name, round(AVG(assignments_grades.grade)) as avg_grade
FROM students
JOIN assignments_grades ON students.student_id = assignments_grades.student_id
GROUP BY students.student_id
ORDER BY avg_grade DESC
LIMIT 10;
"""


with sqlite3.connect('homework.sqlite') as conn:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    print(f"Топ 10 учеников с лучшим средним баллом:")
    for item in result:
        print(f"\'{item[0]}\' - {item[1]} б.")