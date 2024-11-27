from flask import request, Blueprint, jsonify
from models.transactions import Transactions
from models import db
from routes.sessions import current_session
from bussines.wallet import Wallet
from models.users import Usuarios
from sqlalchemy import func



expenses_bp = Blueprint('expenses_bp', __name__)

@expenses_bp.route('/expenses/add', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()
        user_id = current_session.get('user_id')

        if not data or 'amount' not in data or 'description' not in data or 'date' not in data or 'category' not in data:
            return jsonify({"message": "Missing required fields"}), 400


        if user_id is None:
            return jsonify({"message": "User not authenticated"}), 401
        
        current_wallet = Wallet(1)
        current_wallet.insert_amount(data.get('amount'), data.get('description'), data.get('date'), 2, data.get('category'))
        return jsonify({"message": "expense_saved_successfully", "response": "success"}), 201

    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500


@expenses_bp.route('/expenses/day', methods=['POST'])
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


@expenses_bp.route('/expenses/month', methods=['POST'])
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


@expenses_bp.route('/expenses/year', methods=['POST'])
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

@expenses_bp.route('/expenses/aotday', methods=['POST'])
def get_expense_per_day_aot():
    data_json = request.get_json()
    user_id = current_session.get('user_id')

    if user_id is None:
        return jsonify({"message": "User not authenticated"}), 401

    expenses = db.session.query(
        func.date(Transactions.date).label('date'),
        func.sum(Transactions.amount).label('total_amount')
    ).join(
        Usuarios, Usuarios.id == Transactions.user_id  # Aquí es Usuarios, no Users
    ).filter(
        Transactions.type_id == 2,
        Transactions.user_id == user_id
    ).group_by(func.date(Transactions.date)).all()

    result = [{'date': str(expense.date), 'amount': expense.total_amount} for expense in expenses]

    return jsonify({
        "message": "expense_per_day_returned", 
        "resource": result
    }), 200


@expenses_bp.route('/expenses/aotmonth', methods=['POST'])
def get_expense_per_month_aot():
    data_json = request.get_json()
    user_id = current_session.get('user_id')

    if user_id is None:
        return jsonify({"message": "User not authenticated"}), 401

    expenses = db.session.query(
        func.date_format(Transactions.date, '%Y-%m').label('month'),
        func.sum(Transactions.amount).label('total_amount')
    ).join(Usuarios, Usuarios.id == Transactions.user_id).filter(
        Transactions.type_id == 2,
        Transactions.user_id == user_id
    ).group_by(
        func.date_format(Transactions.date, '%Y-%m')
    ).all()
    result = [{'date': str(expense.date), 'amount': expense.total_amount} for expense in expenses]

    return jsonify({
        "message": "expense_per_month_returned", 
        "resource": result
    }), 200


@expenses_bp.route('/expenses/aotyear', methods=['POST'])
def get_expense_per_year_aot():
    data_json = request.get_json()
    user_id = current_session.get('user_id')

    if user_id is None:
        return jsonify({"message": "User not authenticated"}), 401

    expenses = db.session.query(
        func.year(Transactions.date).label('year'),
        func.sum(Transactions.amount).label('total_amount')
    ).join(
        Usuarios, Usuarios.id == Transactions.user_id  # Aquí es Usuarios, no Users
    ).filter(
        Transactions.type_id == 2,
        Transactions.user_id == user_id
    ).group_by(func.year(Transactions.date)).all()

    result = [{'date': expense.year, 'amount': expense.total_amount} for expense in expenses]

    return jsonify({
        "message": "expense_per_year_returned", 
        "resource": result
    }), 200



@expenses_bp.route("/expenses/allexpenses", methods=["GET"])
def get_all_expenses():
    user_id = current_session.get('user_id')  
    if not user_id:
        return jsonify({"status": "error", "message": "No autenticado"}), 401

    wallet = Wallet(user_id=user_id)

    try:
        expenses = wallet.get_all_expenses() 
        return jsonify({"status": "success", "data": expenses}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500