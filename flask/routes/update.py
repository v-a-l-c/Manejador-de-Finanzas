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


@update.route('/update_rfc', methods=['PUT'])
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
    

@update.route('/update_curp', methods=['PUT'])
def update_curp():
    data = request.get_json()
    curp = data.get('CURP')
    user_id = current_session.get('user_id')
    user = Usurarios.query.get(user_id)
    if is_curp_correct(curp):
        user.set_curp(curp)
        db.session.commit()
        return jsonify({"message" : "curp_uploaded"}), 201
    return jsonify({"message": "invalid_curp_no_saved"}), 401

@update.route('/update_name', methods=['PUT'])
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

@update.route('/update_last_name', methods=['PUT'])
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