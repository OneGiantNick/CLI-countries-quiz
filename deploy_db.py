# Used to initialise database
import sqlite3
from sqlite3 import Error

database = "countries.db"


def create_connection(db_file):
    con = None
    try:
        con = sqlite3.connect(db_file)
        return con
    except Error as e:
        print(e)

    return con


def create_table(con, create_table_sql):
    try:
        c = con.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    sql_create_countries_table = """
        CREATE TABLE IF NOT EXISTS countries(
            country_name text PRIMARY KEY,
            country_code text NOT NULL
        );
    """

    sql_create_countries_code_table = """
        CREATE TABLE IF NOT EXISTS countries_answer(
            country_code text PRIMARY KEY,
            answer integer NOT NULL,
            FOREIGN KEY (country_code) REFERENCES countries (country_code)
        );
    """

    con = create_connection(database)

    if con is not None:
        create_table(con, sql_create_countries_table)
        create_table(con, sql_create_countries_code_table)

    else:
        print("Error! cannot create the database connection.")

    con.close()


if __name__ == "__main__":
    main()
