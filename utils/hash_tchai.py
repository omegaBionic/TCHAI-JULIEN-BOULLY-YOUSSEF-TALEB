import hashlib
import database_requests

class HashTchai:
    @staticmethod
    def calculate_hash(sender, receiver, time_transaction, money, last_hash, is_first_iteration):
        # Formalise datas
        money = format(float(money), ".6f")

        # hash
        salt = "youss0and0boule123"

        # For first iteration
        if is_first_iteration:
            last_hash = "youss5boul6666"

        transaction_hash = hashlib.sha512(f"{sender}{receiver}{salt}{time_transaction}{money}{last_hash}".encode())
        transaction_hash = transaction_hash.digest().hex()
        # print("[utils/calculate_hash] transaction_hash: '{}'".format(transaction_hash))


        # Debug
        print("----------------")
        print("sender: '{}'".format(sender))
        print("receiver: '{}'".format(receiver))
        print("salt: '{}'".format(salt))
        print("time_transaction: '{}'".format(time_transaction))
        print("money: '{}'".format(money))
        print("last_hash: '{}'".format(last_hash))
        print("----------------")

        return transaction_hash
