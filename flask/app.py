from flask import Flask
from .db_config import db  
from routes.signup import signup_bp 
from routes.signout import signout_bp  

def create_app():
    app = Flask(__name__)
    app.secret_key = "epicomomentogamer"  

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpassword@mysql/mydatabase'
    db.init_app(app)

    app.register_blueprint(signup_bp, url_prefix='/auth')
    app.register_blueprint(signout_bp, url_prefix='/auth')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
