# from flask import *
import datetime

from flask import Flask, render_template, request, make_response, jsonify

from database_requests import *

app = Flask(__name__)
transactions = []


@app.route('/')
def index():
    request_is_successful, request_response = DatabaseRequests.get_transactions()
    json_datas = json.loads(json.dumps([dict(ix) for ix in request_response]))

    # Truncate money
    for i, transaction in enumerate(json_datas):
        json_datas[i]["money"] = format(transaction["money"], ".6f")

    print(json_datas)

    return render_template('index.html', jsonfile=json_datas)


@app.route('/add', methods=['GET'])
def add():
    return render_template('add.html')


@app.route('/wallet', methods=['GET'])
def wallet():
    # Get all transaction for sort after and get wallets
    request_is_successful, request_response = DatabaseRequests.get_transactions()
    json_datas = json.loads(json.dumps([dict(ix) for ix in request_response]))

    # Append sender and receiver in wallets list
    wallet_names = []
    for json_data in json_datas:
        wallet_names.append(json_data["sender"]) if json_data["sender"] not in wallet_names else wallet_names
        wallet_names.append(json_data["receiver"]) if json_data["receiver"] not in wallet_names else wallet_names
    print("wallet_name_list: '{}'".format(wallet_names))

    # Request database for all this wallets
    wallets = []
    for wallet_name in wallet_names:
        request_is_successful, request_response = DatabaseRequests.get_money_person(username=wallet_name)
        if request_is_successful:
            wallets.append({"wallet_name": wallet_name, "wallet_balance": request_response})
            print("wallet_name: '{}' - wallet_balance: '{}'".format(wallet_name, request_response))
        else:
            print(" ---> Wallet NOT added")

    wallets = json.loads(json.dumps([dict(ix) for ix in wallets]))
    return render_template('wallet.html', jsonfile=wallets)


@app.route('/api/add', methods=['POST'])
def api_add():
    """Add a transaction to the database"""
    # Get the body of the request as a json object
    transaction = request.form

    # Get the elements of the json object
    sender = transaction['sender']
    receiver = transaction['receiver']
    money = transaction['money']

    # Get the private key from JSON in string format, for example:
    # "private_key": "0xA12D5...."
    private_key = 0x0
    if "private_key" in transaction:
        print("private_key exists in JSON")
        hex_string = transaction["private_key"]
        an_integer = int(hex_string, 16)
        private_key = hex(an_integer)
    else:
        print("private key does not exist in JSON")

    print("[api_add] POST: '{}' - '{}' - '{}' - '{}".format(sender, receiver, money, private_key))

    # Add the user to the table containing the users with their public keys
    request_is_successful, request_response, public_key_created, private_key_created = DatabaseRequests.insert_user_to_table_public_key(sender)

    if private_key_created != 0x0:
        private_key = private_key_created

    # Get the current time and date as a string
    time_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    signature = HashTchai.calculate_signature(sender, receiver, money, time_transaction, private_key)
    transaction_is_added, request_response = DatabaseRequests.insert_transaction_into_table(sender=sender,
                                                                                            receiver=receiver,
                                                                                            time_transaction=time_transaction,
                                                                                            money=money,
                                                                                            signature=signature)
    print("[api_add] POST: '{}' - '{}'".format(transaction_is_added, request_response))
    if transaction_is_added:
        response_message_dict = {'message': 'Transaction added', 'code': 'SUCCESS'}
        return make_response(jsonify(response_message_dict), 200)
    else:
        response_message_dict = {'message': 'TRANSACTION CANNOT BE ADDED', 'code': 'ERROR',
                                 'details': 'Ensure that the database is created and the body is in a JSON format with the fields: sender, receiver and money.'}
        return make_response((jsonify(response_message_dict), 400))


@app.route('/api/transactions', methods=['GET'])
def show_all_transactions():
    """Show transactions in chronological order"""
    request_is_successful, request_response = DatabaseRequests.get_transactions()
    # return request_response.__str__()
    if request_is_successful:
        return make_response(json.dumps([dict(ix) for ix in request_response]), 200)
    else:
        return make_response("ERROR", 400)


@app.route('/api/transactions/<username>', methods=['GET'])
def show_user_transactions(username):
    """Show transactions in chronological order"""
    request_is_successful, request_response = DatabaseRequests.get_user_transactions(username)
    # return request_response.__str__()
    if request_is_successful:
        return make_response(json.dumps([dict(ix) for ix in request_response]), 200)
    else:
        return make_response("ERROR", 400)


@app.route('/api/transactions/<username>/money', methods=['GET'])
def show_user_money(username):
    """Show how much money a user has"""
    request_is_successful, money = DatabaseRequests.get_money_person(username=username)
    if request_is_successful:
        return make_response(jsonify({'person': username, 'money': money}), 200)
    else:
        return make_response("ERROR", 400)


@app.route('/api/integrity', methods=['GET'])
def integrity():
    # Vars global
    salt_first_iteration = "boule0and0youss666"

    # Get all transactions
    request_is_successful, request_response = DatabaseRequests.get_transactions()

    if not request_is_successful:
        return make_response(jsonify({'ERROR': "CANNOT SEND REQUEST TO DATABASE"}), 400)

    transactions = json.loads(json.dumps([dict(ix) for ix in request_response]))

    # Check hash integrity
    false_transactions = []
    for i, transaction in enumerate(transactions):
        if int(transaction["id"]) == 1:
            calculate_hash = HashTchai.calculate_hash(sender=transaction["sender"], receiver=transaction["receiver"],
                                                      time_transaction=transaction["time_transaction"],
                                                      money=transaction["money"],
                                                      last_hash=salt_first_iteration, is_first_iteration=True)
        else:
            calculate_hash = HashTchai.calculate_hash(sender=transaction["sender"], receiver=transaction["receiver"],
                                                      time_transaction=transaction["time_transaction"],
                                                      money=transaction["money"],
                                                      last_hash=transactions[i - 1]["hash"], is_first_iteration=False)

        # Check hash
        if calculate_hash == transaction["hash"]:
            print("Transaction OK")
        else:
            print("Transaction FAIL")
            false_transactions.append([transaction, ["calculate_hash", calculate_hash]])

    # Return request
    if len(false_transactions) == 0:
        return make_response(jsonify({'integrity': "OK"}), 200)
    else:
        return make_response(jsonify([false_transactions]), 200)


app.run(host='0.0.0.0', debug=True)
