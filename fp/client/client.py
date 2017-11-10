import socket
import sys
import select

BUFSIZE=100

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
print >>sys.stderr, 'connecting to %s port %s' % server_address
cek=0
while cek==0:
	pil=raw_input("MENU AWAL!\n1. Login\n2. Register\nPilihan : ")
	client_socket.send(pil)
	print pil
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
			print psn
		else:
			nama=msg
			print "Berhasil Login!"
			cek=1
	else:
		print "Inputan salah"


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
