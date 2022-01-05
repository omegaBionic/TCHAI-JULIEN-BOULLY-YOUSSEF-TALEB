import hashlib
import database_requests
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from cryptography.hazmat.primitives.serialization import *


class HashTchai:
    @staticmethod
    def calculate_hash(sender, receiver, time_transaction, money, last_hash, is_first_iteration=False):
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

    @staticmethod
    def generate_rsa():
        key = RSA.generate(2048)
        public_key = key.export_key()
        private_key = key.publickey().export_key()
        return public_key, private_key

    @staticmethod
    def calculate_signature(sender, receiver, money, time_transaction, private_key):
        message = f'{sender} {receiver} {money} {time_transaction}'

        # TODO use the private key which is not stored in a pem or der file
        key = RSA.import_key(open('private_key.der').read())

        h = SHA256.new(message)
        signature = pkcs1_15.new(key).sign(h)

        return signature.hex()


