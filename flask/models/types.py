from . import db

class Types(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.type_name}>'