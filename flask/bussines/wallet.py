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
    
    def response_data(self, current_amount):
        show_data = {}
        cont = 1
        total = 0
        for row in current_amount:
            show_data[cont] = {"amount": row.amount, "description": row.description, "date": row.date}
            cont += 1
            total += float(row.amount)
        show_data[0] = {"total": str(total)}
        return show_data

    def get_amount_per_day(self, date, type_id):
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date)
            .filter(Usuarios.id == self.user_id)
            .filter(Transactions.date == date)
            .filter(Transactions.type_id == type_id)
        )
        return self.response_data(current_amount)

    def get_amount_per_month(self, date, type_id):
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date)
            .filter(Usuarios.id == self.user_id)
            .filter(func.month(Transactions.date) == func.month(date))
            .filter(func.year(Transactions.date) == func.year(date))
            .filter(Transactions.type_id == type_id)
        )
        return self.response_data(current_amount)

    def get_amount_per_year(self, date, type_id):
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date)
            .filter(Usuarios.id == self.user_id)
            .filter(func.year(Transactions.date) == func.year(date))
            .filter(Transactions.type_id == type_id)
        )
        return self.response_data(current_amount)
    
    def get_amount_per_week(self, date, type_id):
        current_amount = db.session.execute(
            db.select(Usuarios, Transactions.amount, Transactions.description, Transactions.date)
            .filter(Usuarios.id == self.user_id)
            .filter(func.week(Transactions.date) == func.week(date))
            .filter(Transactions.type_id == type_id)
        )
        return self.response_data(current_amount)

    def get_all_incomes(self):
        current_incomes = db.session.execute(
            db.select(Transactions)
            .filter(Transactions.user_id == self.user_id)
            .filter(Transactions.type_id == 1) 
        ).scalars().all()

        return [
            {
                "amount": income.amount,
                "description": income.description,
                "date": income.date,
                "id": income.id,
            }
            for income in current_incomes
        ]

    def get_all_expenses(self):
        current_expenses = db.session.execute(
            db.select(Transactions)
            .filter(Transactions.user_id == self.user_id)
            .filter(Transactions.type_id == 2)  
        ).scalars().all()

        return [
            {
                "amount": expense.amount,
                "description": expense.description,
                "date": expense.date,
                "id": expense.id,
            }
            for expense in current_expenses
        ]

    def get_all_expenses_period(self, timespan):
        current_expenses = db.session.execute(
            db.select(Transactions)
            .filter(Transactions.user_id == self.user_id)
            .filter(Transactions.type_id == 2)  
        ).scalars().all()

        expenses_by_period = defaultdict(float)

        for expense in current_expenses:
            expense_date = expense.date
            period_key = self.get_period_key(expense_date, timespan)  

            expenses_by_period[period_key] += expense.amount

        return [{"period": period, "total": total} for period, total in expenses_by_period.items()]

    def get_period_key(self, date, timespan):
        """
        Calcula la clave del período (día, mes, año, etc.) para la fecha del gasto.
        :param date: Fecha del gasto
        :param timespan: El período por el que agrupar (día, mes, año, etc.)
        :return: Clave del período (formato: día, mes, año)
        """
        if timespan == "day":
            return date.strftime('%Y-%m-%d')  
        elif timespan == "month":
            return date.strftime('%Y-%m')  
        elif timespan == "year":
            return date.strftime('%Y')
        elif timespan == "half":
            day = date.day
            if day <= 15:
                return f"{date.year}-{date.month:02d}-01-15"
            else:
                return f"{date.year}-{date.month:02d}-16-31"
        return None