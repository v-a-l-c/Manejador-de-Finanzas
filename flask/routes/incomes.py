from flask import request, Blueprint, jsonify
from routes.sessions import current_session
from bussines.wallet import Wallet

incomes = Blueprint('incomes', __name__)

@incomes.route('/incomes', methods=['POST'])
def register_income():
    try:

        data_json = request.get_json()
        #user_id = current_session.get('user_id')

        #if not user:
         #   return jsonify({"message": "no_user_founded", "response" : str(e)}), 400

        current_wallet = Wallet(1)
        current_wallet.insert_amount(data_json.get('amount'), data_json.get('description'), data_json.get('date'))
        return jsonify({"messege": "income_saved_successfully", "response": "success"}), 201

    except Exception as e:
        return jsonify({"message" : "server_not_process_data", "response" : str(e)}), 500

@incomes.route('/incomes/per-day', methods=['POST'])
def get_amount_per_day():
    pass

@incomes.route('/incomes/per-month', methods=['POST'])
def get_amount_per_month():
    pass

@incomes.route('/incomes/per-year', methods=['POST'])
def get_amount_per_year():
    pass
