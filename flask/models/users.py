from . import db

class Usuarios(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    authenticated = db.Column(db.Boolean, nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)

    def get_password_hash(self):
        return password_hash
    
    def username(self):
        return username

    def __repr__(self):
        return f'<Usuario {self.username}>'