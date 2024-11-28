from flask import request, Blueprint, jsonify
from routes.sessions import current_session
from bussines.debt_account import DebtsAccount

debts_record = Blueprint('debts_record', __name__)

@debts_record('/debts', methods=['POST'])
def register_debt():
    pass
