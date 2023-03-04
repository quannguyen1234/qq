from email.message import EmailMessage
import ssl
import  smtplib

sender='nhquan0911@gmail.com'


def send_email(receiver,subject,body):
    em=EmailMessage()
    em['From']=sender
    em['To']=receiver
    em['Subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender,"fyrndwbfbzhcdmhj")
        smtp.sendmail(sender,receiver,em.as_string())
    