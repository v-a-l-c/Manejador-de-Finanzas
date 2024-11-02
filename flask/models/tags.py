from . import db

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.tag_name}>'