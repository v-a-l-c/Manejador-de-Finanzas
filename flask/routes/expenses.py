from flask import request, Blueprint, jsonify
from models.transactions import Transactions
from models import db
from routes.sessions import current_session

expenses_bp = Blueprint('expenses_bp', __name__)

#Por el momento lo agrego en transaction (pq creo que no hay egresos en el front).
@expenses_bp.route('/transaction', methods=['POST'])
def addExpense():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500

    if not data or 'amount' not in data or 'description' not in data or 'date' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    amount = data.get('amount')
    description = data.get('description')
    date = data.get('date')

    new_expense = Transactions(
        user_id=current_session['user_id'],
        type_id=2,
        amount=amount,
        description=description,
        date=date
    )

    try:
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({"response": "Expense_added_successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500