from models import db
from models.users import Usuarios
from models.transactions import Transactions

"""Create a new wallet from the current user. post and put incomes filter by day, month, year to show
The class only has a logic personal wallet, to insert and show the amount registered. """

class Wallet:
    
    def __init__(self, user_id):
        self.user_id = user_id
    
    def insert_amount(self, amount, description, date):

        new_transaction = Transactions(
            user_id= self.user_id, 
            type_id=1, 
            amount= amount, 
            description=description,
            date=date)

        db.session.add(new_transaction)
        db.session.commit()
    
    def get_amount_per_day(self, date):
        pass
    
    def get_amount_per_month(self, data):
        pass
    
    def get_amount_per_year(self, data):
        pass

        
