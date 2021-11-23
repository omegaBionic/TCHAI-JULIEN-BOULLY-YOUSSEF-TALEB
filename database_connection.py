
import sqlite3

DATABASE_NAME = 'SQL_TCHAI.sqlite'
TABLE_TRANSACTIONS_NAME = 'tblTransactions'


def execute_request_to_database(sqlite_request):
    request_is_successful = False
    try:
        sqlite_connection = sqlite3.connect(DATABASE_NAME)
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        cursor.execute(sqlite_request)

        sqlite_connection.commit()
        print(f"Request is executed")

        cursor.close()
        request_is_successful = True

    except sqlite3.Error as error:
        print("Failed to execute the request", error)
        request_is_successful = False
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("The SQLite connection is closed")
        return request_is_successful


def insert_variable_into_table(sender, receiver, time_transaction, money):
    variable_is_added = False
    try:
        sqlite_connection = sqlite3.connect(DATABASE_NAME)
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = f"""INSERT INTO {TABLE_TRANSACTIONS_NAME}
                          (sender, receiver, time_transaction, money) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (sender, receiver, time_transaction, money)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print(f"Python Variables inserted successfully into {TABLE_TRANSACTIONS_NAME} table")

        cursor.close()
        variable_is_added = True

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        variable_is_added = False
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("The SQLite connection is closed")
        return variable_is_added


