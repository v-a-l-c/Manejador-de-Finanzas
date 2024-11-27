from bussines.wallet import Wallet
class Graph(Wallet):

    def __init__(self, user_id):
        self.user_id = user_id

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
