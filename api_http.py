from flask import *
import datetime
from database_connection import *

app = Flask(__name__)
transactions = []


@app.route('/transaction', methods=['POST'])
def add():
    # Get the body of the request as a json object
    transaction_json = request.json

    # Get the elements of the json object
    sender = transaction_json.get("sender", None)
    receiver = transaction_json.get("receiver", None)
    money = transaction_json.get("money", None)
    # Get the current time and date as a string
    time_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_variable_into_table(sender=sender, receiver=receiver, time_transaction=time_transaction,money=money)

    response_message_dict = {'message': 'Transaction added', 'code': 'SUCCESS'}
    return make_response(jsonify(response_message_dict), 200)







app.run(host='0.0.0.0', debug=True)
