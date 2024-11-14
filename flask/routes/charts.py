from flask import Blueprint, jsonify
from models.transactions import Transactions
from models.types import Types  # Si tienes una tabla 'types' para los tags
from models import db

chart_bp = Blueprint('chart', __name__)

@chart_bp.route('/api/transactions/summary', methods=['GET'])
def transactions_summary():

    results = db.session.query(
        Types.name,  
        db.func.sum(Transactions.amount)
    ).join(Transactions, Transactions.type_id == Types.id
    ).group_by(Types.name).all()

    data = [{"tag": tag, "total": float(total)} for tag, total in results]
    return jsonify(data)
