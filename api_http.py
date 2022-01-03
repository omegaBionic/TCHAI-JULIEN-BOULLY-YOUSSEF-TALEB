# from flask import *
import datetime
import json
from flask import Flask, render_template, request, make_response, jsonify

from database_requests import *

app = Flask(__name__)
transactions = []


@app.route('/')
def index():
    request_is_successful, request_response = DatabaseRequests.get_transactions()
    json_datas = json.loads(json.dumps([dict(ix) for ix in request_response]))
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
        if request_response:
            wallets.append({"wallet_name": wallet_name, "wallet_balance": request_response})
            print("wallet_name: '{}' - wallet_balance: '{}'".format(wallet_name, request_response))
        else:
            print(" ---> Wallet NOT added")

    wallets = json.loads(json.dumps([dict(ix) for ix in wallets]))
    return render_template('wallet.html', jsonfile=wallets)


@app.route('/api/add', methods=['POST'])
def api_add():
    """Add a user to the database"""
    # Get the body of the request as a json object
    transaction = request.form

    # Get the elements of the json object
    sender = transaction['sender']
    receiver = transaction['receiver']
    money = transaction['money']
    print("[api_add] POST: '{}' - '{}' - '{}'".format(sender, receiver, money))

    # Get the current time and date as a string
    time_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction_is_added, request_response = DatabaseRequests.insert_transaction_into_table(sender=sender,
                                                                                            receiver=receiver,
                                                                                            time_transaction=time_transaction,
                                                                                            money=money)
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


app.run(host='0.0.0.0', debug=True)
