import sqlite3


sql_query = """SELECT s.full_name, assignment_text
FROM students s
JOIN assignments_grades ag ON s.student_id = ag.student_id
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
JOIN students_groups sg ON s.group_id = sg.group_id
JOIN teachers t ON sg.teacher_id = t.teacher_id
WHERE t.teacher_id = (
  SELECT a.teacher_id
  FROM assignments a
  GROUP BY a.teacher_id
  ORDER BY AVG((SELECT AVG(grade) FROM assignments_grades WHERE a.assisgnment_id = a.assisgnment_id)) DESC
  LIMIT 1
)
GROUP BY s.student_id
ORDER BY AVG(ag.grade) DESC
LIMIT 10;
"""


with sqlite3.connect('homework.sqlite') as conn:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    print(f"Задания, за которые ученики получают самый высокий средний балл")
    for item in result:
        print(f"\'{item[1]}\'")