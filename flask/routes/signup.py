from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.users import Usuarios 
from models import db  
from routes.sessions import current_session

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/', methods=['POST'])
def signup():
    try:
        data = request.get_json()

    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500

    username = data.get('username')
    password = data.get('password')
    mail = data.get('mail')

    if not username or not password:
        return jsonify({"message": "Missing username or password"})

    if Usuarios.query.filter_by(username=username).first() or Usuarios.query.filter_by(mail=mail).first():
        return jsonify({"message": "User already exists"})

    new_user = Usuarios(
        username=username,
        password_hash=generate_password_hash(password),
        authenticated=False,
        mail=mail,
        firstName=data.get('firstName', ''),  # vacios de primerassss
        secondNames=data.get('secondNames', ''),
        curp=data.get('curp', ''),
        rfc=data.get('rfc', '')
    )

    db.session.add(new_user)
    db.session.commit()
    current_session['user_id'] = new_user.id
    return jsonify({"message": "User created successfully"})
