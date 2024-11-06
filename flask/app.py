from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
from models.users import Usuarios
from routes.signup import signup_bp
from routes.signout import signout_bp
from routes.login import login_route

def create_app():
    app = Flask(__name__, static_folder='public', static_url_path='')  # Configura Flask para servir archivos estáticos desde "public"
    app.secret_key = "epicomomentogamer"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpassword@mysql/mydatabase'
    CORS(app, resources={r"/auth/*": {"origins": "*", "methods": ["POST", "OPTIONS"], "supports_credentials": True}})
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Esto creará todas las tablas en la base de datos
    
    # Registra los blueprints para las rutas de autenticación
    app.register_blueprint(signup_bp, url_prefix='/auth')
    app.register_blueprint(signout_bp, url_prefix='/auth')
    app.register_blueprint(login_route, url_prefix='/auth')

    # Ruta para servir la página principal
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    # Ruta para servir otras páginas (e.g., /signup.html, /dashboard.html)
    @app.route('/<path:path>')
    def serve_file(path):
        return send_from_directory(app.static_folder, path)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

