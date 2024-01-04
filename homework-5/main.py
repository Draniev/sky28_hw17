import json

import psycopg2

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    print(params)
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, suppliers)
                print("FOREIGN KEY успешно добавлены")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'CREATE DATABASE {db_name};')
    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    with open(script_file, 'r') as script:
        sql_query = script.read()
    cur.execute(sql_query)


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    cur.execute('CREATE TABLE suppliers ('
                'supplier_id SERIAL PRIMARY KEY,'
                'company_name VARCHAR(255) NOT NULL,'
                'contact VARCHAR(255),'
                'address VARCHAR(255),'
                'phone VARCHAR(255),'
                'fax VARCHAR(255),'
                'homepage VARCHAR(255)'
                ');')


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""

    with open(json_file, 'r') as json_data:
        data = json.load(json_data)

    # Проверяем наличие апострофов в данных и заменяем на экранированные
    for item in data:
        for key, value in item.items():
            if "\'" in value:
                item[key] = value.replace("\'", "\'\'")
    return data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""

    for item in suppliers:
        cur.execute(f"INSERT INTO suppliers "
                    f"(company_name, contact, address, phone, fax, homepage) "
                    f"VALUES ("
                    f"\'{item["company_name"]}\',"
                    f"\'{item["contact"]}\',"
                    f"\'{item["address"]}\',"
                    f"\'{item["phone"]}\',"
                    f"\'{item["fax"]}\',"
                    f"\'{item["homepage"]}\'"
                    ");")


def add_foreign_keys(cur, suppliers: list[dict]) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""

    cur.execute('ALTER TABLE products '
                'ADD COLUMN supplier_id INT;')

    for item in suppliers:
        cur.execute(f"SELECT supplier_id FROM suppliers "
                    f"WHERE company_name = \'{item['company_name']}\';")
        supp_id = cur.fetchone()
        for product in item['products']:
            if "\'" in product:
                product = product.replace("\'", "\'\'")
            cur.execute(f'UPDATE products SET supplier_id = {supp_id[0]} '
                        f'WHERE product_name = \'{product}\'')


if __name__ == '__main__':
    main()
