import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conf import Gmail

class Email:
    def __init__(self):
        self._conf = Gmail()
        self.recipient_email = 'leonard@aps.holdings'

    def send_email(self,subject, body):

        msg = MIMEMultipart()
        msg['From'] = self._conf.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(self._conf.smtp_server, self._conf.port) as server:
            server.starttls()
            server.login(self._conf.sender_email, self._conf.password)
            text = msg.as_string()
            server.sendmail(self._conf.sender_email, self.recipient_email, text)