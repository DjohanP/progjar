import socket
import sys
import base64
import select
import os
import json

BUFSIZE=100

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
print >>sys.stderr, 'connecting to %s port %s' % server_address
nama = ''
def printMenu():
	print "--Cetingan Messenger--"
	print "1. Login"
	print "2. Register"
	print "0. Keluar"
	print "Pilihan : "
	
def printMenuMasuk(name):
	print "Halo "+name+"!"
	print "Selamat Datang di Cetingan Messenger"
	print "------------------------------------"
	print "1. List user online"
	print "2. Private Chat"
	print "3. Broadcast"
	print "4. Group Chat"
	print "0. Logout"

def printGroupMenu():
	print "-----Grup Chat Beranda-----"
	print "1. Create Grup Chat"
	print "2. List Grup Chat"
	print "3. Grup Chat"
	print "0. Kembali Ke Menu Utama"

def printGroupChat():
	print "----------(Masukkan Nama Grup)-----------"

# def printGroupRoom(name, sock):
# 	print "-------------------------------------------------------------"
# 	print "Grup ", name
# 	print "Mode: Mengirim Pesan"
# 	print "Petunjuk: "
# 	print "- Masukkan 0 jika ingin mengahiri pengiriman pesan"
# 	print "  dan berubah menjadi mode menerima pesan"
# 	print "- Masukkan <<EXIT>> untuk mengahiri percakapan"
# 	print "-------------------------------------------------------------"
# 	while(1):
# 		pesan = raw_input('> ')
# 		sock.send(pesan)
# 		if(pesan == '0'):
# 			break
# 		if(pesan == '<<EXIT>>'):
# 			return
	
# 	chatRoomRecv(name, sock)


def printPesan(pesan):
	for i in xrange(0, len(pesan)+4):
		sys.stdout.write("-")
	print "\n| "+pesan+" |"
	for i in xrange(0, len(pesan)+4):
		sys.stdout.write("-")
	
	print ''

def printBack():
	print "(Masukkan apapun untuk kembali ke menu)"

def decrypt(msg):
	return base64.b64decode(msg)

def getChatHistory(sock):
	chats = json.loads(sock.recv(1024))
	#print chats
	
	print '>> Chat History <<\n'
	for chat in chats:
		print str(chat[0])+'\t:', decrypt(str(chat[2]))
	print '>> Chat History END <<'

def chatRoomRecv(name, sock):
	print "-------------------------------------------------------------"
	print "Chatting dengan", name
	print "Mode: Menerima Pesan"
	print "Petunjuk: Akan otomatis berubah ke mode mengirim pesan ketika "+name
	print "sudah mengahiri pengiriman pesannya"
	print "-------------------------------------------------------------"
	
	while(1):
		pesan = sock.recv(100)
		sock.send(pesan)
		if(pesan == '0'):
			break
		elif(pesan == '<<EXIT>>'):
			return
		else:
			print name+':', pesan
		
	print 'Chat Ended'
	chatRoomSend(name, sock)

def broadcastRoomRecv(sock):
	print "-------------------------------------------------------------"
	print "Mode: Menerima Broadcast"
	print "-------------------------------------------------------------"
	
	while(1):
		pesan = sock.recv(100)
		sock.send(pesan)
		if(pesan == '0'):
			break
		elif(pesan == '<<EXIT>>'):
			return
		else:
			print '>', pesan
		
	print 'Chat Ended'


def chatRoomSend(name, sock):
	print "-------------------------------------------------------------"
	print "Chatting dengan", name
	print "Mode: Mengirim Pesan"
	print "Petunjuk: "
	print "- Masukkan 0 jika ingin mengahiri pengiriman pesan"
	print "  dan berubah menjadi mode menerima pesan"
	print "- Masukkan <<EXIT>> untuk mengahiri percakapan"
	print "-------------------------------------------------------------"
	while(1):
		pesan = raw_input('> ')
		sock.send(pesan)
		if(pesan == '0'):
			break
		if(pesan == '<<EXIT>>'):
			return
	
	chatRoomRecv(name, sock)

def broadcastRoomSend(sock):
	print "-------------------------------------------------------------"
	print "Mode: Broadcast Mengirim Pesan"
	print "Petunjuk: "
	print "- Masukkan <<EXIT>> untuk mengahiri broadcast"
	print "-------------------------------------------------------------"
	while(1):
		pesan = raw_input('> ')
		sock.send(pesan)
		if(pesan == '<<EXIT>>'):
			return

