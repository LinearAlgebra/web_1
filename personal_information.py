# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Length
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
	form_1 in xrange(1,10):
		passm_1 = QueryForm()
	if form.validate_on_submit():
		student = Student.query.filter_by(student_number=form.student_number.data).first()
		if student is None:
			student = Student(student_number=form.student_number.data,name=form.name.data)
			detail = Detail_Info(phone_number=form.phone_number.data,identity=student)
			db.session.add_all([student,detail])
			db.session.commit()
			return render_template('personal_information.html', form=form, form_1=form_1, data=['学号信息录入成功，如需更改请联系管理员。 xietaitong@163.com'])
			session['known'] = False
		else:
			return render_template('personal_information.html', form=form, data=['学号被占用，占用人信息:'] + [student.name] + ['如有需要请联系管理员 xietaitong@163.com'])
	if form_1.validate_on_submit():
		student_data = Student.query.join(Detail_Info.phone_number).filter_by(student_number=form.student_number.data).first().phone_number
		return render_template('personal_information.html', form=form, form_1=form_1, data=[student_data])
	return render_template('personal_information.html', form=form)

class InformationForm(Form):
	student_number = StringField("请输入学号:", validators=[Length(10)])
	name = StringField("请输入姓名:", validators=[Required()])
	phone_number = StringField("请输入电话号码:", validators=[Length(11)])
	submit = SubmitField("提交")

class QueryForm(Form):
	name_query = StringField("\n请输入姓名:", validators=[Required()])
	search = SubmitField("查询")

class Student(db.Model):
	__tablename__ = 'students'
	student_number = db.Column(db.String(10), primary_key=True,unique=True)
	name = db.Column(db.String(64))
	identity = db.relationship('Detail_Info', backref='identity')

	def __repr__(self):
		return '<Student %r>' % self.name

class Detail_Info(db.Model):
	__tablename__ = 'detail_info'
	student_number = db.Column(db.String(10), db.ForeignKey('students.student_number'),primary_key=True,unique=True)
	phone_number = db.Column(db.String(11))

	def __repr__(self):
		return '<Phonenumber %r>' % self.phonenumber

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8422)