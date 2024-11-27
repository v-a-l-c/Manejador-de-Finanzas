from models import db
from models.users import Usuarios
from models.transactions import Transactions
from models.tags import Tags
from sqlalchemy import func

"""Create a new wallet from the current user. post and put incomes filter by day, month, year to show
The class only has a logic personal wallet, to insert and show the amount registered. """

class Wallet:

    def __init__(self, user_id):
        self.user_id = user_id

    def insert_amount(self, amount, description, date, type_id, tag):
        current_tag = Tags.query.filter(Tags.tag_name==tag).scalar()
        new_tag = current_tag or Tags(tag_name=tag)
        db.session.add(new_tag)
        db.session.commit()  
        new_transaction = Transactions(
            user_id=self.user_id,
            type_id=type_id,
            tag_id= new_tag.id,
            amount=amount,
            description=description,
            date=date
        )
        db.session.add(new_transaction)
        db.session.commit()
    
    def response_data(self, current_amount):
        show_data = {}
        cont = 1
        total = 0
        for row in current_amount:
            show_data[cont] = {"amount": row.amount, "description": row.description, "date": row.date, "category": row.tag_name}
            cont += 1
            total += float(row.amount)
        show_data[0] = {"total": str(total)}
        return show_data

    def get_amount_per_day(self, date, type_id):
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date, Tags.tag_name)
            .filter(Usuarios.id == self.user_id)
            .filter(Transactions.date == date)
            .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
        )
        return self.response_data(current_amount)

    def get_amount_per_month(self, date, type_id):
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date, Tags.tag_name)
            .filter(Usuarios.id == self.user_id)
            .filter(func.month(Transactions.date) == func.month(date))
            .filter(func.year(Transactions.date) == func.year(date))
            .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
        )
        return self.response_data(current_amount)

    def get_amount_per_year(self, date, type_id):
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date, Tags.tag_name)
            .filter(Usuarios.id == self.user_id)
            .filter(func.year(Transactions.date) == func.year(date))
            .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
        )
        return self.response_data(current_amount)
    
    def get_amount_per_week(self, date, type_id):
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date, Tags.tag_name)
            .filter(Usuarios.id == self.user_id)
            .filter(func.week(Transactions.date) == func.week(date))
            .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
        )
        return self.response_data(current_amount)

    def get_all_incomes(self):
        current_incomes = db.session.execute(
            db.select(Transactions, Tags.tag_name)
            .filter(Transactions.user_id == self.user_id)
            .filter(Transactions.type_id == 1).join(Tags).filter(Transactions.tag_id == Tags.id)
        ).all()

        return [
            {
                "amount": income.amount,
                "description": income.description,
                "category": tag_name,
                "date": income.date,
                "id": income.id,
            }
            for income, tag_name in current_incomes
        ]

    def get_all_expenses(self):
        current_expenses = db.session.execute(
            db.select(Transactions, Tags.tag_name)
            .filter(Transactions.user_id == self.user_id)
            .filter(Transactions.type_id == 2).join(Tags).filter(Transactions.tag_id == Tags.id)  
        ).all()

        return [
            {
                "amount": expense.amount,
                "description": expense.description,
                "category": tag_name,
                "date": expense.date,
                "id": expense.id,
            }
            for expense, tag_name in current_expenses
        ]