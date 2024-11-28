from bussines.wallet import Wallet
from models.debts import Debts
class DebtAccount:

    def __init__(self, user_id, wallet):
        self.user_id = user_id
        self.wallet = wallet

    def register_debt(self):
        pass
    
    def pop_debt(self):
        pass
    
    def date_status(self):
        pass
    
    def calc_interest(self):
        pass

    def send_end_date(self):
        pass