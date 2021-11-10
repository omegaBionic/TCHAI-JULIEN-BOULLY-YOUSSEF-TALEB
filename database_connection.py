
import sqlite3

DATABASE_NAME = 'SQL_TCHAI.sqlite'
TABLE_TRANSACTIONS_NAME = 'tblTransactions'


def insert_variable_into_table(sender, receiver, time_transaction, money):
    try:
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = f"""INSERT INTO {TABLE_TRANSACTIONS_NAME}
                          (sender, receiver, time_transaction, money) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (sender, receiver, time_transaction, money)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print(f"Python Variables inserted successfully into {TABLE_TRANSACTIONS_NAME} table")
        print(f"Python Variables inserted successfully into {TABLE_TRANSACTIONS_NAME} table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
