from flask import request, Blueprint, jsonify
from routes.sessions import current_session
from bussines.wallet import Wallet
from bussines.debt_account import DebtAccount


debt = Blueprint('debt', __name__)

def get_current_debtAcc():
    user_id = current_session.get('user_id')
    current_wallet = Wallet(user_id)
    return DebtAccount(current_wallet)

@debt.route('/debt', methods=['POST'])
def register_debt():
    try:
        data_json = request.get_json()
        debt_account = get_current_debtAcc()
        debt_account.register_debt(
            data_json['creditor'], data_json['amount'], data_json['description'], 
            data_json['date'], 3, data_json['category'], data_json['interest'])
        return jsonify({"message": "success_debt_saved", "response": "success"}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500

@debt.route('/debt/pop', methods=['DELETE'])
def pop_debt():
    try:
        data_json = request.get_json()
        debt_account = get_current_debtAcc()
        debt_account.pop_debt(data_json['id'])
        return jsonify({"message": "success debt deleted and transfered to expenses section", "response": "success"}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500

@debt.route('/debt/interest', methods=['GET'])
def calc_interest():
    try:
        user_id = current_session.get('user_id')
        if not user_id:
            return jsonify({"status": "error", "message": "No autenticado"}), 401
        data_json = request.get_json()
        debt_account = get_current_debtAcc()
        return jsonify({"message": "server_calc_debts", "resource": debt_account.calc_interest(data_json['id'])}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500

@debt.route('/debt/all-debts', methods=['GET'])
def get_all_debts():
    try:
        user_id = current_session.get('user_id')
        if not user_id:
            return jsonify({"status": "error", "message": "No autenticado"}), 401
        debt_account = get_current_debtAcc()
        return jsonify({"status": "success", "resource": debt_account.get_all_debts(3)}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500

@debt.route('/debt/remind-debts', methods=['GET'])
def remind_record_debt():
    try:
        user_id = current_session.get('user_id')
        if not user_id:
            return jsonify({"status": "error", "message": "No autenticado"}), 401
        data_json = request.get_json()
        debt_account = get_current_debtAcc()
        return jsonify({"message": "server_sent_record", "resource": debt_account.date_status(data_json['id'])}), 201
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500
