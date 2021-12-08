import sqlite3
from sqlite3 import Error
import utils.config as Config

config = Config.Config()

try:
    conn = sqlite3.connect(config.config_data["database_config"]["database_name"])
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

