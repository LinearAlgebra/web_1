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
		student = Student.query.filter_by(id=form.id_1.data).first()
		student_1 = Student(id=form.id_1.data,
							name=form.name.data,
							daoshi_1=form.daoshi_1.data,
							daoshi_2=form.daoshi_2.data,
							daoshi_3=form.daoshi_3.data,
							phone = form.phone.data,
							stime = time.strftime("%Y-%m-%d %H:%M:%S"))
		if student is None:
			db.session.add(student_1)
			try:
				pass
			except:
				flash('信息录入失败，请重新录入','alert alert-danger')
				db.session.rollback()
				return render_template('select_daoshi.html', form=form)
			flash('信息录入成功','alert alert-success')
			return render_template('select_daoshi.html', form=form)
		else:
			if student.name == student_1.name and [student.daoshi_1,student.daoshi_2,student.daoshi_3] == [student_1.daoshi_1,student_1.daoshi_2,student_1.daoshi_3] and student.phone==student_1.phone:
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
	id_1 = StringField("请输入学号:", validators=[Length(10)])
	name = StringField("请输入姓名:", validators=[Required()])
	daoshi_1 = StringField("请输入一志愿导师:", validators=[Required()])
	daoshi_2 = StringField("请输入二志愿导师:", validators=[Required()])
	daoshi_3 = StringField("请输入三志愿导师:", validators=[Required()])
	phone = StringField("请输入个人手机号:", validators=[Length(11)])
	submit = SubmitField("提交")

class Student(db.Model):
	__tablename__ = 'daoshi'
	id = db.Column(db.String(10), primary_key=True,unique=True)
	name = db.Column(db.String(6))
	daoshi_1 = db.Column(db.String(6))
	daoshi_2 = db.Column(db.String(6))
	daoshi_3 = db.Column(db.String(6))
	phone = db.Column(db.String(11))
	stime = db.Column(db.String(25))


	def __repr__(self):
		return '<Student %r>' % self.name+self.daoshi_1+self.daoshi_2+self.daoshi_3


if __name__ == '__main__':
	# db.create_all()
	app.run(host='0.0.0.0',port=8890)
