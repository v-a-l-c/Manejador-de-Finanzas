from flask import request
from models.user import User
from db_config import db

def log(app):
    
    @app.route('/login', methods = ['GET', 'POST'])
    def log_user():
        if request.method == 'GET':
            return "test get route"
        else:
            return "other case"
        
        
    
