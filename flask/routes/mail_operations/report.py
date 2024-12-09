from flask import Blueprint, make_response, jsonify, send_file, current_app
from routes.sessions import current_session
from bussines.mail import Mail
from flask_mail import Message
from models.users import Usuarios
from models import db
from routes.mail_operations.mail_corp import MailCorp

report  = Blueprint('report',__name__)

@report.route('/report-pdf', methods=['GET', 'POST'])
def download_report():
    #try:
    user_id = 1 #current_session.get('user_id')
    user_mail = db.session.execute(db.select(Usuarios.mail).where(Usuarios.id == user_id)).scalar()
    if not user_mail:
        return jsonify({"message": "failed_success", "response": "user_not_found"}), 401
    mail = Mail(MailCorp.get_corp_mail(), user_mail)
    mail.send_mail("Incomes and expenses", "generic body")
    return jsonify({"message": "message_was_sent", "response": "success"}), 201
    #except Exception as e:
        #return jsonify({"message": "server_not_process_data", "response": str(e)}),499