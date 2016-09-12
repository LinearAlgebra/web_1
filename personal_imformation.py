from flask import Flask, render_template
from flask_script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Email, NumberRange
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12518ll+.@localhost/test1'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
	form = InformationForm()
	if form.validate_on_submit():
		student = Student.query(student_number=form.name.data).first()
		if student is None:
			student = Student(student_number=form.student_number.data,name=form.name.data)
			detail = Detail_Info(phone_number=form.phone_number.data,identity=student)
			db.session.add([student,detail])
			db.session.commit()
			return '<h1> 2333 </h1>'
			session['known'] = False


class InformationForm(Form):
	student_number = IntegerField("请输入学号:", validators=[Required()])
	name = StringField("请输入姓名:", validators=[Required()])
	phone_number = IntegerField("请输入电话号码:", validators=[Required()])
	submit = SubmitField("Submit")

class Student(db.Model):
	__tablename__ = 'students'
	student_number = db.Column(db.String(64), primary_key=True,unique=True)
	name = db.Column(db.String(64))
	identity = db.relationship('Detail_Info', backref='identity')

	def __repr__(self):
		return '<Student %r>' % self.name

class Detail_Info(db.Model):
	__tablename__ = 'detail_info'
	student_number = db.Column(db.String(64), db.ForeignKey('students.student_number'),primary_key=True,unique=True)
	phone_number = db.Column(db.String(64))

	def __repr__(self):
		return '<Phonenumber %r>' % self.phonenumber

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=8842)