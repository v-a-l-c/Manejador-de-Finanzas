from . import db

class Debts(db.Model):
    __tablename__ = 'debts'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'), nullable=False)
    creditor = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f'<Transacción {self.creditor}>'