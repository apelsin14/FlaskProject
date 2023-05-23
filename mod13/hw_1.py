import sqlite3


def check_if_vaccine_has_spoiled(cursor: sqlite3.Cursor, truck_number: str) -> bool:
    query = """
        SELECT CASE 
            WHEN COUNT(*) > 0 THEN 1
            ELSE 0
        END AS has_spoiled_vaccine
        FROM (
            SELECT timestamp, 
                CASE 
                    WHEN temperature_in_celsius < -20 OR temperature_in_celsius > -16 THEN 1
                    ELSE 0
                END AS is_temperature_violated
            FROM table_truck_with_vaccine
            WHERE truck_number = ? AND timestamp >= datetime('now', '-3 hours')
        )
        WHERE is_temperature_violated = 1;
    """
    cursor.execute(query, (truck_number,))
    result = cursor.fetchone()[0]
    return bool(result)
