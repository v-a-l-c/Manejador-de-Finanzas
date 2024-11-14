from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for

mail = Mail()
serializer = URLSafeTimedSerializer('your-secret-key')

def send_confirmation_email(user_email):
    token = serializer.dumps(user_email, salt='email-confirm')
    confirm_url = url_for('confirm_email.confirm_email', token=token, _external=True)
    msg = Message(
        subject="Confirm your email",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user_email]
    )
    msg.body = f"Please click the link to confirm your email: {confirm_url}"
    mail.send(msg)
