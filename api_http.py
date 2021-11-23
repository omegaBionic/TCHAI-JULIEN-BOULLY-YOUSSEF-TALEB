from flask import *
import datetime
from database_connection import *


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

    transaction_is_added = insert_variable_into_table(sender=sender, receiver=receiver, time_transaction=time_transaction, money=money)
    if transaction_is_added:
        response_message_dict = {'message': 'Transaction added', 'code': 'SUCCESS'}
        return make_response(jsonify(response_message_dict), 200)
    else:
        response_message_dict = {'message': 'TRANSACTION CANNOT BE ADDED', 'code': 'ERROR', 'details': 'Ensure that the body is in a JSON format with the fields: sender, receiver and money.'}
        return make_response((jsonify(response_message_dict), 400))


@app.route('/api/transactions', methods=['GET'])
def show_all_transactions():
    """Show transactions in chronological order"""

    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM tblTransactions').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)




app.run(host='0.0.0.0', debug=True)
