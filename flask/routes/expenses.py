from flask import request, Blueprint, jsonify
from models.transactions import Transactions
from models import db
from routes.sessions import current_session
from bussines.wallet import Wallet

expenses_bp = Blueprint('expenses_bp', __name__)

@expenses_bp.route('/expenses/add', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()
        
        if not data or 'amount' not in data or 'description' not in data or 'date' not in data:
            return jsonify({"message": "Missing required fields"}), 400

        
        amount = data.get('amount')
        description = data.get('description')
        date = data.get('date')
        user_id = current_session.get('user_id')

        if user_id is None:
            return jsonify({"message": "User not authenticated"}), 401

        new_expense = Transactions(
            user_id=user_id,
            type_id=2, 
            amount=amount,
            description=description,
            date=date
        )

        db.session.add(new_expense)
        db.session.commit()
        return jsonify({"response": "Expense_added_successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500


@expenses_bp.route('/expenses/per-day', methods=['POST'])
def get_expense_per_day():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        
        if user_id is None:
            return jsonify({"message": "User not authenticated"}), 401

        current_wallet = Wallet(user_id)
        return jsonify({
            "message": "expense_per_day_returned", 
            "resource": current_wallet.get_amount_per_day(data_json['date'], type_id=2)
        }), 200

    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500


@expenses_bp.route('/expenses/per-month', methods=['POST'])
def get_expense_per_month():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        
        if user_id is None:
            return jsonify({"message": "User not authenticated"}), 401

        current_wallet = Wallet(user_id)
        return jsonify({
            "message": "expense_per_month_returned", 
            "resource": current_wallet.get_amount_per_month(data_json['date'], type_id=2)
        }), 200

    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500


@expenses_bp.route('/expenses/per-year', methods=['POST'])
def get_expense_per_year():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        
        if user_id is None:
            return jsonify({"message": "User not authenticated"}), 401

        current_wallet = Wallet(user_id)
        return jsonify({
            "message": "expense_per_year_returned", 
            "resource": current_wallet.get_amount_per_year(data_json['date'], type_id=2)
        }), 200

    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500
