# How many countries can you name?
import sqlite3


def menu():
    start = input("Start game? y/n ")
    if start == "y":
        score = game()
    else:
        pass
    print("congrats! you scored {}/195!".format(score))
    return


def game():
    database = "countries.db"
    con = sqlite3.connect(database)
    cur = con.cursor()

    # Sets all previously answered records to 0
    restart_game = """UPDATE countries_answer SET answer = 0"""
    cur.execute(restart_game)
    con.commit()

    count = 0
    while True:
        answer = str(input('Name a Country (type "end" to give up) ')).lower()
        if answer == "end":
            return count
        else:
            sql_statement = (
                """SELECT country_code FROM countries WHERE country_name=?"""
            )
            country_code = con.execute(sql_statement, (answer,)).fetchone()
            if country_code is None:
                print("Wrong answer!")
            else:
                country_code = country_code[0]
                answered = (
                    """SELECT answer FROM countries_answer WHERE country_code=?"""
                )
                answered_or_not = con.execute(answered, (country_code,)).fetchone()[0]
                if answered_or_not == 0:
                    update_answer = (
                        """UPDATE countries_answer SET answer=? WHERE country_code=?"""
                    )
                    con.execute(update_answer, (1, country_code))
                    con.commit()
                    count += 1
                    print("Current Score: {}/195".format(count))
                else:
                    print("Already answered!")


if __name__ == "__main__":
    menu()
