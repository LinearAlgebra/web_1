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
		student = Student.query.filter_by(StuID=form.StuID.data).first()
		student_1 = Student(StuID=form.StuID.data,
							StuName=form.name.data,
							First=form.First.data,
							Second=form.Second.data,
							Third=form.Third.data,
							Phone = form.Phone.data,
							stime = time.strftime("%Y-%m-%d %H:%M:%S"))
		if student is None:
			try:
				db.session.add(student_1)
			except:
				flash('信息录入失败，请重新录入','alert alert-danger')
				db.session.rollback()
				return render_template('select_daoshi.html', form=form)
			flash('信息录入成功','alert alert-success')
			return render_template('select_daoshi.html', form=form)
		else:
			if student.StuName == student_1.StuName and [student.First,student.Second,student.Third] == [student_1.First,student_1.Second,student_1.Third] and student.Phone==student_1.Phone:
				flash('该学号已登记，登记时间为%s，你此次输入的信息与数据库中保存的信息相符' % student.stime, 'alert alert-success')
			else:
				flash('该学号已登记，登记时间%s, 并且你此次输入的信息与数据库保存的信息不符。如需更改登记信息请微信联系管理员，或用本人南开邮箱发送邮件至2120162310@mail.nankai.edu.cn' % student.stime, 'alert alert-danger')
			# db.session.rollback()
			return render_template('select_daoshi.html', form=form)
	flash('为了防止个人志愿被篡改，在本网页只能提交一次志愿。之后如需要更改，可直接通过微信或者通过南开邮箱联系我2120162310@mail.nankai.edu.cn（发件时请使用本人南开邮箱）','alert alert-info')
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
	First = StringField("请输入一志愿导师:", validators=[Required()])
	Second = StringField("请输入二志愿导师:", validators=[Required()])
	Third = StringField("请输入三志愿导师:", validators=[Required()])
	Phone = StringField("请输入个人手机号:", validators=[Length(11)])
	submit = SubmitField("提交")

class Student(db.Model):
	__tablename__ = 'daoshi'
	StuID = db.Column(db.String(10), primary_key=True,unique=True)
	StuName = db.Column(db.String(6))
	First = db.Column(db.String(6))
	Second = db.Column(db.String(6))
	Third = db.Column(db.String(6))
	Phone = db.Column(db.String(11))
	stime = db.Column(db.String(25))


	def __repr__(self):
		return '<Student %r>' % self.StuName+self.First+self.Second+self.Third


if __name__ == '__main__':
	# db.create_all()
	app.run(host='0.0.0.0',port=8888,threaded=True)