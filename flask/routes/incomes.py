from flask import request, Blueprint, jsonify, Response
from routes.sessions import current_session
from bussines.wallet import Wallet
from bussines.pdf_report import PDFreport

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
        current_wallet.insert_amount(data_json.get('amount'), data_json.get('description'), data_json.get('date'), 1, data_json.get('tag'))
        return jsonify({"message": "income_saved_successfully", "response": "success"}), 201

    except Exception as e:
        return jsonify({"message" : "server_not_process_data", "response" : str(e)}), 400

@incomes.route("/incomes/allincomes", methods=["GET"])
def get_all_incomes():
    user_id = current_session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "No autenticado"}), 401

    wallet = Wallet(user_id)

    try:
        return jsonify({"status": "success", "data": wallet.get_all_transactions(1)}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@incomes.route('/incomes/search', methods=['POST'])
def search_transaction():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        current_wallet = Wallet(user_id)
        return jsonify({"message": "transaction_search_returned", "resource": current_wallet.search_transaction(
        data_json['date'], data_json['type_of_date'], data_json['tag'], 1)})
    except Exception as e:
        return jsonify({"message": "server_not_process_data", "response": str(e)}), 500

@incomes.route('/incomes/delete', methods=['DELETE'])
def delete_transaction():
    try:
        data_json = request.get_json()
        user_id = current_session.get('user_id')
        transaction_id = data_json.get("id")
        current_wallet = Wallet(user_id)
        current_wallet.delete_transaction(transaction_id)
        return jsonify({"message": "transaction_deleted_successfully", "response": "success"}), 201

    except Exception as e:
        return jsonify({"message" : "server_not_process_data", "response" : str(e)}), 400

@incomes.route('/incomes/pdf', methods=['GET'])
def generate_pdf():
    try:
        user_id = current_session.get('user_id')
        current_wallet = Wallet(user_id)
        reporte = PDFreport(current_wallet)
        pdf_output = reporte.output(dest='S').encode('latin1')
        return Response(pdf_output, mimetype='application/pdf', headers={
            "Content-Disposition": "inline; filename=report.pdf"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
