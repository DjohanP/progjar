import socket
import sys
import mysql.connector

sockets=[]#buat kumpulan client
idPort = []

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_address=('localhost',5000)

print >> sys.stderr,'starting up on %s port %s'%server_address
sock.bind(server_address)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(1)

def masukdb(user,passw):
	print user
	print passw
	
	#mysql.connector.connect(host='localhost',database='fp',user='root',password='')
	#sudo dpkg -i mysql-connector-python_2.0.5-1ubuntu16.04_all.deb install mysql
	cnx = mysql.connector.connect(host='localhost',database='fp',user='root',password='')
	cursor = cnx.cursor()
	add_user = ("INSERT INTO user "
		       "(nama, password) "
		       "VALUES (%s, %s)")
	data_user = (user, passw)
	cursor.execute(add_user, data_user)
	#emp_no = cursor.lastrowid
	cnx.commit()

	cursor.close()
	cnx.close()

def cekusr(usr):
	a=[]
	cnx = mysql.connector.connect(host='localhost',database='fp',user='root',password='imanuel89')
	cursor = cnx.cursor(buffered=True)
	add_user = "SELECT * FROM user WHERE nama=%s"


	cursor.execute(add_user,(usr,))
	data = cursor.fetchall()
	for row in data:
		a.append(row)
	#emp_no = cursor.lastrowid
	cnx.commit()

	cursor.close()
	cnx.close()
	if len(a)>0:
		return 0
	else:
		return 1

	

input_socket=[sock]
try:
	while True:
		client, address = sock.accept()
		sockets.append(client)
		#print client
		#print address
		print('client connected from: ',address[0],'with id : ', address[1])
		idPort.append(address[1])
		#client.sendto("Masukkan nama anda: ",address)

		cekk=0
		while cekk==0:
			pil = client.recv(100)
			print pil
			if pil=="2":
				print "reg"
				usr = client.recv(100)
				pwd = client.recv(100)
				#print usr
				#print pwd
				a=cekusr(usr)
				if a==0:
					client.sendto("Sudah Ada",address)
				else:	
					client.sendto("Belum Ada",address)
					cekk=1
					#masukdb(usr,pwd)
		

except KeyboardInterrupt:
	sock.close()
sys.exit(0)
