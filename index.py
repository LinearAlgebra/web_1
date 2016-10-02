from select_daoshi import *

@app.route('/turtor', methods=['GET', 'POST'])
def turtor():
	form = InformationForm()
	if form.validate_on_submit():
		student = Student.query.filter_by(id=form.id.data).first()
		student_1 = Student(id=form.id.data,
							name=form.name.data,
							daoshi_1=form.daoshi_1.data,
							daoshi_2=form.daoshi_2.data,
							daoshi_3=form.daoshi_3.data,
							phone = form.phone.data,
							stime = time.strftime("%Y-%m-%d %H:%M:%S"))
		if student is None:
			db.session.add(student_1)
			db.session.commit()
			flash('信息录入成功','alert alert-success')
			return render_template('select_daoshi.html', form=form)
		else:
			if student.name == student_1.name and [student.daoshi_1,student.daoshi_2,student.daoshi_3] == [student_1.daoshi_1,student_1.daoshi_2,student_1.daoshi_3] and student.phone==student_1.phone:
				flash('该学号已登记，登记时间为%s，你此次输入的信息与数据库中保存的信息相符' % student.stime, 'alert alert-success')
			else:
				flash('该学号已登记，登记时间%s, 并且你此次输入的信息与数据库保存的信息不符。如需更改登记信息请微信联系管理员，或用本人南开邮箱发送邮件至2120162310@mail.nankai.edu.cn' % student.stime, 'alert alert-danger')
			db.session.rollback()
			return render_template('select_daoshi.html', form=form)
	flash('为了防止个人志愿被篡改，在本网页只能提交一次志愿。之后如需要更改，可直接通过微信或者通过南开邮箱联系我2120162310@mail.nankai.edu.cn（发件时请使用本人南开邮箱）','alert alert-info')
	return render_template('select_daoshi.html', form=form):

if __name__ == '__main__':
	db.create_all()
	app.run(host='0.0.0.0',port=80)
