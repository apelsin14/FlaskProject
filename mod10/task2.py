import sqlite3

if __name__ == '__main__':
    with sqlite3.connect('hw_2_database.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM table_checkout ORDER BY sold_count DESC").fetchone()[0]
        print(f"Телефоны цвета {result} покупают чаще всего")

        result = cursor.execute("SELECT * FROM table_checkout WHERE phone_color IN ('Red','Blue') ORDER BY sold_count DESC").fetchall()
        if result[0][1] == result[1][1]:
            print("Телефонов красного и синего цвета покупают одинаково")
        else: print(f"Чаще покупают телефоны цвета - {result[0][0]}")

        result = cursor.execute("SELECT * FROM table_checkout ORDER BY sold_count").fetchone()[0]
        print(f"Телефоны цвета {result} покупают реже всего")