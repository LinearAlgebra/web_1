from flask import Flask, render_template, flash
from flask_script import Manager
from flask.ext.bootstrap import Bootstrap

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Email, NumberRange
import threading, sys
sys.path.append('./web_model')
import train_monitor

app = Flask(__name__)
# manager = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'EASY TO GUESS'

@app.route('/user/<name>')
def hello(name):
	return render_template('base.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	flash('只能查询过去一小时至未来三小时的晚点情况~~~')
	if form.validate_on_submit():
		train_num = form.train_num.data
		a_station = form.a_station.data
		email = form.email.data
		time_interval = form.time_interval.data
		try:
			threading.Thread(target=train_monitor.train_monitor, args=(train_num,a_station, email, time_interval)).start()
			flash('列车晚点监控程序启动成功！')
			return render_template('train_monitor.html', form=form)
		except:
			return render_template('train_monitor.html', form=form, data=['程序启动失败！'])
	return render_template('train_monitor.html', form=form)

class NameForm(Form):
	train_num = StringField("Input train number:", validators=[Required()])
	a_station = StringField("Input arriving station:", validators=[Required()])
	email = StringField("Input your email address:", validators=[Email()])
	time_interval = IntegerField("Input time interval (unit: second):", validators=[NumberRange(600,6000)])
	submit = SubmitField("Submit")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8421)
