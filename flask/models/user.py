from db_config import db
"""Create a <code>User</code> class that use ORM pattern
to users table. This class indicate a database representation,
the reason we use <code>db.Model</code>"""

class User(db.Model):
    """Define the main columns schema to create the table"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String, nullable=False, unique=True)
    authenticated = db.Column(db.Boolean)
    mail = db.Column(db.String)

    def __init__(self, password_hash, authenticated, mail):
        self.password_hash = password_hash
        self.authenticated = authenticated
        self.mail = mail
