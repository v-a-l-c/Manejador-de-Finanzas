from fpdf import FPDF
from datetime import datetime
from bussines.wallet import Wallet

class PDFreport(FPDF):

    def __init__(self):
        #self.wallet = wallet
        super().__init__(orientation='P', unit='mm', format='A4')
        self.add_page()

    #title and date
    def header(self):
        self.set_font('Times', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'Reporte Programado MonkeyApp', 0, 0, 'C')
        self.ln(10)
        self.set_font('Times', '', 11)
        self.cell(0, 10, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 1, 'R')
        self.ln(10)

    #incomes table
    def table_incomes(self):
        self.ln(10)
        #data = current_wallet.get_all_transactions(0)
        self.set_font('Times', '', 12)
        self.cell(0, 10, 'Ingresos:', 0, 1, 'L')
        self.ln(5)
        self.set_font('Times', 'B', 12)
        self.cell(40, 10, 'Rubro', 1, 0, 'C')
        self.cell(40, 10, 'Monto', 1, 0, 'C')
        self.cell(40, 10, 'Fecha', 1, 0, 'C')
        self.cell(40, 10, 'Descripción', 1, 1, 'C')
        self.set_font('Times', '', 12)
        data = [
            ('Rubro1', "$150.00", "2024-12-10", "Lorem ipsum"),
            ("Rubro2", "$200.00", "2024-12-11", "Otra descripción"),
        ]
        if not data:
            self.cell(0, 10, 'No hay ingresos registrados.', 1, 1, 'C')
            return
        for income in data:
            self.cell(40, 10, income["category"], 1, 0, 'C')
            self.cell(40, 10, f'${income["amount"]}', 1, 0, 'R')
            self.cell(40, 10, income["date"], 1, 0, 'C')
            self.multi_cell(40, 10, income["description"], 1)

    #expenses table
    def table_expenses(self):
        ##data = current_wallet.get_all_transactions(1)
        self.ln(5)
        self.set_font('Times', '', 12)
        self.cell(0, 10, 'Egresos:', 0, 1, 'L')
        self.ln(5)
        self.set_font('Times', 'B', 12)
        self.cell(40, 10, 'Rubro', 1, 0, 'C')
        self.cell(40, 10, 'Monto', 1, 0, 'C')
        self.cell(40, 10, 'Fecha', 1, 0, 'C')
        self.cell(40, 10, 'Descripción', 1, 1, 'C')
        self.set_font('Times', '', 12)
        #if not data:
            #self.cell(0, 10, 'No hay egresos registrados.', 1, 1, 'C')
            #return
        #for income in data:
            #self.cell(40, 10, income["category"], 1, 0, 'C')
            #self.cell(40, 10, f'${income["amount"]}', 1, 0, 'R')
            #self.cell(40, 10, income["date"], 1, 0, 'C')
            #self.multi_cell(40, 10, income["description"], 1)

    #balance table
    def balance_content(self):
        self.ln(10)
        self.set_font('Times', '', 12)
        self.cell(0, 10, 'Balance General:', 0, 1, 'L')
        self.ln(5)
        self.set_font('Times', 'B', 12)
        self.cell(50, 10, 'Descripción', 1, 0, 'C')
        self.cell(50, 10, 'Monto', 1, 1, 'C')
        self.set_font('Times', '', 12)
        self.cell(50, 10, 'Ingresos Totales', 1, 0, 'L')
        self.cell(50, 10, '$1000.00', 1, 1, 'R')
        self.cell(50, 10, 'Egresos Totales', 1, 0, 'L')
        self.cell(50, 10, '$500.00', 1, 1, 'R')
        self.cell(50, 10, 'Balance Final', 1, 0, 'L')
        self.cell(50, 10, '$500.00', 1, 1, 'R')
        pass

    def generate_pdf(self):
        console.log("Generating pdf...")
        self.table_incomes()
        self.table_expenses()
        self.balance_content()
        self.output('balance_report.pdf')
