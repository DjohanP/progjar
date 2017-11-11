import socket
import sys
import select
import os
import json

BUFSIZE=100

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
print >>sys.stderr, 'connecting to %s port %s' % server_address

def printMenu():
	print "--Cetingan Messenger--"
	print "1. Login"
	print "2. Register"
	print "0. Keluar"
	print "Pilihan : "
	
def printMenuMasuk():
	print "Selamat Datang di Cetingan Messenger"
	print "------------------------------------"
	print "1. List user online"
	print "2. Private Chat"
	print "3. Broadcast"
	print "0. Logout"

def printBack():
	print "(Masukkan apapun untuk kembali ke menu)"


pesan = ''
cek=0
while(1):
	while cek==0:
		os.system('clear')
		if (pesan != ''):
			print pesan
		pesan = ''
		printMenu()
		pil=raw_input()
		client_socket.send(pil)
		#print pil
		if pil=="2":
			print "Masukkan email anda :"
			msg = raw_input()
			client_socket.send(msg)
			print "Masukkan password anda :"
			message = raw_input()
			client_socket.send(message)
			psn=client_socket.recv(1000)
			if(psn=="Sudah Ada"):
				print "Email Sudah Ada!"
			else:
				nama=msg
				print "Akun anda sudah masuk"
				cek=1
		elif pil=="1":
			print "Masukkan email anda :"
			msg = raw_input()
			client_socket.send(msg)
			print "Masukkan password anda :"
			message = raw_input()
			client_socket.send(message)
			psn=client_socket.recv(1000)
			if(psn=="Gagal Login!"):
				pesan = psn
			else:
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
			print pesan
		pesan = ''
		printMenuMasuk()
		selected = raw_input()
		
		if(selected == "1"):
			client_socket.send(selected)
			onuser = client_socket.recv(100)
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
