from bussines.wallet import Wallet
from models.debts import Debts
from models.interests import Interests
from models import db

class DebtAccount:

    def __init__(self, user_id, wallet):
        self.user_id = user_id
        self.wallet = wallet
        self.debt_id = 0
    
    def set_debt_id(self, debt_id):
        self.debt_id = debt_id

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
        self.set_debt_id(new_debt.id)

    def pop_debt(self, debt_id, transaction_id):
        pass

    def date_status(self, debt_id):
        pass
    
    def calc_interest(self):
        pass

    def send_end_date(self):
        pass
    
    def get_all_debts(self, type_id):
        return self.wallet.get_all_transactions(type_id)