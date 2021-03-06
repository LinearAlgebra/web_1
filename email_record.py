# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash
from flask_script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Length, Email
from flask_script import Manager

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12518ll+.@localhost/test1'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'EASY TO GUESS'

@app.route('/', methods=['GET', 'POST'])
def index():
	form = InformationForm()
	form_1 = QueryForm()
	if form.validate_on_submit():
		student = Student.query.filter_by(student_number=form.student_number.data).first()
		students = Student(student_number=form.student_number.data,name=form.name.data)
		if student is None:
			db.session.add(students)
			flash('邮箱信息录入成功')
			return render_template('mail_record.html', form=form, form_1=form_1)
			session['known'] = False
		else:
			db.session.merge(students)
			db.session.commit()
			flash('邮箱信息已更新')
			return render_template('mail_record.html', form=form, form_1=form_1)
	if form_1.validate_on_submit():
		# students_ = Student(student_number=form_1.student_number_.data,name=form_1.name_.data)
		query_ans = Student.query.filter_by(student_number=form_1.student_number_.data,name=form_1.name_.data).first()
		if query_ans:
			db.session.delete(query_ans)
			db.session.commit()
			flash('邮箱信息已移除')
		else:
			flash('查无此人，请检查信息是否正确')
		return render_template('mail_record.html', form=form, form_1=form_1)
	return render_template('mail_record.html', form=form, form_1=form_1)

class InformationForm(Form):
	student_number = StringField("请输入学号:", validators=[Length(10)])
	name = StringField("请输入邮箱:", validators=[Email()])
	submit = SubmitField("提交邮箱信息")

class QueryForm(Form):
	student_number_ = StringField("请输入学号:", validators=[Length(10)])
	name_ = StringField("请输入姓名:", validators=[Email()])
	submit = SubmitField("不愿继续接受邮件，在邮件列表中删除邮箱")

class Student(db.Model):
	__tablename__ = 'student_email'
	student_number = db.Column(db.String(10), primary_key=True,unique=True)
	name = db.Column(db.String(64))

	def __repr__(self):
		return self.name

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8850,debug=True)
