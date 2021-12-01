import sqlite3

DATABASE_NAME = 'SQL_TCHAI.sqlite'
TABLE_TRANSACTIONS_NAME = 'tblTransactions'


class DatabaseRequests:

    @staticmethod
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

    @staticmethod
    def insert_transaction_into_table(sender, receiver, time_transaction, money):
        sqlite_insert_request = f"INSERT INTO {TABLE_TRANSACTIONS_NAME} (sender, receiver, time_transaction, money) " \
                                f"VALUES ('{sender}', '{receiver}', '{time_transaction}', {money});"
        print(sqlite_insert_request)
        return DatabaseRequests.execute_request_to_database(sqlite_insert_request)

    @staticmethod
    def get_transactions():
        sqlite_get_request = f'SELECT * FROM {TABLE_TRANSACTIONS_NAME} ORDER BY time_transaction ASC ;'
        return DatabaseRequests.execute_request_to_database(sqlite_get_request)

    @staticmethod
    def get_user_transactions(username):
        sqlite_get_request = f"SELECT * FROM {TABLE_TRANSACTIONS_NAME} WHERE receiver = '{username}' COLLATE NOCASE " \
                             f"OR sender = '{username}' COLLATE NOCASE ORDER BY time_transaction ASC;"
        return DatabaseRequests.execute_request_to_database(sqlite_get_request)


    # TODO verify if request is unsuccessful
    # TODO verify if user exists
    @staticmethod
    def get_money_person(username):
        sqlite_get_request_received_sum = f"SELECT SUM(money) FROM {TABLE_TRANSACTIONS_NAME} WHERE receiver = " \
                                          f"'{username}' COLLATE NOCASE;"
        sqlite_get_request_sent_sum = f"SELECT SUM(money) FROM {TABLE_TRANSACTIONS_NAME} WHERE sender = " \
                                      f"'{username}' COLLATE NOCASE;"

        sqlite_connection = sqlite3.connect(DATABASE_NAME)
        # This enables column access by name: row['column_name']
        sqlite_connection.row_factory = sqlite3.Row
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        cursor.execute(sqlite_get_request_received_sum)
        received_sum = cursor.fetchone()[0]
        print(f'received_sum {received_sum}')
        cursor.execute(sqlite_get_request_sent_sum)
        sent_sum = cursor.fetchone()[0]
        print(f'sent_sum {sent_sum}')

        #is_successful_request_received_sum, received_sum = DatabaseRequests.execute_request_to_database(sqlite_get_request_received_sum)
        #print(f"RECEIVED SUM: {received_sum.__str__()}")
        #is_successful_request_sent_sum, sent_sum = DatabaseRequests.execute_request_to_database(sqlite_get_request_sent_sum)
        #print(sent_sum)
        #if not is_successful_request_sent_sum or not is_successful_request_received_sum:
        #    not_successful_response = received_sum
        #    return False, not_successful_response

        #print(received_sum.__str__())

        return True, received_sum - sent_sum

