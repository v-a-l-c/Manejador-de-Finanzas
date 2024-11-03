from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.users import Usuarios 
from models import db  

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/', methods=['POST'])  # La ruta ahora es relativa
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    if Usuarios.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = Usuarios(
        username=username,
        password_hash=generate_password_hash(password),
        authenticated=False
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201
