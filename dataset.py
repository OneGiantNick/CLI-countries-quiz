import pandas as pd
import sqlite3
import requests
import io

# Downloading the csv file from github

url = "https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv"
download = requests.get(url).content

# Reading the downloaded content and turning it into a pandas dataframe

df = pd.read_csv(io.StringIO(download.decode("utf-8")))

# Only take independent countries
df = df.loc[(df["is_independent"]) == "Yes"]

df = df[["ISO3166-1-Alpha-3", "official_name_en", "CLDR display name"]]

# Establish connection to sql server
database = "countries.db"
con = sqlite3.connect(database)
cur = con.cursor()

for index, row in df.iterrows():
    sql_insert_country = """
        INSERT OR IGNORE INTO countries(country_name, country_code)
        VALUES (?, ?)
        """
    sql_insert_answer = """
        INSERT OR IGNORE INTO countries_answer(country_code, answer) VALUES (?,?)
        """
    cur.execute(
        sql_insert_country, (row["CLDR display name"].lower(), row["ISO3166-1-Alpha-3"])
    )
    cur.execute(sql_insert_answer, (row["ISO3166-1-Alpha-3"], 0))

con.commit()
con.close()
