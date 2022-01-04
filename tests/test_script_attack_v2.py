
import database_requests

if __name__ == "__main__":
    print("---ATTACK VERSION 2---")

    TABLE_TRANSACTIONS_NAME = database_requests.TABLE_TRANSACTIONS_NAME

    # Request to attack tchai V2 by deleting a transaction (the first one in this example)
    sqlite_request_attack = f"DELETE FROM tblTransactions WHERE id = 1;"
    print(f"sqlite_request_attack: {sqlite_request_attack}")
    database_requests.DatabaseRequests.execute_request_to_database(sqlite_request_attack)

    print("---ATTACK VERSION 2 EXECUTED---")
