from flask import request, Blueprint, jsonify
from routes.sessions import current_session
from bussines.wallet import Wallet

tags = Blueprint('tags', __name__)

@tags.route('/', methods=['GET'])
def load_tags():
    try:
        data_json = request.get_json()
        current_wallet = Wallet(current_session.get('user_id'))
        wallet.get_my_tags()
    except Exception as e:
        return jsonify({"message": "server_no_proccess_data", "response": str(e)})