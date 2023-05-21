import requests
import sqlite3
import time
import threading

CREATE_TABLE_SQL_QUERY = """
CREATE TABLE IF NOT EXISTS starwars (id INT PRIMARY KEY, name TEXT, age TEXT, gender TEXT)
"""

INSERT_SQL_QUERY = """
INSERT INTO 'starwars' (name, age, gender)
VALUES (?, ?, ?);
"""


def get_data(url: str, result: list) -> None:
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return

    name = data["name"]
    age = data["birth_year"]
    gender = data["gender"]

    result.append((name, age, gender))


def load_data_sequential():
    url = "https://swapi.dev/api/people/"
    with sqlite3.connect("homework.db") as c:
        cursor = c.cursor()

    result = []
    for i in range(1, 21):
        get_data(url + str(i), result)

    cursor.executemany(INSERT_SQL_QUERY, result)
    c.commit()


def load_data_multithreading():
    url = "https://swapi.dev/api/people/"
    with sqlite3.connect("homework.db") as c:
        cursor = c.cursor()

    result = []
    threads = []
    for i in range(1, 21):
        thread = threading.Thread(target=get_data, args=(url + str(i), result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    cursor.executemany(INSERT_SQL_QUERY, result)
    c.commit()


if __name__ == "__main__":
    with sqlite3.connect("homework.db") as conn:
        cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL_QUERY)
    conn.close()

    start_time = time.time()
    load_data_sequential()
    end_time = time.time()
    print(f"Время выполнения последовательной функции {end_time - start_time}")

    start_time = time.time()
    load_data_multithreading()
    end_time = time.time()

    print(f"Время выполнения многопоточной функции {end_time - start_time}")