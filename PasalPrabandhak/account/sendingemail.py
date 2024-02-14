import smtplib
from email.message import EmailMessage

def send_email(subject,to,emailmessage):
    EMAIL_ADDRESS = 'demoemailhw@gmail.com'
    EMAIL_PASSWORD = 'xpcqalgygmeyzalx'

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg.set_content(emailmessage)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
