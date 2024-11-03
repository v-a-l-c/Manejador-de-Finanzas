from flask import request, Blueprint, jsonify
from models.users import Usuarios
import hashlib


login_route = Blueprint('login_route', __name__)

#define login endpoint logic
@login_route.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:

            current_username = request.form["username"]
            currrent_password = request.form["password"]
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user = db.session.execute(db.select(users).filter_by(username = current_username)).first_or_404()

            if user.get_password_hash() == password_hash:
                #define a ok hash password through database
                return jsonify({'username': user.get_username(), 'message': "success"})

        except Exception as error:
            return jsonify({'response': "error_find_query"})
    else:
        return jsonify({'response': "NO_POST_METHOD"})