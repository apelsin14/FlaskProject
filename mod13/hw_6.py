import sqlite3
from datetime import datetime, timedelta


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    cursor.execute("DELETE FROM table_friendship_schedule")

    training_preferences = {
        "понедельник": "футбол",
        "вторник": "хоккей",
        "среда": "шахматы",
        "четверг": "SUP-сёрфинг",
        "пятница": "бокс",
        "суббота": "Dota2",
        "воскресенье": "шахбокс"
    }

    employees = [
        {"id": 1, "name": "Сотрудник 1", "preference": "шахматы"},
        {"id": 2, "name": "Сотрудник 2", "preference": "бокс"},
    ]

    employee_index = 0

    for day in range(1, 367):
        weekday = get_weekday(day)
        training = training_preferences.get(weekday)

        while training and training == employees[employee_index]["preference"]:
            employee_index = (employee_index + 1) % len(employees)

        employee_id = employees[employee_index]["id"]

        cursor.execute(
            "INSERT INTO table_friendship_schedule (day, employee_id) VALUES (?, ?)",
            (day, employee_id))

        employee_index = (employee_index + 1) % len(employees)


def get_weekday(day: int) -> str:
    start_date = datetime(2023, 1, 1)
    target_date = start_date + timedelta(days=day - 1)
    weekday_num = target_date.weekday()
    weekday_mapping = {
        0: "понедельник",
        1: "вторник",
        2: "среда",
        3: "четверг",
        4: "пятница",
        5: "суббота",
        6: "воскресенье"
    }
    return weekday_mapping[weekday_num]


connection = sqlite3.connect("hw.db")
cursor = connection.cursor()

update_work_schedule(cursor)

connection.commit()

connection.close()
