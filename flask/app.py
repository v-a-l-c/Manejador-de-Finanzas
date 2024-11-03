from flask import Flask
from models import db
from routes.login import login_route

# init fflask app and config with database connection.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpassword@mysql:3306/mydatabase'

# init db instance with the current app context
db.init_app(app)
#create database models class defined
with app.app_context():
    db.create_all()

#join the API rout login
app.register_blueprint(login_route)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)