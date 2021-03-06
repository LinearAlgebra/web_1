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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12518ll+.@localhost/test1'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'EASY TO GUESS'

@app.route('/', methods=['GET', 'POST'])
def index():
	db.session.rollback()
	form = InformationForm()
	form_1 = QueryForm()
	student_data = db.session.query(Student).all()
	if form.validate_on_submit():
		student = Student.query.filter_by(student_number=form.student_number.data).first()
		students = Student(student_number=form.student_number.data,name=form.name.data)
		if student is None:
			db.session.add(students)
			db.session.commit()
			flash('信息录入成功')
			student_data = db.session.query(Student).all()
			return render_template('personal_information.html', form=form, form_1=form_1,data=student_data)
			session['known'] = False
		else:
			db.session.merge(students)
			db.session.commit()
			flash('信息已更新')
			student_data = db.session.query(Student).all()
			return render_template('personal_information.html', form=form, form_1=form_1,data=student_data)
	if form_1.validate_on_submit():
		db.session.rollback()
		# students_ = Student(student_number=form_1.student_number_.data,name=form_1.name_.data)
		query_ans = Student.query.filter_by(student_number=form_1.student_number_.data,name=form_1.name_.data).first()
		if query_ans:
			db.session.delete(query_ans)
			db.session.commit()
			flash('信息已移除')
		else:
			flash('查无此人，请检查信息是否正确')
		student_data = db.session.query(Student).all()
		return render_template('personal_information.html', form=form, form_1=form_1, data=student_data)
	db.session.rollback()
	flash('有兴趣参加随机分组的同学，可以把信息留到周末，我们到时候随机~~~')
	flash('由于服务器比较慢，如果看到一大串英文，后退重来一次即可~~~')
	return render_template('personal_information.html', form=form, form_1=form_1,data=student_data)

class InformationForm(Form):
	student_number = StringField("请输入学号:", validators=[Length(10)])
	name = StringField("请输入姓名:", validators=[Required()])
	submit = SubmitField("提交信息，寻找队友")

class QueryForm(Form):
	student_number_ = StringField("请输入学号:", validators=[Length(10)])
	name_ = StringField("请输入姓名:", validators=[Required()])
	submit = SubmitField("已找到队伍，在候选名单中移除本人")

class Student(db.Model):
	__tablename__ = 'student_group'
	student_number = db.Column(db.String(10), primary_key=True,unique=True)
	name = db.Column(db.String(64))

	def __repr__(self):
		return self.name

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8848,debug=True)