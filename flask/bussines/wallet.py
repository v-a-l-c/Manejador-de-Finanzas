from models import db
from models.users import Usuarios
from models.transactions import Transactions
from sqlalchemy import func
"""Create a new wallet from the current user. post and put incomes filter by day, month, year to show
The class only has a logic personal wallet, to insert and show the amount registered. """

class Wallet:
    def __init__(self, user_id):
        self.user_id = user_id

    def insert_amount(self, amount, description, date, type_id=1):
        new_transaction = Transactions(
            user_id=self.user_id,
            type_id=type_id,
            amount=amount,
            description=description,
            date=date
        )
        db.session.add(new_transaction)
        db.session.commit()

    def get_amount_per_day(self, date, type_id=1):
        show_data = {}
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date)
            .filter(Usuarios.id == self.user_id)
            .filter(Transactions.date == date)
            .filter(Transactions.type_id == type_id)
        )

        cont = 1
        total = 0
        for row in current_amount:
            show_data[cont] = {"amount": row.amount, "description": row.description, "date": row.date}
            cont += 1
            total += float(row.amount)
        show_data[0] = {"total": str(total)}
        return show_data

    def get_amount_per_month(self, date, type_id=1):
        show_data = {}
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date)
            .filter(Usuarios.id == self.user_id)
            .filter(func.month(Transactions.date) == func.month(date))
            .filter(func.year(Transactions.date) == func.year(date))
            .filter(Transactions.type_id == type_id)
        )

        cont = 1
        total = 0
        for row in current_amount:
            show_data[cont] = {"amount": row.amount, "description": row.description, "date": row.date}
            cont += 1
            total += float(row.amount)
        show_data[0] = {"total": str(total)}
        return show_data

    def get_amount_per_year(self, date, type_id=1):
        show_data = {}
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date)
            .filter(Usuarios.id == self.user_id)
            .filter(func.year(Transactions.date) == func.year(date))
            .filter(Transactions.type_id == type_id)
        )

        cont = 1
        total = 0
        for row in current_amount:
            show_data[cont] = {"amount": row.amount, "description": row.description, "date": row.date}
            cont += 1
            total += float(row.amount)
        show_data[0] = {"total": str(total)}
        return show_data
