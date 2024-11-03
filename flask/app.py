from flask import Flask
from models import db 
from models.users import Usuarios  # Asegúrate de importar tu modelo de usuarios
from routes.signup import signup_bp
from routes.signout import signout_bp
from routes.login import login_route  

def create_app():
    app = Flask(__name__)
    app.secret_key = "epicomomentogamer"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpassword@mysql/mydatabase'
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Esto creará todas las tablas, asegúrate de que los modelos estén definidos

    app.register_blueprint(signup_bp, url_prefix='/auth')
    app.register_blueprint(signout_bp, url_prefix='/auth')
    app.register_blueprint(login_route, url_prefix='/auth') 

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
