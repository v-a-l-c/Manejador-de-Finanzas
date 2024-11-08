from . import db
from sqlalchemy.orm import relationship

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(10), unique=True, nullable=False)

    # borrer relaiones pq causaban problemas

    def __repr__(self):
        return f'<Tag {self.tag_name}>'
