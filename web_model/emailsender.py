import smtplib
from email.mime.text import MIMEText
from email.header import Header

class MailInput():
    def __init__(self):
        self.receiver = input('Please input receiver:')
        self.subject = input('Please input subject:')
        self.message = input('Please input message:')
        self.sender = '412313393@qq.com'

    def send(self):
        message = MIMEText(self.message, 'plain', 'utf-8')
        message['From'] = Header('谢泰彤', 'utf-8')
        message['To'] =  Header("YOU", 'utf-8')
        message['Subject'] = Header(self.subject, 'utf-8')
        smtpObj = smtplib.SMTP('smtp.qq.com',587)
        smtpObj.starttls()
        smtpObj.login('412313393@qq.com','xwxsxkestgedcajf')
        try:
            receiver = eval(self.receiver)
            for i in receiver:
                smtpObj.sendmail(self.sender, i, message.as_string())        
        except:
            smtpObj.sendmail(self.sender, self.receiver, message.as_string())
        finally:
            print('Email has been sent.')
            smtpObj.close()
            
        
class Mail():
    def __init__(self, receiver, subject, message):
        self.receiver = receiver
        self.subject = subject
        self.message = message
        self.sender = '412313393@qq.com'

    def send(self):
        message = MIMEText(self.message, 'plain', 'utf-8')
        message['From'] = Header('谢泰彤', 'utf-8')
        message['To'] =  Header("YOU", 'utf-8')
        message['Subject'] = Header(self.subject, 'utf-8')
        smtpObj = smtplib.SMTP('smtp.qq.com',587)
        smtpObj.starttls()
        smtpObj.login('412313393@qq.com','xwxsxkestgedcajf')
        if isinstance(self.receiver, list):
            for i in self.receiver:
                smtpObj.sendmail(self.sender, i, message.as_string())        
        else:
            smtpObj.sendmail(self.sender, self.receiver, message.as_string())
        print('Email has been sent.')
        smtpObj.close()

    def set_message(self, message):
        self.message = message
            
