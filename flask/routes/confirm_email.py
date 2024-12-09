from flask import Blueprint, jsonify
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from models.users import Usuarios
from models import db

confirm_email_bp = Blueprint('confirm_email', __name__)
serializer = URLSafeTimedSerializer('clave-secreta-para-tokens')

@confirm_email_bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=36000)  
    except (SignatureExpired, BadSignature):
        return jsonify({"message": "Invalid or expired confirmation link"}), 400

    user = Usuarios.query.filter_by(mail=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.authenticated = True  
    db.session.commit()
    
    return jsonify({"message": "Email confirmed successfully"}), 200
