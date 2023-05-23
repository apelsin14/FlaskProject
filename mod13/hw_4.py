import sqlite3


def ivan_sovin_the_most_effective(cursor: sqlite3.Cursor, name: str) -> None:
    query = """
        SELECT salary
        FROM table_effective_manager
        WHERE name = 'Иван Совин';
    """
    cursor.execute(query)
    ivan_salary = cursor.fetchone()[0]

    query = """
        SELECT salary
        FROM table_effective_manager
        WHERE name = ?;
    """
    cursor.execute(query, (name,))
    employee_salary = cursor.fetchone()[0]

    if employee_salary > ivan_salary:
        query = """
            DELETE FROM table_effective_manager
            WHERE name = ?;
        """
        cursor.execute(query, (name,))
    else:
        increased_salary = employee_salary * 1.1
        query = """
            UPDATE table_effective_manager
            SET salary = ?
            WHERE name = ?;
        """
        cursor.execute(query, (increased_salary, name))

    cursor.connection.commit()
