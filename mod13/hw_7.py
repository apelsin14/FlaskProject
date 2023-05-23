import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username: str = "'; DROP TABLE table_users; --"
    password: str = "'; INSERT INTO table_users (username, password) VALUES ('hacker', 'hacked'); --"
    register(username, password)
