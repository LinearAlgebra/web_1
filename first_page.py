from flask import Flask
from flask import abort
from flask import redirect
import os, sys, urllib.request
sys.path.append('./web_model')

import train_monitor, emailsender

app = Flask(__name__)

@app.route('/')
def index():
	return '<h1> Hello World!</h1>'

@app.route('/train_monitor/<order>')
def run_order(order):
	order_str = urllib.request.unquote(order)
	order_list = order_str.split(' ')
	try:
		train_monitor.train_monitor(order_list[0], order_list[1], order_list[2], order_list[3])
	except BaseException as e:
		return '<h1> 抓取错误 %s </h1>' % e

if __name__=='__main__':
	app.run(debug=True, host = '0.0.0.0', port = 8421)
