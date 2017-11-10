import socket
import sys
import mysql.connector
from threading import Thread 
import select

class clienthandler(Thread):
	def __init__(self,client,number):
		Thread.__init__(self)


sockets=[]#buat kumpulan client
idPort = []

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_address=('localhost',5000)

print >> sys.stderr,'starting up on %s port %s'%server_address
sock.bind(server_address)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(1)
sockets.append(sock)
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
	cnx = mysql.connector.connect(host='localhost',database='fp',user='root',password='')
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

def cekpwd(usr,pwd):
	#print usr
	#print pwd
	a=[]
	cnx = mysql.connector.connect(host='localhost',database='fp',user='root',password='')
	cursor = cnx.cursor(buffered=True)
	add_user = "SELECT * FROM user WHERE nama=%s and password=%s"


	cursor.execute(add_user,(usr,pwd,))
	data = cursor.fetchall()
	for row in data:
		a.append(row)
	#emp_no = cursor.lastrowid
	cnx.commit()

	cursor.close()
	cnx.close()
	if len(a)>0:
		return 1
	else:
		return 0

def broadcast(sockx,message):
	for skt in sockets:
		if skt!=sock and skt!=sockx:
			try :
				print "pesan berhasil dikirim"
		                skt.send(message)
			except:
				print "tidak berhasil dikirim"
				skt.close()
				sockets.remove(skt)
			

input_socket=[sock]
try:
	while True:
		read_sockets,write_sockets,error_sockets = select.select(sockets,[],[])
		for sockx in read_sockets:
			if sock==sockx:
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
							masukdb(usr,pwd)
					elif pil=="1":
						print "login"
						usr = client.recv(100)
						pwd = client.recv(100)
						a=cekpwd(usr,pwd)
						if a==0:
							client.sendto("Gagal Login!",address)
						else:
							client.sendto("Berhasil Login!",address)
							cekk=1
			else:
				try:
					datax = sockx.recv(1024)
					if datax=="close":
						print "mati"
						sockx.close()
						sockets.remove(sockx)
						continue
					elif datax:
						print "hidup"
						broadcast(sockx,datax)
						print datax
				except:
					print "mati"
					print sockx
					sockx.close()
					sockets.remove(sockx)
					continue
					#print "Client (%s, %s) is offline" % addr
		

except KeyboardInterrupt:
	sock.close()
sys.exit(0)
