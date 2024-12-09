from fpdf import FPDF


class PDFreport:

    def __init__(self):
        pdf = FPDF(orientation = 'P', unit= 'mm', format='A4')
        pdf.add_page()
        self.pdf = pdf
    
    #title and date
    def headers(self):
        pass
    
    #incomes and expenses table
    def tables_content(self):
        pass

    #balance table
    def balance_content(self):
        pass
    
    def generate_pdf(self):
        self.pdf.output('balance_report.pdf')
    