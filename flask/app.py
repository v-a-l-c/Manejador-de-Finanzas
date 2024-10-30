from flask import Flask
from db_config import db
from routes.logging import log

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Xd310703@db/test_db'
db.init_app(app)
   
log(app)


if __name__ == "main":
    app.run(debug=True);
