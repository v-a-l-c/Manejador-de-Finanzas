from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    authenticated = db.Column(db.Boolean, nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)

    #Modificables por el usuario:
    firstName = db.Column(db.String(50), nullable=True)
    secondNames = db.Column(db.String(70), nullable=True)
    curp = db.Column(db.String(18), nullable=True)
    rfc = db.Column(db.String(13), nullable=True)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_username(self, username):
        self.username = username

    def set_mail(self, mail):
        self.mail = mail

    def get_id(self):
        return self.id
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<Usuario {self.username}>'
