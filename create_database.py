import datetime
import sqlite3
from pathlib import Path
from sqlite3 import Error

import database_requests
import utils.config as Config

config = Config.Config()
database_name = config.config_data["database_config"]["database_name"]

# Create database
try:
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE tblTransactions ( id INTEGER PRIMARY KEY AUTOINCREMENT, sender VARCHAR(30) NOT NULL, receiver VARCHAR(30) NOT NULL, time_transaction VARCHAR(20) NOT NULL, money REAL NOT NULL);
              ''')
    conn.commit()
except Error as e:
    print(e)
finally:
    if conn:
        conn.close()
    print("BDD created.")

# Insert data into database
try:
    absolute_path = Path(database_name).resolve()
except FileNotFoundError:
    print("BDD FileNotFoundError exception.")
else:
    DatabaseRequests.DatabaseRequests.insert_transaction_into_table("boule", "yous",
                                                                    datetime.datetime.now().strftime(
                                                                        "2021-12-08 01:20:10"),
                                                                    100.00)
    DatabaseRequests.DatabaseRequests.insert_transaction_into_table("yous", "boule",
                                                                    datetime.datetime.now().strftime(
                                                                        "2021-12-08 02:23:22"),
                                                                    100.00)
    print("Data's added into database.")
