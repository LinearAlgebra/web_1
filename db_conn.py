import MySQLdb


a =  'mysql://root:12518ll+.@http://52.23.150.84:3306/mysql'
conn = MySQLdb.connect(host='52.23.150.84',port=3306,user='root',passwd='12518ll+.',db='mysql')

cur = conn.cursor()
