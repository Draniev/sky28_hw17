"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv

import psycopg2

#
# with psycopg2.connect(**conn_params) as conn:
#     with conn.cursor() as cur:
#         cur.execute("INSERT INTO my_table VALUES (%s, %s)", (1, "Test"))
#         cur.execute("SELECT * FROM mytable")
#
#         rows = cur.fetchall()
#         for row in rows:
#             print(row)

# INSERT INTO post VALUES (1, 'Happy New Year', '');
# INSERT INTO post VALUES
# (2, 'My plans for 2023', ''),
# (3, 'Lesson learned from 2022', ''),
# (4, 'NewPost!', '');


def read_csv(filename: str) -> list[dict]:
    try:
        csvfile = open(filename, newline='')
    except Exception:
        raise FileNotFoundError('Проблема с файлом... Не найден?')
    else:
        with csvfile:
            result = []
            reader = csv.DictReader(csvfile)
            for row in reader:
                result.append(row)
        return result


def convert_to_str(data: dict) -> str:
    string = ''
    string += '('
    index = 0
    for val in data.values():
        index += 1
        if type(val) is str:
            val = val.replace("\'", "`")
            string += f'\'{val}\''
        else:
            string += f'{val}'
        if index < len(data):
            string += ', '
    string += ')'
    return string


def add_to_db(conn_params: dict, data: list[dict], tablename: str) -> None:
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            for row in data:
                data_str = convert_to_str(row)
                print(data_str)
                cur.execute(f"INSERT INTO {tablename} VALUES {data_str}")

# INSERT INTO post VALUES
# (2, 'My plans for 2023', ''),
# (3, 'Lesson learned from 2022', ''),
# (4, 'NewPost!', '');


def main() -> None:

    conn_params = {
        'host': "localhost",
        'database': "north",
        'user': "postgres",
        'password': "postgres"
    }

    # customers = read_csv('north_data/customers_data.csv')
    orders = read_csv('north_data/orders_data.csv')
    employees = read_csv('north_data/employees_data.csv')

    # add_to_db(conn_params, customers, 'customers')
    add_to_db(conn_params, employees, 'employees')
    add_to_db(conn_params, orders, 'orders')


if __name__ == "__main__":
    main()
