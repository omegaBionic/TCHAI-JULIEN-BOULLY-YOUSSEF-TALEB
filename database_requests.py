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
    def insert_transaction_into_table(sender, receiver, time_transaction, money):
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
        sqlite_insert_request = f"INSERT INTO {TABLE_TRANSACTIONS_NAME} (sender, receiver, time_transaction, money, hash) " \
                                f"VALUES ('{sender}', '{receiver}', '{time_transaction}', {money}, \"{transaction_hash}\");"
        print(sqlite_insert_request)
        return DatabaseRequests.execute_request_to_database(sqlite_insert_request)

    @staticmethod
    def get_transactions():
        sqlite_get_request = f'SELECT * FROM {TABLE_TRANSACTIONS_NAME} ORDER BY time_transaction ASC ;'
        return DatabaseRequests.execute_request_to_database(sqlite_get_request)

    @staticmethod
    def insert_user_to_table_public_key(user):
        user_is_added = False
        private_key = 0x0
        public_key = 0x0
        # Verify if user exists in the table first. The response is 0 or 1
        sqlite_get_request = f"SELECT EXISTS(SELECT 1 FROM {TABLE_USERS_PUBLIC_KEY_NAME} WHERE user='{user}');"
        request_is_successful, request_response = DatabaseRequests.execute_request_to_database(sqlite_get_request)
        if not request_is_successful:
            # return False, False, 0x0, 0x0
            return request_is_successful, user_is_added, public_key, private_key
        # The response is 1 if the user already exists
        if request_response == 1:
            # return True, False, 0x0, 0x0
            return request_is_successful, user_is_added, public_key, private_key
        # If the use doesn't exist
        else:
            public_key_bytes, private_key_bytes = HashTchai.generate_rsa()
            public_key = public_key_bytes.hex()
            private_key = private_key_bytes.hex()
            sqlite_insert_request = f"INSERT INTO {TABLE_USERS_PUBLIC_KEY_NAME} (user, public_key) " \
                                    f"VALUES ('{user}', '{public_key}'); "

            return DatabaseRequests.execute_request_to_database(sqlite_insert_request), public_key, private_key

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

    # TODO: Remove get_last_transaction()
    # @staticmethod
    # def get_last_transaction():
    #     last_transaction = ""
    #
    #     # Get last element
    #     # Check if table is empty
    #     sqlite_insert_request = f"SELECT count(*) FROM {TABLE_TRANSACTIONS_NAME};"
    #     request_is_successful_count, number_of_lines = DatabaseRequests.execute_request_to_database(
    #         sqlite_insert_request)
    #     if str(number_of_lines) == 0:
    #         is_first_transaction = True
    #     else:
    #         # Get last element if table is not empty
    #         is_first_transaction = False
    #         sqlite_insert_request = f"SELECT * FROM {TABLE_TRANSACTIONS_NAME} ORDER by time_transaction DESC LIMIT 1;"
    #         request_is_successful, request_response = DatabaseRequests.execute_request_to_database(
    #             sqlite_insert_request)
    #         last_transaction = json.loads(json.dumps([dict(ix) for ix in request_response]))
    #
    #     print("************************")
    #     print("request_is_successful: '{}'".format(request_is_successful))
    #     print("last_transaction: '{}'".format(last_transaction))
    #     print("************************")
    #
    #     return is_first_transaction, last_transaction

    @staticmethod
    def size_of_table():
        sqlite_insert_request = f"SELECT count(*) FROM tblTransactions;"
        request_is_successful_count, number_of_lines = DatabaseRequests.execute_request_to_database(
            sqlite_insert_request)
        number_of_lines = json.loads(json.dumps([dict(ix) for ix in number_of_lines]))[0]["count(*)"]
        print("number_of_lines: '{}'".format(number_of_lines))
        return request_is_successful_count, number_of_lines
