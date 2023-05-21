import sqlite3


sql_query = """SELECT
  students_groups.group_id,
  AVG(CASE WHEN assignments.due_date < ? AND assignments_grades.grade IS NULL THEN 1 ELSE 0 END) AS avg_overdue_assignments,
  MAX(CASE WHEN assignments.due_date < ? AND assignments_grades.grade IS NULL THEN 1 ELSE 0 END) AS max_overdue_assignments,
  MIN(CASE WHEN assignments.due_date < ? AND assignments_grades.grade IS NULL THEN 1 ELSE 0 END) AS min_overdue_assignments
FROM
  students_groups
  JOIN assignments ON students_groups.group_id = assignments.group_id
  LEFT JOIN assignments_grades ON assignments.assisgnment_id = assignments_grades.assisgnment_id
GROUP BY
  students_groups.group_id;
"""


with sqlite3.connect('homework.sqlite') as conn:
    date = "2020-11-25"
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(sql_query, (date, date, date, ))
    result = cursor.fetchall()
    print(f"Среднее, максимальное и минимальное количество просроченных заданий для каждого класса за \'{date}\'")
    for item in result:
        print(f"Для группы {item[0]} среднее = {item[1]}, максимальное = {item[2]}, минимальное = {item[3]}")