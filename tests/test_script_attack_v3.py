import random
import database_requests

if __name__ == "__main__":
    TABLE_TRANSACTIONS_NAME = database_requests.TABLE_TRANSACTIONS_NAME

    # Request to attack tchai V1 by updating the table
    sqlite_request_attack = f"INSERT INTO tblTransactions (sender, receiver, time_transaction, money, hash) VALUES ('yous', 'boule', '2021-12-08 02:23:22', 1000000.000000, 'HASHFAKE');"
    print(f"sqlite_request_attack: {sqlite_request_attack}")
    database_requests.DatabaseRequests.execute_request_to_database(sqlite_request_attack)
