from flask import Flask
from flask_restful import Resource, Api
from  models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpassword@mysql:3306/mydatabase'

# init db instance with the current app context
db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)