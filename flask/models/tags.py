from . import db
from sqlalchemy.orm import relationship
from .tag_associations import transaction_tag

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(10), unique=True, nullable=False)
    registros = relationship('Registro', secondary=transaction_tag, back_populates='tags')

    def __repr__(self):
        return f'<Tag {self.tag_name}>'