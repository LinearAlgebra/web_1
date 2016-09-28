#-*- encoding: utf-8 -*-
from poplib import POP3_SSL
import os, email, smtplib, pickle, time
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine('mysql+mysqlconnector://root:12518ll+.@localhost:3306/test1')
# db = sessionmaker(bind=engine)
# session = db()

pop3server = 'pop.126.com'
smtpserver = 'smtp.126.com'

revcSer = POP3_SSL(pop3server)
# revcSer.starttls()
revcSer.user('nkjz2016@126.com')  
revcSer.pass_('nkjz2016')

num,total_size = revcSer.stat()

dir_list = os.listdir('./')
if 'record.txt' not in dir_list:
	record_list = []
	for i in range(num):
		hdr,text,octet=revcSer.retr(i+1)
		full_mail = map(bytes.decode, text)
		content = '\n'.join(full_mail)
		msg = email.message_from_string(content)
		record_list.append(msg.get('Message-ID'))
		f = open('record.txt', 'wb')
		pickle.dump(record_list, f)
		f.close()
	time.sleep(300)
while True:
	f = open('record.txt', 'rb')
	record_list = pickle.load(f)
	f.close()
	num,total_size = revcSer.stat()
	while True:
		hdr,text,octet=revcSer.retr(num)
		full_mail = map(bytes.decode, text)
		content = '\n'.join(full_mail)
		msg = email.message_from_string(content)
		smtpObj = smtplib.SMTP(smtpserver)
		smtpObj.login('nkjz2016@126.com','nkjz2016')
		if msg.get('Message-ID') in record_list:
			break
		else:
			engine = create_engine('mysql+mysqlconnector://root:12518ll+.@localhost:3306/test1')
			db = sessionmaker(bind=engine)
			session = db()
			student = session.query(Student).all()
			print(student)
			smtpObj.sendmail('nkjz2016@126.com',['412313393@qq.com','814453212@qq.com'],msg.as_string())
			record_list.append(msg.get('Message-ID'))
			num -= 1
	smtpObj.quit()
	f = open('record.txt', 'wb')
	pickle.dump(record_list, f)
	f.close()
	time.sleep(300)

class Student(db.Model):
	__tablename__ = 'student_email'
	student_number = Column(String(10), primary_key=True,unique=True)
	name = Column(String(64))
