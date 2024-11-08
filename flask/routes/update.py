from models.users import Usuarios 
from models import db  
from flask import jsonify, Blueprint, session, request
from routes.sessions import current_session

update = Blueprint('update', __name__)

## Rutas de actualización de datos. Hecho por el Front pa##
# Nombre de usuario
@update.route('/update_username', methods=['PUT'])
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


@update.route('/update_mail', methods=['PUT'])
def update_mail():

    data = request.get_json()
    new_mail = data.get("mail")
    user_id = current_session.get('user_id')
    user = Usuarios.query.get(user_id)
    
    if user:
        user.set_mail(new_mail)
        db.session.commit()
        return({"message": "success_update_mail"}), 201
    
    return jsonify({"error": "no_user_found "}), 400

@update.route('/update_password', methods=['PUT'])
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