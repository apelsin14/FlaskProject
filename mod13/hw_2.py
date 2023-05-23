import sqlite3
import csv


def delete_wrong_fees(cursor: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file, 'r') as file:
        csv_reader = csv.reader(file)
        wrong_fees_data = list(csv_reader)

        for row in wrong_fees_data:
            date, car_number = row

            query = """
                DELETE FROM table_fees
                WHERE timestamp = ? AND truck_number = ?;
            """
            cursor.execute(query, (date, car_number))

    cursor.connection.commit()


if __name__ == "__main__":
    with sqlite3.connect("hw.db") as conn:
        cursor = conn.cursor()

        delete_wrong_fees(cursor, "wrong_fees.csv")
