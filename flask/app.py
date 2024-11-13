from flask import Flask, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
from models.users import Usuarios
from models.types import initialize_types


def create_app():
    app = Flask(__name__, static_folder='public', static_url_path='')
    app.secret_key = "epicomomentogamer"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpassword@mysql/mydatabase'
    CORS(app, resources={r"/auth/*": {"origins": "*", "methods": ["POST", "OPTIONS", "PUT"], "supports_credentials": True}})
    db.init_app(app)


    from routes.signup import signup_bp
    from routes.signout import signout_bp
    from routes.login import login_route
    from routes.update import update

    

    with app.app_context():
        db.create_all()
        initialize_types()

    app.register_blueprint(update, url_prefix='/auth')
    app.register_blueprint(signup_bp, url_prefix='/auth')
    app.register_blueprint(signout_bp, url_prefix='/auth')
    app.register_blueprint(login_route, url_prefix='/auth')

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_file(path):
        return send_from_directory(app.static_folder, path)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
