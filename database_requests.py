import json
import sqlite3

import utils.config as Config
from utils.hash_tchai import HashTchai

config = Config.Config()

print(config.config_data)
DATABASE_NAME = config.config_data["database_config"]["database_name"]
TABLE_TRANSACTIONS_NAME = config.config_data["database_config"]["table_name"]
TABLE_USERS_PUBLIC_KEY_NAME = config.config_data["database_config"]["table_users_public_key_name"]


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
            request_response = ""
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("The SQLite connection is closed")
            return request_is_successful, request_response

    @staticmethod
    def insert_transaction_into_table(sender, receiver, time_transaction, money, signature):
        # Uniformize datas
        sender = sender.lower()
        receiver = receiver.lower()
        money = format(float(money), ".6f")

        # hash
        # Get all transactions
        request_is_successful, request_response = DatabaseRequests.get_transactions()
        transactions = json.loads(json.dumps([dict(ix) for ix in request_response]))
        request_is_successful_count, table_size = DatabaseRequests.size_of_table()
        if int(table_size) == 0:
            transaction_hash = HashTchai.calculate_hash(sender, receiver, time_transaction, money, "", True)
        else:
            transaction_hash = HashTchai.calculate_hash(sender, receiver, time_transaction, money,
                                                        transactions[-1]["hash"], False)

        # Concatenate sql request
        sqlite_insert_request = f"INSERT INTO {TABLE_TRANSACTIONS_NAME} (sender, receiver, time_transaction, money, hash, signature) " \
                                f"VALUES ('{sender}', '{receiver}', '{time_transaction}', {money}, '{transaction_hash}','{signature}');"
        print(sqlite_insert_request)
        return DatabaseRequests.execute_request_to_database(sqlite_insert_request)

    @staticmethod
    def get_transactions():
        sqlite_get_request = f'SELECT * FROM {TABLE_TRANSACTIONS_NAME} ORDER BY time_transaction ASC ;'
        return DatabaseRequests.execute_request_to_database(sqlite_get_request)

    @staticmethod
    def insert_user_to_table_public_key(user):
        user_is_added = False
        private_key = b''
        public_key = b''
        # Verify if user exists in the table first. The response is 0 or 1
        sqlite_get_request_is_user_exist = f"SELECT EXISTS(SELECT 1 FROM {TABLE_USERS_PUBLIC_KEY_NAME} WHERE user='{user}');"
        print("---insert_user_to_table_public_key---")
        print(f'sqlite_get_request for adding user to table of public keys : {sqlite_get_request_is_user_exist}')
        request_is_successful, request_response = DatabaseRequests.execute_request_to_database(sqlite_get_request_is_user_exist)
        print(f'request_is_successful: {request_is_successful}, request_response {request_response}')
        is_user_exists = False
        try:
            sqlite_connection = sqlite3.connect(DATABASE_NAME)
            # This enables column access by name: row['column_name']
            sqlite_connection.row_factory = sqlite3.Row
            cursor = sqlite_connection.cursor()
            print("Connected to SQLite")

            cursor.execute(sqlite_get_request_is_user_exist)
            is_user_exists = True if cursor.fetchone()[0] == 1 else False
            print(f'is_user_exists {is_user_exists}')
            request_is_successful = True
        except sqlite3.Error as error:
            print("Failed to execute the request", error)
            request_is_successful = False
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("The SQLite connection is closed")

        if not request_is_successful:
            # return False, False, 0x0, 0x0
            return request_is_successful, user_is_added, public_key, private_key
        # is_user_exists == True if the user already exists
        if is_user_exists:
            # return True, False, 0x0, 0x0
            return request_is_successful, user_is_added, public_key, private_key
        # If the user doesn't exist
        else:
            public_key_bytes, private_key_bytes = HashTchai.generate_rsa()
            public_key = public_key_bytes
            private_key = private_key_bytes
            sqlite_insert_request = f"INSERT INTO {TABLE_USERS_PUBLIC_KEY_NAME} (user, public_key) " \
                                    f"VALUES ('{user}', '{public_key.decode('utf-8')}'); "
            request_is_successful, request_response = DatabaseRequests.execute_request_to_database(sqlite_insert_request)
            user_is_added = True
            print(f'sqlite_insert_request: {sqlite_insert_request}')
            print(f'user_is_added: true, request_is_successful: {request_is_successful}, request_response {request_response}')
            return request_is_successful, user_is_added, public_key, private_key

    @staticmethod
    def get_user_transactions(username):
        username = username.lower()
        sqlite_get_request = f"SELECT * FROM {TABLE_TRANSACTIONS_NAME} WHERE receiver = '{username}' COLLATE NOCASE " \
                             f"OR sender = '{username}' COLLATE NOCASE ORDER BY time_transaction ASC;"
        return DatabaseRequests.execute_request_to_database(sqlite_get_request)

    @staticmethod
    def get_money_person(username):
        username = username.lower()
        print(f"Get money for: '{username}'")
        sqlite_get_request_received_sum = f"SELECT SUM(money) FROM {TABLE_TRANSACTIONS_NAME} WHERE receiver = " \
                                          f"'{username}' COLLATE NOCASE;"
        sqlite_get_request_sent_sum = f"SELECT SUM(money) FROM {TABLE_TRANSACTIONS_NAME} WHERE sender = " \
                                      f"'{username}' COLLATE NOCASE;"
        request_is_successful = False
        try:
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
            request_is_successful = True
        except sqlite3.Error as error:
            print("Failed to execute the request", error)
            request_is_successful = False
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("The SQLite connection is closed")

        # If None = 0
        if received_sum is None:
            received_sum = 0
        if sent_sum is None:
            sent_sum = 0

        return request_is_successful, received_sum - sent_sum

    @staticmethod
    def size_of_table():
        sqlite_insert_request = f"SELECT count(*) FROM tblTransactions;"
        request_is_successful_count, number_of_lines = DatabaseRequests.execute_request_to_database(
            sqlite_insert_request)
        number_of_lines = json.loads(json.dumps([dict(ix) for ix in number_of_lines]))[0]["count(*)"]
        print("number_of_lines: '{}'".format(number_of_lines))
        return request_is_successful_count, number_of_lines

    @staticmethod
    def get_public_key(user):
        sqlite_get_public_key_request = f"SELECT public_key FROM {TABLE_USERS_PUBLIC_KEY_NAME} " \
                                        f"WHERE user = '{user}' COLLATE NOCASE;"
        request_is_successful = False
        user_public_key = ""
        try:
            sqlite_connection = sqlite3.connect(DATABASE_NAME)
            # This enables column access by name: row['column_name']
            sqlite_connection.row_factory = sqlite3.Row
            cursor = sqlite_connection.cursor()
            print("Connected to SQLite")

            cursor.execute(sqlite_get_public_key_request)
            user_public_key = cursor.fetchone()[0]
            print(f'public_key : {user_public_key}')

            request_is_successful = True
        except sqlite3.Error as error:
            print("Failed to execute the request", error)
            request_is_successful = False
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("The SQLite connection is closed")

        print(f'user_public_key: {user_public_key}')
        return request_is_successful, user_public_key
