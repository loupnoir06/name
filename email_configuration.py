import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# Email configuration
def send_mail(gmail, code):
    sender_email = 'azizjona089@gmail.com'
    reciever_email = gmail
    subject = 'Akount aktivatsiya kodi.'
    message = f'Sizning aktivatsiya kodingiz: {code} \nUshbu kodni xech kimga bermang. Xattoki, bizning xodimlarga ham'
    # SMTP server configuration for gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'azizjona089@gmail.com'
    smtp_password = 'ycndbqnrolbceprr'
    # Create a multipart message and set headers
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = reciever_email
    email_message['Subject'] = subject
    email_message.attach(MIMEText(message, 'plain'))
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(email_message)

#Generate code
def generate_code():
    s=str(random.randint(1000, 9999))
    return s