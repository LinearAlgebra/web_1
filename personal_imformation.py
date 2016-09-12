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
	pass




class InformationForm(Form):
	train_num = StringField("Input train number:", validators=[Required()])
	a_station = StringField("Input arriving station:", validators=[Required()])
	email = StringField("Input your email address:", validators=[Email()])
	time_interval = IntegerField("Input time interval (unit: second):", validators=[NumberRange(600,6000)])
	submit = SubmitField("Submit")

class Student(db.Model):
	__tablename__ = 'students'
	student_number = db.Column(db.SmallInteger, primary_key=True,unique=True)
	name = db.Column(db.String(64))
	identity = db.relationship('Detail_Info', backref='identity')

	def __repr__(self):
		return '<Student %r>' % self.name

class Detail_Info(db.Model):
	__tablename__ = 'detail_info'
	student_number = db.Column(db.SmallInteger, db.ForeignKey('students.student_number'),primary_key=True,unique=True)
	phonenumber = db.Column(db.String(64))

	def __repr__(self):
		return '<Phonenumber %r>' % self.phonenumber

if __name__ == '__main__':
	manager.run()