# routes/signout.py
from flask import Blueprint, session, jsonify
from routes.sessions import current_session
signout_bp = Blueprint('signout_bp', __name__)

@signout_bp.route('/signout', methods=['POST'])
def signout():
    current_session.pop('user_id', None)
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200
