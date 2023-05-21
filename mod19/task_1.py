import sqlite3


sql_query = """
SELECT teachers.full_name, round(AVG(assignments_grades.grade)) as avg_grade
FROM teachers
JOIN assignments ON assignments.teacher_id = teachers.teacher_id
JOIN assignments_grades ON assignments_grades.assisgnment_id = assignments.assisgnment_id
GROUP BY teachers.teacher_id
ORDER BY avg_grade ASC
LIMIT 1;
"""


with sqlite3.connect('homework.sqlite') as conn:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchone()
    print(f"Преподователь \"{result[0]}\" задает самые сложные задания. Средняя оценка равна {result[1]}")