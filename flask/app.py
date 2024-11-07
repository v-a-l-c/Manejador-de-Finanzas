from flask import Flask, send_from_directory, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
from models.users import Usuarios
from routes.signup import signup_bp
from routes.signout import signout_bp
from routes.login import login_route

def create_app():
    app = Flask(__name__, static_folder='public', static_url_path='')
    app.secret_key = "epicomomentogamer"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpassword@mysql/mydatabase'
    CORS(app, resources={r"/auth/*": {"origins": "*", "methods": ["POST", "OPTIONS"], "supports_credentials": True}})

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(signup_bp, url_prefix='/auth')
    app.register_blueprint(signout_bp, url_prefix='/auth')
    app.register_blueprint(login_route, url_prefix='/auth')

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_file(path):
        return send_from_directory(app.static_folder, path)

    # Ruta para obtener el usuario actual
    @app.route('/auth/get_user', methods=['GET'])
    def get_user():
        user_id = session.get('user_id')
        if user_id:
            user = Usuarios.query.get(user_id)
            if user:
                return jsonify({"username": user.username, "email": user.email})
        return jsonify({"error": "User not found"}), 404
    
    
    ## Rutas de actualización de datos. Hecho por el Front pa##
    # Nombre de usuario
    @app.route('/auth/update_username', methods=['POST'])
    def update_username():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        new_username = data.get("new_username")

        user = Usuarios.query.get(user_id)
        if user:
            user.username = new_username
            db.session.commit()
            return jsonify({"message": "Username updated successfully"})
        return jsonify({"error": "User not found"}), 404

    # Correo
    @app.route('/auth/update_email', methods=['POST'])
    def update_email():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        new_email = data.get("new_email")

        user = Usuarios.query.get(user_id)
        if user:
            user.email = new_email
            db.session.commit()
            return jsonify({"message": "Email updated successfully"})
        return jsonify({"error": "User not found"}), 404

    # Contraseña
    @app.route('/auth/update_password', methods=['POST'])
    def update_password():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        new_password = data.get("new_password")

        user = Usuarios.query.get(user_id)
        if user:
            user.password = new_password  # Nota: Hay que encriptar la contraseña, xfa
            db.session.commit()
            return jsonify({"message": "Password updated successfully"})
        return jsonify({"error": "User not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
