import sqlite3

if __name__ == '__main__':
    with sqlite3.connect('hw_4_database.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT COUNT(*) FROM (SELECT salary FROM salaries WHERE salary<5000)").fetchone()[0]
        print(f"Человек с острова N находящихся за чертой бедности - {result}")

        result = cursor.execute("SELECT AVG(salary) FROM salaries").fetchone()[0]
        print(f"Средняя зарплата на острове: {result}")

        array = cursor.execute("SELECT salary FROM salaries ORDER BY salary").fetchall()
        result = array[(len(array)) // 2][0]
        print(f"Медианная зарплата на острове: {result}")

        count = cursor.execute("SELECT COUNT(salary) FROM salaries").fetchone()[0]
        total = cursor.execute("SELECT SUM(salary) FROM salaries").fetchone()[0]
        top10 = cursor.execute(f"SELECT SUM(salary) FROM (SELECT * FROM salaries ORDER BY salary DESC LIMIT 0.1 * {count})").fetchone()[0]
        top90 = total - top10
        F = round(top10/top90 * 100, 2)
        print(f"Социальное неравенство на острове: {F}%")