pesan = ''
cek=0
while(1):
	while cek==0:
		os.system('clear')
		if (pesan != ''):
			printPesan(pesan)
		pesan = ''
		printMenu()
		pil=raw_input()
		client_socket.send(pil)
		#print pil
		if pil=="2":
			print "Masukkan username anda :"
			msg = raw_input()
			client_socket.send(msg)
			print "Masukkan password anda :"
			message = raw_input()
			client_socket.send(message)
			psn=client_socket.recv(1000)
			if(psn=="Sudah Ada"):
				pesan = "Username Sudah Terdaftar!"
			else:
				nama=msg
				pesan = 'Registrasi Berhasil!'
		elif pil=="1":
			print "Masukkan username anda :"
			msg = raw_input()
			client_socket.send(msg)
			print "Masukkan password anda :"
			message = raw_input()
			client_socket.send(message)
			psn=client_socket.recv(1000)
			if(psn=="Gagal Login!"):
				pesan = "User belum terdaftar / password salah"
			else:
				global nama
				nama=msg
				pesan = "Berhasil Login!"
				cek=1
		elif pil=="0":
			client_socket.close()
			sys.exit(0)	
		else:
			print "Inputan salah"

	while cek == 1:
		os.system('clear')
		if (pesan != ''):
			printPesan(pesan)
		pesan = ''
		printMenuMasuk(nama)
		selected = raw_input()
		grup=0
		if(selected == "1"):
			client_socket.send(selected)
			onuser = client_socket.recv(1024)
			print onuser
			onuser = json.loads(onuser)
			print onuser
			os.system('clear')
			print 'User Online:\n'
			for index, user in enumerate(onuser):
				print index+1, '->', user[1]
			
			print ''
			printBack()
			raw_input()
			
		if(selected == "2"):
			client_socket.send(selected)
			tujuan = raw_input('Tulis nama yang akan kamu chat: ')
			client_socket.send(tujuan)
			action = raw_input('Masukkan 1 untuk mengirim pesan atau 2 untuk menerima pesan: ')
			client_socket.send(action)
			os.system('clear')
			if(action == '1'):
				getChatHistory(client_socket)
				chatRoomSend(tujuan, client_socket)
			if(action == '2'):
				getChatHistory(client_socket)
				chatRoomRecv(tujuan, client_socket)
		if(selected == "3"):
			client_socket.send(selected)
			action = raw_input('Masukkan 1 untuk mengirim pesan atau 2 untuk menerima pesan: ')
			client_socket.send(action)
			os.system('clear')
			if(action == '1'):
				broadcastRoomSend(client_socket)
			if(action == '2'):
				broadcastRoomRecv(client_socket)
		if(selected == "4"):
			client_socket.send(selected)
			grup=1
			while grup == 1:
				os.system('clear')
				if (pesan != ''):
					printPesan(pesan)
				pesan = ''
				printGroupMenu()
				gc_menu = raw_input()
				client_socket.send(gc_menu)
				if(gc_menu == "1"):
					print "(Masukkan Nama Grup Yang Akan Dibuat)"
					nama_grup = raw_input()
					client_socket.send(nama_grup)
					pesan = client_socket.recv(100)
				if(gc_menu == "2"):
					ongrup = client_socket.recv(100)
					# print onuser
					ongrup = json.loads(ongrup)
					print ongrup
					os.system('clear')
					print 'List Grup:\n'
					for index, grupku in enumerate(ongrup):
						print index+1, '->', grupku[1]
					
					print ''
					printBack()
					raw_input()
				if(gc_menu == "0"):
					grup=0
					break

			
		if(selected == "0"):
			client_socket.send(selected)
			ret = client_socket.recv(100)
			if(ret == '1'):
				pesan = 'Berhasil Logout!'
				cek = 0
		

try:
	while True:
		socket_list = [sys.stdin, client_socket]
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		for sock in read_sockets:
			if sock == client_socket:
				data = sock.recv(4096)
				if not data :
					print "koneksi mati"
					client_socket.close()
					exit()
				else:
					print data
			else:
				print nama		
				msg = raw_input()
				if msg=="close":
					client_socket.send(msg)
					client_socket.close()
					exit()

				msg = "\r"+"<"+str(nama)+">"+msg
				client_socket.send(msg)

except KeyboardInterrupt:
	client_socket.close()
sys.exit(0)
