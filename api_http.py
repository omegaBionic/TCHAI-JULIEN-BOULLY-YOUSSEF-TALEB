# from flask import *
import datetime
import json

from flask import Flask, render_template, request, make_response, jsonify

from DatabaseRequests import *

app = Flask(__name__)
transactions = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/transaction', methods=['POST'])
def add():
    """Add a user to the database"""
    # Get the body of the request as a json object
    transaction_json = request.json

    # Get the elements of the json object
    sender = transaction_json.get("sender", None)
    receiver = transaction_json.get("receiver", None)
    money = transaction_json.get("money", None)
    # Get the current time and date as a string
    time_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transaction_is_added, request_response = DatabaseRequests.insert_transaction_into_table(sender=sender,
                                                                                            receiver=receiver,
                                                                                            time_transaction=time_transaction,
                                                                                            money=money)
    if transaction_is_added:
        response_message_dict = {'message': 'Transaction added', 'code': 'SUCCESS'}
        return make_response(jsonify(response_message_dict), 200)
    else:
        response_message_dict = {'message': 'TRANSACTION CANNOT BE ADDED', 'code': 'ERROR',
                                 'details': 'Ensure that the body is in a JSON format with the fields: sender, receiver and money.'}
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
    _, money = DatabaseRequests.get_money_person(username=username)
    return make_response(jsonify({'person': username, 'money': money}), 200)


app.run(host='0.0.0.0', debug=True)
