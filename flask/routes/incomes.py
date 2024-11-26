from flask import request, Blueprint, jsonify
from routes.sessions import current_session
from bussines.wallet import Wallet

incomes = Blueprint('incomes', __name__)


# Define incomes API route.
# Recieve a data_json with the next keys; amount, description, date and create a current 
# wallet where the instance recieve a user_id current session.
@incomes.route('/incomes', methods=['POST'])
def register_income():
    try:

        data_json = request.get_json()
        user_id = current_session.get('user_id')
        current_wallet = Wallet(user_id)
        current_wallet.insert_amount(data_json.get('amount'), data_json.get('description'), data_json.get('date'))
        return jsonify({"message": "income_saved_successfully", "response": "success"}), 201

    except Exception as e:
        return jsonify({"message" : "server_not_process_data", "response" : str(e)}), 400

# Define incomes API amount per-day route.
# Recieve a data_json with the next keys; date. it ensures the current session through user_id 
# hash table reference, therefore it will do current wallet instance.
@incomes.route('/incomes/per-day', methods=['GET'])
def get_amount_per_day():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        current_wallet = Wallet(user_id)
        return jsonify({"message": "income_per_day_returned", "resource" : current_wallet.get_amount_per_day(data_json['date'], 1)}), 201

    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500

@incomes.route('/incomes/per-month', methods=['GET'])
def get_amount_per_month():
    try: 
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        current_wallet = Wallet(user_id)
        return jsonify({"message": "income_per_month_returned", "resource": current_wallet.get_amount_per_month(data_json['date'], 1)}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500

@incomes.route('/incomes/per-year', methods=['GET'])
def get_amount_per_year():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        current_wallet= Wallet(user_id)
        return jsonify({"message": "income_per_year_returned", "resource": current_wallet.get_amount_per_year(data_json['date'], 1)}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response" : str(e)}), 500

@incomes.route('/incomes/per-week', methods=['GET'])
def get_amount_per_week():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        current_wallet = Wallet(user_id)
        return jsonify({"message": 'income_per_week_returned', "resource": current_wallet.get_amount_per_week(data_json['date'], 1)}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response" : str(e)}), 500

@incomes.route("/incomes/allincomes", methods=["GET"])
def get_all_incomes():
    user_id = current_session.get('user_id')  
    if not user_id:
        return jsonify({"status": "error", "message": "No autenticado"}), 401

    wallet = Wallet(user_id=user_id)

    try:
        incomes = wallet.get_all_incomes() 
        return jsonify({"status": "success", "data": incomes}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500