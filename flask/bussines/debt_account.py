from bussines.wallet import Wallet
from models.debts import Debts
from models.interests import Interests
from models.transactions import Transactions
from models.tags import Tags
from models import db
from datetime import datetime, time, date

class DebtAccount:

    def __init__(self, wallet):
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
        self.update_amount(new_debt.id)
    
    def calc_payments(self, current_interest, amount, date):
        show_calcs = {}
        month_position = {
            1: "01", 2: "02", 3: "03",
            4: "04", 5: "05", 6: "06", 7: "07",
            8: "08", 9: "09", 10: "10",
            11: "11", 12: "12" 
        }
        cont = 1
        current_date = date.today()
        between_months = (date.year - current_date.year)*12 + date.month - current_date.month 
        amount_total = (float(current_interest)*float(amount)) + float(amount)
        amount = float(amount_total/between_months)
        current_month = current_date.month + 1
        current_year = current_date.year

        for month in range(1, between_months + 1):

            if current_month > 12:
                current_month = 1
                current_year += 1

            show_calcs[cont] = {
                "date": str(current_year) +"-"+ month_position[current_month]+"-"+str(date.day),
                "calc_amount": round(amount, 2)
            }
            current_month += 1
            cont +=1
        show_calcs[cont + 1] = {"total_to_pay": round(amount_total, 2)}
        return show_calcs

    def response_data(self, stmt_query_debt):
        show_data = {}
        cont = 1
        for row in stmt_query_debt:
            show_data[cont] = {
                "amount": row.amount, 
                "interest": row.percent, 
                "creditor": row.creditor,
                "end_of_date": row.date,
                "payments": self.calc_payments(row.percent, row.amount, row.date)}
            cont += 1
        return show_data


    def pop_debt(self, debt_id):
        db.session.execute(
            db.update(Transactions)
            .where(Transactions.user_id == self.wallet.get_wallet_id()).where(Transactions.id == Debts.transaction_id).where(Debts.id == debt_id).values(type_id= 2))
        db.session.commit()
        Debts.query.filter(Debts.id == debt_id).delete()
        db.session.commit()

    #remind me whom i will pay
    def date_status(self, debt_id):
        show_data = {}
        stmt_record = db.session.execute(db.select(Debts.creditor, Transactions.amount)
        .join(Transactions, Debts.transaction_id == Transactions.id)
        .where(Transactions.user_id == self.wallet.get_wallet_id()).where(Debts.id == debt_id)).all()
        for row in stmt_record:
            show_data = {
                "creditor": row.creditor,
                "amount_to_pay": row.amount
            }
        return show_data

    #func to calcute amount with the interest, default by month
    def calc_interest(self, debt_id):
        creditor_interest_value = db.session.execute(db.select(Debts.creditor, Transactions.amount, Transactions.date, Interests.percent)
        .join(Debts, Debts.interest_id ==  Interests.id).join(Transactions, Debts.transaction_id == Transactions.id)
        .where(Debts.id == debt_id)).all()
        return self.response_data(creditor_interest_value)

    def update_amount(self, debt_id):
        new_amount = 0
        interest = 0
        stmt_query = db.session.execute(
            db.select(Transactions.amount, Interests.percent)
            .join(Debts, Debts.transaction_id == Transactions.id)
            .join(Interests, Debts.interest_id == Interests.id)
            .where(Transactions.user_id == self.wallet.get_wallet_id())
            .where(Debts.id == debt_id)
        )
        for row in stmt_query:
            interest = row.percent
            new_amount = row.amount

        new_amount = float(new_amount)*float(interest) + float(new_amount)
        new_amount = round(new_amount, 2)
        self.update_amount_interest(new_amount, debt_id)
            

    def update_amount_interest(self, new_amount, debt_id):
        db.session.execute(
            db.update(Transactions).where(Transactions.user_id == self.wallet.get_wallet_id()).where(Transactions.id == Debts.transaction_id)
            .where(Debts.id == debt_id)
            .values(amount=new_amount)
        )
        db.session.commit()

    def get_all_debts(self, type_id):
        current_transactions = db.session.execute(
            db.select(Debts, Transactions.amount, Transactions.description, Transactions.date, Tags.tag_name)
            .filter(Transactions.user_id == self.wallet.get_wallet_id())
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