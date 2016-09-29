#-*- encoding: utf-8 -*-
from poplib import POP3_SSL
import os, email, smtplib, pickle, time
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# engine = create_engine('mysql+mysqlconnector://root:12518ll+.@localhost:3306/test1')
# db = sessionmaker(bind=engine)
# session = db()

pop3server = 'pop.126.com'
smtpserver = 'smtp.gmail.com'

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
	revcSer.close()
	time.sleep(300)

class Student(Base):
	__tablename__ = 'student_email'
	student_number = Column(String(10), primary_key=True,unique=True)
	name = Column(String(64))

def main():
	while True:
		f = open('record.txt', 'rb')
		record_list = pickle.load(f)
		f.close()
		revcSer = POP3_SSL(pop3server)
		revcSer.user('nkjz2016@126.com') 
		revcSer.pass_('nkjz2016')
		num,total_size = revcSer.stat()
		while True:
			f = open('record.txt', 'rb')
			record_list = pickle.load(f)
			f.close()
			hdr,text,octet=revcSer.retr(num)
			full_mail = map(bytes.decode, text)
			content = '\n'.join(full_mail)
			msg = email.message_from_string(content)
			smtpObj = smtplib.SMTP('smtp.gmail.com',587)
			smtpObj.starttls()
			smtpObj.login('m.linearalgebra@gmail.com','vottkcjbaheqzgiw')
			if msg.get('Message-ID') in record_list:
				print('没有新邮件！' + time.strftime('%H:%M',time.localtime()))
				break
			else:
				engine = create_engine('mysql://root:12518ll+.@localhost:3306/test1')
				db = sessionmaker(bind=engine)
				session = db()
				student = session.query(Student).all()
				mail_list = list(map(lambda x:x.name, student))
				session.close()
				smtpObj.sendmail('m.linearalgebra@gmail.com',mail_list,msg.as_string())
				record_list.append(msg.get('Message-ID'))
				num -= 1
				f = open('record.txt', 'wb')
				pickle.dump(record_list, f)
				f.close()
				dh = email.header.decode_header(msg.get('subject'))
				my_subject = dh[0][0].decode(dh[0][1])
				print('新邮件已发送' + my_subject + time.strftime('%H:%M',time.localtime()))
				time.sleep(1000)
		revcSer.close()
		smtpObj.quit()
		time.sleep(1000)

if __name__=='__main__':
	while True:
		try:
			main()
		except BaseException as e:
			print('获取失败，进入冷却')
			print(e)
			time.sleep(1000)