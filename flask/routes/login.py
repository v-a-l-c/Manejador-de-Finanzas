from flask import request, Blueprint, jsonify, session
from models.users import Usuarios
from models import db

login_route = Blueprint('login_route', __name__)

#define login endpoint logic
@login_route.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = session.get("user_id")
        data_json = request.get_json()
        password = data_json.get('password')
        current_username = data_json.get('username')
        user = db.session.execute(db.select(Usuarios).filter_by(username = current_username)).scalar_one_or_none()

        if not user: 
            return jsonify({"username": current_username, "response": "no_user_found"}), 400

        elif user.check_password(password):
            return jsonify({"username": current_username, "response": "success"}), 201

        else:
            return jsonify({"username": current_username, "response": "no_access", "description": "invalid password"})

    return jsonify({'response': "NO_POST_METHOD"})