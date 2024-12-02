from flask import request, Blueprint, jsonify
from routes.sessions import current_session
from bussines.wallet import Wallet
from bussines.debt_account import DebtAccount
debt = Blueprint('debt', __name__)

@debt.route('/debt', methods=['POST'])
def register_debt():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        current_wallet = Wallet(user_id)
        debt_account = DebtAccount(user_id, current_wallet)
        debt_account.register_debt(
            data_json['creditor'], data_json['amount'], data_json['description'], 
            data_json['date'], 3, data_json['tag'], data_json['interest'])
        return jsonify({"message": "success_debt_saved", "response": "succcess"}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500

@debt.route('/debt/pop', methods=['POST'])
def pop_debt():
    pass

@debt.route('/debt/interest', methods=['GET'])
def calc_interest():
    pass

@debt.route('/debt/all-debts', methods=['GET'])
def get_all_debts():
    try:
        user_id = current_session.get('user_id')
        if not user_id:
            return jsonify({"status": "error", "message": "No autenticado"}), 401
        current_wallet = Wallet(user_id)
        debt_account = DebtAccount(user_id, current_wallet)
        return jsonify({"message": "success_debts_returned", "resource": debt_account.get_all_debts(3)}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500
