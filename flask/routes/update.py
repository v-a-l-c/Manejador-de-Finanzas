from models.users import Usuarios 
from models import db  
from flask import Flask, jsonify, Blueprint, session, request, url_for
from routes.sessions import current_session
from bussines import Mail
from itsdangerous import URLSafeTimedSerializer



update_bp = Blueprint('update', __name__)
serializer = URLSafeTimedSerializer('clave-secreta-para-tokens')

## Rutas de actualización de datos. Hecho por el Front pa##
# Nombre de usuario
@update_bp.route('/update_username', methods=['PUT'])
def update_username():

    data = request.get_json()
    new_username = data.get("username")
    user_id = current_session.get('user_id')
    user = Usuarios.query.get(user_id)

    if user:
        user.set_username(new_username)
        db.session.commit()
        return jsonify({"message": "Username updated successfully"}), 201

    return jsonify({"error": "user_not_found"}), 400


@update_bp.route('/update_email', methods=['PUT'])
def update_mail():
    try:
        data = request.get_json()  
    except Exception as e:
        logging.error(f"Invalid data format: {str(e)}")
        return jsonify({"message": "Invalid data format", "error": str(e)}), 400

    new_mail = data.get("mail")
    user_id = current_session.get('user_id')

    if not user_id or not new_mail:
        logging.error(f"Missing user_id or new mail. user_id: {user_id}, new_mail: {new_mail}")
        return jsonify({"message": "Missing user_id or new mail"}), 400

    user = Usuarios.query.get(user_id)

    if not user:
        logging.error(f"User not found. user_id: {user_id}")
        return jsonify({"message": "User not found"}), 404

    try:
        user.mail = new_mail
        user.authenticated = False
        db.session.commit()

        token = serializer.dumps(new_mail, salt='email-confirm')
        confirm_url = url_for('confirm_email.confirm_email', token=token, _external=True)

        subject = "Confirm your new email"
        body = f"""
        <p>Hi {user.username},</p>
        <p>You have updated your email. Please click the link below to confirm your new email address:</p>
        <p><a href="{confirm_url}">Confirm Email</a></p>
        <p>This link will expire in 1 hour.</p>
        """

        mail_service = Mail(sender='monkeymyp@gmail.com', reciever=new_mail)
        mail_service.send_mail(subject, body)

        return jsonify({"message": "Email updated and confirmation email sent"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to update email or send confirmation", "details": str(e)}), 500



@update_bp.route('/update_password', methods=['PUT'])
def update_password():

    data = request.get_json()
    password = data.get("password")
    user_id = current_session.get('user_id')
    user = Usuarios.query.get(user_id)
    
    if user:
        user.set_password(password)
        db.session.commit()
        return({"message": "success_update_password"}), 201
    
    return jsonify({"error": "no_user_found "}), 400

def is_rfc_correct(rfc):
    clear_rfc = rfc.strip()
    verify_upper = ""
    if len(clear_rfc) != 13:
        return False
    for index  in range(0, 4):
        verify_upper = clear_rfc[index]
    if  not verify_upper.isupper():
        return False
    return True


@update_bp.route('/update_rfc', methods=['PUT'])
def update_rfc():
    data = request.get_json()
    rfc = data.get('RFC')
    user_id = current_session.get('user_id')
    user = Usuarios.query.get(user_id)
    if user and is_rfc_correct(rfc):
        user.set_rfc(rfc)
        db.session.commit()
        return jsonify({"message" : "rfc_uploaded"}), 201
    return jsonify({"msessage": "invalid_rfc_no_saved"}), 401

def is_curp_correct(curp):
    curp = curp.strip()
    if len(curp) != 18:
        return False
    return True
    

@update_bp.route('/update_curp', methods=['PUT'])
def update_curp():
    data = request.get_json()
    curp = data.get('CURP')
    user_id = current_session.get('user_id')
    user = Usuarios.query.get(user_id)
    if is_curp_correct(curp):
        user.set_curp(curp)
        db.session.commit()
        return jsonify({"message" : "curp_uploaded"}), 201
    return jsonify({"message": "invalid_curp_no_saved"}), 401

@update_bp.route('/update_name', methods=['PUT'])
def update_name():
    data = request.get_json()
    name = data.get('name')
    user_id = current_session.get('user_id')
    user = Usuarios.query.get(user_id)
    if user:
        user.set_first_name(name)
        db.session.commit()
        return jsonify({"message": "name_uploaded"}), 201
        
    return jsonify({"message": "invalid_name_no_saved"}), 401

@update_bp.route('/update_last_name', methods=['PUT'])
def update_last_name():
    data =request.get_json()
    last_names = data.get('last_names')
    user_id = current_session.get('user_id')
    user = Usuarios.query.get(user_id)
    if user:
        user.set_second_names(last_names)
        db.session.commit()
        return jsonify({"message":"last_names_uploaded"}), 201

    return jsonify({"message": "invalid_last_name_no_saved"}), 401