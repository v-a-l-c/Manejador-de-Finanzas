from bussines.wallet import Wallet
from models.debts import Debts
from models.interests import Interests
from models.transactions import Transactions
from models.tags import Tags
from models import db

class DebtAccount:

    def __init__(self, user_id, wallet):
        self.user_id = user_id
        self.wallet = wallet

    def register_debt(self, creditor, amount, description, date, type_id, tag, interest):
        transaction_id_ = self.wallet.insert_amount(amount, description, date, type_id, tag)
        calc_interest = Interests.query.filter(Interests.percent == interest).scalar()
        calc_interest = calc_interest or Interests(percent=interest)
        db.session.add(calc_interest)
        db.session.commit()

        new_debt = Debts(
            transaction_id= transaction_id_,
            interest_id= calc_interest.id,
            creditor=creditor
        )
        db.session.add(new_debt)
        db.session.commit()

    def pop_debt(self, debt_id):
        db.session.execute(
            db.update(Transactions)
            .where(Transactions.user_id == self.user_id).where(Transactions.id == Debts.transaction_id).where(Debts.id == debt_id).values(type_id= 2))
        db.session.commit()
        Debts.query.filter(Debts.id == debt_id).delete()
        db.session.commit()

    def date_status(self):
        pass
    #func to calcute amount with the interest, default by month
    def calc_interest(self):
        pass

    def send_end_date(self):
        pass
    
    def get_all_debts(self, type_id):
        current_transactions = db.session.execute(
            db.select(Debts, Transactions.amount, Transactions.description, Transactions.date, Tags.tag_name)
            .filter(Transactions.user_id == self.user_id)
            .filter(Transactions.type_id == type_id).join(Transactions, Debts.transaction_id == Transactions.id).join(Tags, Transactions.tag_id == Tags.id)
        ).all()

        return [
            {
                "amount": amount,
                "description": description,
                "category": tag_name,
                "creditor": debt.creditor,
                "date":date,
                "id": debt.id,
            }
            for debt, amount, description, date, tag_name in current_transactions
        ]