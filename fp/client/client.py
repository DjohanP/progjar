import socket
import sys


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


try:
	while True:
		print nama
		input()

except KeyboardInterrupt:
	client_socket.close()
sys.exit(0)
