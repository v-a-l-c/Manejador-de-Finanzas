import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mail:

    def __init__(self, sender, reciever):
        self.sender = sender
        self.reciever = reciever
    

    def send_mail(self, subject, body):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, 'rnsc bogy cbsk rqfz')

        message = MIMEMultipart()

        message['from'] = self.sender
        message['To'] = self.reciever
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))
        server.sendmail(self.sender, self.reciever, message.as_string())

        server.quit()


