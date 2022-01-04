
import random
import database_requests

if __name__ == "__main__":
    column_name_money = "money"
    # Generate random float between 100 and 0
    new_money_value = round(random.random()*100, 2)
    id_transaction_to_modify = 1

    TABLE_TRANSACTIONS_NAME = database_requests.TABLE_TRANSACTIONS_NAME

    # Request to attack tchai V1 by updating the table
    sqlite_request_attack = f"UPDATE {TABLE_TRANSACTIONS_NAME} SET {column_name_money} = {new_money_value} " \
                            f"WHERE  id= {id_transaction_to_modify}; "
    print(f"sqlite_request_attack: {sqlite_request_attack}")
    database_requests.DatabaseRequests.execute_request_to_database(sqlite_request_attack)
    