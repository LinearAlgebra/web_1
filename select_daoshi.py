# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12518ll+.@52.23.150.84/test1'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'EASY TO GUESS'

@app.route('/', methods=['GET', 'POST'])
def index():
	form = InformationForm()
	if form.validate_on_submit():
		student = Student.query.filter_by(id=form.id.data).first()
		students = Student(id=form.id.data,
							name=form.name.data,
							daoshi_1=form.daoshi_1.data,
							daoshi_2=form.daoshi_2.data,
							daoshi_3=form.daoshi_3.data,
							phone = form.phone.data)
		if student is None:
			db.session.add(students)
			db.session.commit()
			flash('信息录入成功','alert alert-success')
			return render_template('select_daoshi.html', form=form)
		else:
			db.session.rollback()
			flash('该学号已登记，如需更改请微信联系管理员', 'alert alert-success')
			return render_template('select_daoshi.html', form=form)
	return render_template('select_daoshi.html', form=form)

class InformationForm(Form):
	id = StringField("请输入学号:", validators=[Length(10)])
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


	def __repr__(self):
		return '<Student %r>' % self.name


if __name__ == '__main__':
	db.create_all()
	app.run(host='0.0.0.0',port=8899,debug=True)