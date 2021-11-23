
import sqlite3

DATABASE_NAME = 'SQL_TCHAI.sqlite'
TABLE_TRANSACTIONS_NAME = 'tblTransactions'


def execute_request_to_database(sqlite_request):
    request_is_successful = False
    try:
        sqlite_connection = sqlite3.connect(DATABASE_NAME)
        # This enables column access by name: row['column_name']
        sqlite_connection.row_factory = sqlite3.Row
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")


        cursor.execute(sqlite_request)
        request_response = cursor.fetchall()
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
        return request_is_successful, request_response


def insert_transaction_into_table(sender, receiver, time_transaction, money):
    sqlite_insert_request = f"INSERT INTO {TABLE_TRANSACTIONS_NAME} (sender, receiver, time_transaction, money) " \
                            f"VALUES ('{sender}', '{receiver}', '{time_transaction}', {money});"
    print(sqlite_insert_request)
    return execute_request_to_database(sqlite_insert_request)


def get_transactions():
    sqlite_get_request = f'SELECT * FROM {TABLE_TRANSACTIONS_NAME}'
    return execute_request_to_database(sqlite_get_request)





