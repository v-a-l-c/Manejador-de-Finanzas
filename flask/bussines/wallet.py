from models import db
from models.users import Usuarios
from models.transactions import Transactions
from models.tags import Tags
from sqlalchemy import func
from datetime import datetime

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

    def delete_transaction(self, transaction_id):
        transaction_to_delete = Transactions.query.filter(
            Transactions.id == transaction_id,
        ).first()
        db.session.delete(transaction_to_delete)
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

    def get_all_transactions(self, type_id):
        current_transactions = db.session.execute(
            db.select(Transactions, Tags.tag_name)
            .filter(Transactions.user_id == self.user_id)
            .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
        ).all()

        return [
            {
                "amount": transaction.amount,
                "description": transaction.description,
                "category": tag_name,
                "date": transaction.date,
                "id": transaction.id,
            }
            for transaction, tag_name in current_transactions
        ]
    def search_transaction(self, date, type_of_date, tag, type_id):
        dates_transaction = {
            "day": self.get_amount_per_day(date, type_id),
            "week": self.get_amount_per_week(date, type_id),
            "month": self.get_amount_per_month(date, type_id),
            "year": self.get_amount_per_year(date, type_id)
        }
        if not type_of_date and tag:
            current_transaction = db.session.execute(
                db.select(Transactions.amount, Transactions.description, Transactions.date, Tags.tag_name)
                .filter(Transactions.user_id == self.user_id)
                .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
                .filter(Tags.tag_name == tag)
            )
            return self.response_data(current_transaction)

        elif not tag and type_of_date:
            return dates_transaction[type_of_date]
        else:
            if type_of_date == "day":
                current_transaction = db.session.execute(
                db.select(
                    Transactions.amount,
                    Transactions.description,
                    Transactions.date,
                    Tags.tag_name
                )
                .filter(Transactions.user_id == self.user_id)
                .filter(Transactions.date == date)
                .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
                .filter(Tags.tag_name == tag)
                ).all()
            elif type_of_date == "week":
                current_transaction = db.session.execute(
                db.select(
                    Transactions.amount,
                    Transactions.description,
                    Transactions.date,
                    Tags.tag_name
                )
                .filter(Transactions.user_id == self.user_id)
                .filter(func.week(Transactions.date) == func.week(date))
                .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
                .filter(Tags.tag_name == tag)
                ).all()
            elif type_of_date == "month":
                current_transaction = db.session.execute(
                db.select(
                    Transactions.amount,
                    Transactions.description,
                    Transactions.date,
                    Tags.tag_name
                )
                .filter(Transactions.user_id == self.user_id)
                .filter(func.month(Transactions.date) == func.month(date))
                .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
                .filter(Tags.tag_name == tag)
                ).all()
            elif type_of_date == "year":
                current_transaction = db.session.execute(
                db.select(
                    Transactions.amount,
                    Transactions.description,
                    Transactions.date,
                    Tags.tag_name
                )
                .filter(Transactions.user_id == self.user_id)
                .filter(func.year(Transactions.date) == func.year(date))
                .filter(Transactions.type_id == type_id).join(Tags).filter(Transactions.tag_id == Tags.id)
                .filter(Tags.tag_name == tag)
                ).all()
            return self.response_data(current_transaction)
