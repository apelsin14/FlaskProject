import sqlite3


def log_bird(cursor: sqlite3.Cursor, bird_name: str, date_time: str) -> None:
    query = """
        INSERT INTO table_birds (bird_name, date_time)
        VALUES (?, ?);
    """
    cursor.execute(query, (bird_name, date_time))
    cursor.connection.commit()


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor,
                                    bird_name: str) -> bool:
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM table_birds
            WHERE bird_name = ?
            LIMIT 1
        );
    """
    cursor.execute(query, (bird_name,))
    result = cursor.fetchone()[0]
    return bool(result)
