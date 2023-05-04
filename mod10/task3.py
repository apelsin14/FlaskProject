import sqlite3

if __name__ == '__main__':
    with sqlite3.connect('hw_3_database.db') as conn:
        cursor = conn.cursor()
        result = []
        for i in range(1,4):
            cursor.execute(f"SELECT COUNT(*) FROM table_{i}")
            result.append(cursor.fetchone()[0])
            print(f'Записей в table_{i} - {result[i-1]}')

        result = cursor.execute("SELECT COUNT(DISTINCT value) FROM table_1").fetchone()[0]
        print(f'Уникальных записей в таблице table_1 - {result}')

        result = cursor.execute("SELECT COUNT(*) FROM table_1 WHERE value IN (SELECT value FROM table_2)").fetchone()[0]
        print(f"Записей из таблицы table_1 встречается в table_2 - {result}")

        result = cursor.execute("SELECT COUNT(*) FROM table_1 WHERE value IN (SELECT value FROM table_2)"
                                " AND value IN (SELECT value FROM table_3)").fetchone()[0]
        print(f"Записей из таблицы table_1 встречается и в table_2, и в table_3 - {result}")