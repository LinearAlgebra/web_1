from flask import Flask
from flask import abort
from flask import redirect
import os
import web_model.train_monitor

app = Flask(__name__)

@app.route('/')
def index():
	return '<h1> Hello World!</h1>'

@app.route('/xtt/<order>')
def run_order(order):
	os.system(order)

if __name__=='__main__':
	app.run(debug=True, host = '0.0.0.0', port = 8421)
