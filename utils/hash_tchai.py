import hashlib


class HashTchai:
    @staticmethod
    def calculate_hash(sender, receiver, time_transaction, money):
        # Formalise datas
        money = format(float(money), ".6f")

        # hash
        salt = "youssandboule"

        # DEBUG
        # print("******")
        # print("sender: '{}'".format(sender))
        # print("receiver: '{}'".format(receiver))
        # print("salt: '{}'".format(salt))
        # print("time_transaction: '{}'".format(time_transaction))
        # print("money: '{}'".format(money))
        # print("******")

        # Calculate hash
        transaction_hash = hashlib.sha512(f"{sender}{receiver}{salt}{time_transaction}{money}".encode())
        transaction_hash = transaction_hash.digest().hex()
        # print("[utils/calculate_hash] transaction_hash: '{}'".format(transaction_hash))

        return transaction_hash
