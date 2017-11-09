import mysql.connector
a=[]
#mysql.connector.connect(host='localhost',database='fp',user='root',password='')
#sudo dpkg -i mysql-connector-python_2.0.5-1ubuntu16.04_all.deb install mysql
cnx = mysql.connector.connect(host='localhost',database='fp',user='root',password='')
cursor = cnx.cursor(buffered=True)
email=('djohan.prabowo1927@gmail.com')
add_user = "SELECT * FROM user WHERE nama=%s"


cursor.execute(add_user,(email,))
data = cursor.fetchall()
for row in data:
	a.append(row)
#emp_no = cursor.lastrowid
cnx.commit()

cursor.close()
cnx.close()

print len(a)
#if len(a)>0:
#	return 0#ada datanya
#else:
	#return 1#tidak ada datanya
