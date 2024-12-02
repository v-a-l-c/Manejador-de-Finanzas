from . import db
from sqlalchemy.orm import relationship

class Interests(db.Model):
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True)
    percent = db.Column(db.Float)

    def __repr__(self):
        return f'<Interest {self.percent}>'