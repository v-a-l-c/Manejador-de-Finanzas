from flask import Blueprint, request, jsonify, url_for, current_app
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from models.users import Usuarios
from models import db
from routes.sessions import current_session
from bussines import Mail 

signup_bp = Blueprint('signup', __name__)

serializer = URLSafeTimedSerializer('clave-secreta-para-tokens')

@signup_bp.route('/', methods=['POST'])
def signup():
    try:
        data = request.get_json() 
    except Exception as e:
        return jsonify({"message": "Invalid data format", "error": str(e)}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('mail')

    if not username or not password or not email:
        return jsonify({"message": "Missing username, password, or email"}), 400

    if Usuarios.query.filter_by(username=username).first() or Usuarios.query.filter_by(mail=email).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = Usuarios(
        username=username,
        password_hash=generate_password_hash(password),
        authenticated=False,
        mail=email,
        firstName=data.get('firstName', ''),
        secondNames=data.get('secondNames', ''),
        curp=data.get('curp', ''),
        rfc=data.get('rfc', '')
    )

    db.session.add(new_user)
    db.session.commit()

    current_session['user_id'] = new_user.id

    token = serializer.dumps(email, salt='email-confirm')
    confirm_url = url_for('confirm_email.confirm_email', token=token, _external=True)

    subject = "Confirm your email"
    body = f"""
    <p>Hi {username},</p>
    <p>Thank you for registering. Please click the link below to confirm your email:</p>
    <p><a href="{confirm_url}">Confirm Email</a></p>
    <p>This link will expire in 10 hours.</p>
    """

    try:
        mail_service = Mail(sender='monkeymyp@gmail.com', reciever=email)
        mail_service.send_mail(subject, body)
    except Exception as e:
        error_message = str(e)  
        return jsonify({
            "message": "User created, but failed to send confirmation email",
            "error": error_message
        }), 500



    return jsonify({"message": "User created successfully, confirmation email sent"})
