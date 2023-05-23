import sqlite3


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int) -> None:
    commands = []
    for i in range(1, number_of_groups + 1):
        commands.append(
            ('Сильная команда {}'.format(i), 'Страна {}'.format(i), 'Сильная'))
        commands.append(('Средняя команда 1 {}'.format(i),
                         'Страна {}'.format(i), 'Средняя'))
        commands.append(('Средняя команда 2 {}'.format(i),
                         'Страна {}'.format(i), 'Средняя'))
        commands.append(
            ('Слабая команда {}'.format(i), 'Страна {}'.format(i), 'Слабая'))

    cursor.executemany(
        'INSERT INTO uefa_commands (command_name, command_country, command_level) VALUES (?, ?, ?)',
        commands)

    draw_results = []
    for i in range(1, number_of_groups + 1):
        draw_results.append((i, i))

    cursor.executemany(
        'INSERT INTO uefa_draw (command_number, group_number) VALUES (?, ?)',
        draw_results)

    cursor.connection.commit()
