from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
#mysql.connector.connect(host='localhost',database='fp',user='root',password='')
#sudo dpkg -i mysql-connector-python_2.0.5-1ubuntu16.04_all.deb install mysql
cnx = mysql.connector.connect(host='localhost',database='fp',user='root',password='')
cursor = cnx.cursor()
add_user = ("INSERT INTO user "
               "(nama, password) "
               "VALUES (%s, %s)")
data_user = ('Djohan', '123456')
cursor.execute(add_user, data_user)
#emp_no = cursor.lastrowid
cnx.commit()

cursor.close()
cnx.close()
