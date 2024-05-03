from logging.handlers import SMTPHandler
import smtplib
from email.message import EmailMessage
from email.utils import localtime

class SSLSMTPHandler(SMTPHandler):
    def emit(self, record):
        try:
            with smtplib.SMTP_SSL(self.mailhost, self.mailport) as smtp:
                smtp.login(self.username, self.password)
                msg = self.format_email(record)
                smtp.send_message(msg)
        except Exception:
            self.handleError(record)

    def format_email(self, record):
        msg = EmailMessage()
        msg['From'] = self.username
        msg['To'] = ','.join(self.toaddrs)
        msg['Subject'] = self.getSubject(record)
        msg['Date'] = localtime()
        msg.set_content(self.format(record))
        return msg
