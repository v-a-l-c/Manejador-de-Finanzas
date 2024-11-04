from . import db

class Usuarios(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Especifica el tamaño para password_hash
    authenticated = db.Column(db.Boolean, nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)

    def get_password_hash(self):
        return self.password_hash
    
    def get_username(self):
        return self.username

    def __repr__(self):
        return f'<Usuario {self.username}>'
