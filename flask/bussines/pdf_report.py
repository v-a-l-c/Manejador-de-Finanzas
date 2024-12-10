from fpdf import FPDF
from datetime import datetime


class PDFreport(FPDF):

    def __init__(self):
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

    #incomes and expenses table
    def tables_content(self):
        pass

    #balance table
    def balance_content(self):
        pass

    def generate_pdf(self):
        self.pdf.output('balance_report.pdf')
