# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, redirect, url_for
from flask_script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Length
from flask_script import Manager
import time

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)
# print(dir(db))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12518ll+.@localhost/test1'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'EASY TO GUESS'

@app.route('/', methods=['GET', 'POST'])
def index():
	# db.session.rollback()
	form = InformationForm()
	if form.validate_on_submit():
		try:
			student = Student.query.filter_by(StuID=form.StuID.data).first()
		except:
			student = Student.query.filter_by(StuID=form.StuID.data).first()
		student_1 = Student(StuID=form.StuID.data,
							StuName=form.name.data,
							First=form.First.data,
							stime = time.strftime("%Y-%m-%d %H:%M:%S"))
		if student is None:
			try:
				db.session.add(student_1)
			except:
				db.session.add(student_1)
			flash('信息录入成功','alert alert-success')
			return render_template('select_daoshi.html', form=form)
		else:
			if student.StuName == student_1.StuName and student.First == student_1.First:
				flash('该学号已登记，登记时间为%s，你此次输入的信息与数据库中保存的信息相符' % student.stime, 'alert alert-success')
			else:
				flash('该学号已登记，登记时间%s, 并且你此次输入的信息与数据库保存的信息不符。如需更改登记信息请微信联系管理员，或用本人南开邮箱发送邮件至2120162310@mail.nankai.edu.cn' % student.stime, 'alert alert-danger')
			# db.session.rollback()
			return render_template('select_daoshi.html', form=form)
	flash('这是一个用来统计《商品投资》模拟期货账户的页面，不要填错~另外登记成功会有提示，没有提示要再输一遍', 'alert alert-info')
	return render_template('select_daoshi.html', form=form)

@app.errorhandler(500)
def handle_500(e):
	db.session.rollback()
	flash('信息录入失败，请重新录入','alert alert-danger')
	return redirect(url_for('index'))

# @app.errorhandler()
# def handle_500(e):
# 	db.session.rollback()
# 	flash('信息录入失败，请重新录入','alert alert-danger')
# 	return redirect(url_for('index'))

class InformationForm(Form):
	StuID = StringField("请输入学号:", validators=[Length(10)])
	name = StringField("请输入姓名:", validators=[Required()])
	First = StringField("模拟账户帐号:", validators=[Required()])
	submit = SubmitField("提交")

class Student(db.Model):
	__tablename__ = 'qihuo'
	StuID = db.Column(db.String(10), primary_key=True,unique=True)
	StuName = db.Column(db.String(6))
	First = db.Column(db.String(20))
	stime = db.Column(db.String(25))


	def __repr__(self):
		return '<Student %r>' % self.StuName+self.First


if __name__ == '__main__':
	db.create_all()
	app.run(host='0.0.0.0',port=8877,threaded=True)
