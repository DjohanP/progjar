import socket
import sys
import mysql.connector
from threading import Thread 
import select
import json
import base64

current_user = []
listSocketUsername = {}
listNumberUsername = {}
class clienthandler(Thread):
	def __init__(self,client,number):
		global sockets
		global idPort		
		Thread.__init__(self)
		self._client = client
		self._number = number
	def run(self):
		global listNumberUsername
		cekk=0
		while (1):			
			while cekk==0:
				pil = self._client.recv(100)
				print pil
				if pil=="2":
					print "reg"
					usr = self._client.recv(100)
					pwd = self._client.recv(100)
					print usr
					print pwd
					a=cekusr(usr)
					if a==0:
						self._client.send("Sudah Ada")
					else:	
						self._client.send("Belum Ada")
						masukdb(usr,pwd)
				elif pil=="1":
					print "login"
					usr = self._client.recv(100)
					pwd = self._client.recv(100)
					print usr
					print pwd
					a=cekpwd(usr,pwd,self._client)
					if a==0:
						self._client.send("Gagal Login!")
					else:
						listNumberUsername[str(self._number)] = usr
						self._client.send("Berhasil Login!")
						cekk=1
				elif pil=="0":
					print "Client Disconnected"
					
			while cekk == 1:
				men_grp = 0
				grup = 0
				pill = self._client.recv(100)
				if pill == "1":
					data = getUserOnline()
					data = json.dumps(data)
					print data
					self._client.send(data)
				if pill == "2":
					lawan = self._client.recv(100)
					action = self._client.recv(100)
					global listSocketUsername
					sock_lawan = listSocketUsername[lawan]
					if(action == '1'):
						chats = getChatHistory(listNumberUsername[str(self._number)], lawan)
						print chats
						chats = json.dumps(chats)
						self._client.send(chats)
						chat(lawan, self._client, sock_lawan, self._number)
						print "RETURNED!"
					elif(action == '2'):
						chats = getChatHistory(listNumberUsername[str(self._number)], lawan)
						print chats
						chats = json.dumps(chats)
						self._client.send(chats)
						terimaChat(lawan, self._client, sock_lawan, self._number)
				if pill == "4":
					men_grp = 1
					while men_grp == 1:
						men = self._client.recv(100)
						if men == "1":
							nama_grup = self._client.recv(100)
							print nama_grup
							createGroup(nama_grup)
							self._client.send('Berhasil Membuat Grup')
						#while grup == 1:
						#	nama_grup = self._client.recv(100)
						#	print nama_grup
						#	createGroup(nama_grup)
						#	grup = 0
						#	self._client.send('Berhasil Membuat Grup')
						elif men == "2":
							data = getGroup()
							data = json.dumps(data)
							print data
							self._client.send(data)
						elif men == "0":
							men_grp = 0
							break
				if pill == "0":
					a = doLogout()
					cekk = 0
					self._client.send('1')
			
		
		


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
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
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
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
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

def cekpwd(usr,pwd,sockclient):
	#print usr
	#print pwd
	global current_user
	a=[]
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
	cursor = cnx.cursor(buffered=True)
	add_user = "SELECT * FROM user WHERE nama=%s and password=%s"


	cursor.execute(add_user,(usr,pwd,))
	data = cursor.fetchall()
	for row in data:
		a.append(row)
	#emp_no = cursor.lastrowid
	cnx.commit()
	
	if len(a)>0:
		cursor = cnx.cursor(buffered=True)
		change_status = "UPDATE user SET status='1' WHERE id=%d"
		cursor.execute(change_status % (a[0][0]))
		cnx.commit()
		current_user = a
		#print 'a = ', a
		#print 'cur = ', current_user
		global listSocketUsername
		listSocketUsername[str(a[0][1])] = sockclient
		print listSocketUsername
		cursor.close()
		cnx.close()	
		return 1
	else:
		cursor.close()
		cnx.close()
		return 0
	
def getUserOnline():
	global current_user
	a=[]
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
	cursor = cnx.cursor(buffered=True)
	query = "SELECT * FROM user WHERE status = 1"

	cursor.execute(query)
	data = cursor.fetchall()
	for row in data:
		a.append(row)
	
	cnx.commit()
	
	return a

def getGroup():
	global current_user
	a=[]
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
	cursor = cnx.cursor(buffered=True)
	query = "SELECT * FROM grup"

	cursor.execute(query)
	data = cursor.fetchall()
	for row in data:
		a.append(row)
	
	cnx.commit()
	
	return a


def doLogout():
	global current_user
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
	cursor = cnx.cursor(buffered=True)
	query = "UPDATE user SET status='0' WHERE id=%d"
	
	print current_user
	print current_user[0][0]
	#print query % (current_user[0])
	cursor.execute(query % (current_user[0][0]))
	cnx.commit()
	
	cursor.close()
	cnx.close()
	
	return 1

def chat(lawan, sock, sock_lawan, thread_number):
	global listNumberUsername
	while(1):
		#print 'masuk fungsi chat'
		pengirim = listNumberUsername[str(thread_number)]
		#print pengirim
		pesan = sock.recv(100)
		#print pesan
		sock_lawan.send(pesan)
		if(pesan == '0'):
			break
		if(pesan == '<<EXIT>>'):
			return
		else:
			insertChat(pengirim, lawan, pesan)
			print 'sent', pesan, 'to', sock_lawan
	terimaChat(lawan, sock, sock_lawan, thread_number)

def terimaChat(lawan, sock, sock_lawan, thread_number):
	while(1):
		pesan = sock.recv(100)
		print 'FROM CLIENT ->', pesan
		if(pesan == '0'):
			break
		if(pesan == '<<EXIT>>'):
			return
		else:
			print lawan+':', pesan
	chat(lawan, sock, sock_lawan, thread_number)

def enkripsi(pesan):
	return base64.b64encode(pesan)
	
def insertChat(dari, ke, pesan):
	pesan = enkripsi(pesan)
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
	cursor = cnx.cursor(buffered=True)
	query = "INSERT INTO pesan (nama_pengirim, nama_penerima, pesan) VALUES ('%s', '%s', '%s')"
	
	print query % (dari, ke, pesan)
	cursor.execute(query % (dari, ke, pesan))
	cnx.commit()
	
	cursor.close()
	cnx.close()
	
	return 1

def getChatHistory(pengirim, penerima):
	chats = []
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
	cursor = cnx.cursor(buffered=True)
	query = """SELECT nama_pengirim, nama_penerima, pesan FROM pesan 
			   WHERE nama_pengirim='%s' AND nama_penerima='%s'
			   OR nama_pengirim='%s' AND nama_penerima='%s' ORDER BY created_at"""
	
	print query % (pengirim, penerima, penerima, pengirim)
	cursor.execute(query % (pengirim, penerima, penerima, pengirim))
	data = cursor.fetchall()
	for row in data:
		chats.append(row)
	cnx.commit()
	
	cursor.close()
	cnx.close()
	
	return chats

def createGroup(nama_grup):
	cnx = mysql.connector.connect(host='localhost',database='fp',user='fp',password='fp')
	cursor = cnx.cursor()
	query = "INSERT INTO grup (nama) VALUES ('%s')"
	cursor.execute(query % (nama_grup))
	#emp_no = cursor.lastrowid
	cnx.commit()

	cursor.close()
	cnx.close()

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
		handlers = []
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
				newthread = clienthandler(client,address[1])
				handlers.append(newthread)
				newthread.daemon = True				
				newthread.start()
				

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
			#for x in handlers:
			#	x.join()
		

except KeyboardInterrupt:
	sock.close()
sys.exit(0)
