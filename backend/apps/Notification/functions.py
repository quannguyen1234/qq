from email.message import EmailMessage
import ssl
import  smtplib
from abc import ABC,abstractmethod

sender='nhquan0911@gmail.com'

class Sender(ABC):
    
    @abstractmethod
    def sendMessage(self):
        pass

class Email(Sender):
    sender=""
    receiver=""
    subject=""
    body=""

    def sendMessage(self):
        em=EmailMessage()
        em['From']=self.sender
        em['To']=self.receiver
        em['Subject']=self.subject
        em.set_content(self.body)
        context=ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(sender,"fyrndwbfbzhcdmhj")
            smtp.sendmail(sender,self.receiver,em.as_string())


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


    