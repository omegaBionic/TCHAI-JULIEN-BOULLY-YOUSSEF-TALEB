import datetime
from pathlib import Path
from sqlite3 import Error

from database_requests import *
import utils.config as Config

config = Config.Config()
database_name = config.config_data["database_config"]["database_name"]
table_name = config.config_data["database_config"]["table_name"]

table_users_public_key_name = config.config_data["database_config"]["table_users_public_key_name"]

# Create database
try:
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute(f'CREATE TABLE {table_name} ( id INTEGER PRIMARY KEY AUTOINCREMENT, sender VARCHAR(30) NOT NULL, '
              f'receiver VARCHAR(30) NOT NULL, time_transaction VARCHAR(20) NOT NULL, money REAL NOT NULL, '
              f'hash VARCHAR(64) NOT NULL, signature VARCHAR(256) NOT NULL);')
    conn.commit()

    c.execute(f'CREATE TABLE {table_users_public_key_name} (id_user INTEGER PRIMARY KEY AUTOINCREMENT, '
              f'user VARCHAR(30) NOT NULL, public_key VARCHAR(256) NOT NULL);')
    conn.commit()
except Error as e:
    print(e)
finally:
    if conn:
        conn.close()
    print("BDD created.")

# # Insert data into database
# try:
#     absolute_path = Path(database_name).resolve()
# except FileNotFoundError:
#     print("BDD FileNotFoundError exception.")
# else:
#     DatabaseRequests.insert_transaction_into_table("boule", "yous",
#                                                    datetime.datetime.now().strftime(
#                                                        "2021-12-08 01:20:10"),
#                                                    100.00)
#     DatabaseRequests.insert_transaction_into_table("yous", "boule",
#                                                    datetime.datetime.now().strftime(
#                                                        "2021-12-08 02:23:22"),
#                                                    100.00)
#     print("Data's added into database.")
