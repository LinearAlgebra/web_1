from flask import Flask, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return redirect('http://www.guqingzhe.com/temp/taitong/pages/myprofile.php')

if __name__ == '__main__':
	# db.create_all()
	app.run(host='0.0.0.0',port=8889)