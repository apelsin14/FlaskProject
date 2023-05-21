import sqlite3


sql_query = """SELECT sg.group_id,
    COUNT(DISTINCT s.student_id) AS total_students,
    AVG(ag.grade) AS avg_grade,
    COUNT(DISTINCT ag.grade) AS num_ungraded,
    COUNT(DISTINCT ag.date > a.due_date) AS num_overdue,
    COUNT(DISTINCT CASE WHEN ag.grade IS NULL AND ag.grade > 1 THEN s.student_id END) AS num_retries
FROM students_groups sg
JOIN students s ON s.group_id = sg.group_id
LEFT JOIN assignments a ON a.group_id = sg.group_id
LEFT JOIN assignments_grades ag ON ag.assisgnment_id = a.assisgnment_id AND ag.student_id = s.student_id
GROUP BY sg.group_id;
"""


with sqlite3.connect('homework.sqlite') as conn:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    print("Общее количество учеников\tСредняя оценка\tКол-во учеников которые не сдали работы\t"
          "Кол-во учеников с просроченными работами\tКол-во повторных сдач")
    for item in result:
        print(f"Статистика для {item[0]} группы:\nОбщее количество учеников: {item[1]}\nСредняя оценка: {item[2]}\n"
              f"Кол-во учеников которые не сдали работы: {item[3]}\nКол-во учеников с просроченными работами: {item[4]}\n"
              f"Кол-во повторных сдач: {item[5]}\n")