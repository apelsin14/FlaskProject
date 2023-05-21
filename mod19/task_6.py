import sqlite3


sql_query = """SELECT round(AVG(grade)) FROM assignments_grades
    WHERE assisgnment_id IN (SELECT assignments.assisgnment_id FROM assignments WHERE assignment_text LIKE '%прочитать%' OR assignment_text LIKE '%выучить%');

"""


with sqlite3.connect('homework.sqlite') as conn:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchone()
    print(f"Средняя оценка за задания, где ученикам нужно было что-то прочитать и выучить равна {result[0]}")