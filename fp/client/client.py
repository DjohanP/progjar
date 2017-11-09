import socket
import sys


BUFSIZE=100
server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
print >>sys.stderr, 'connecting to %s port %s' % server_address
pil=raw_input("1. Login\n2. Register\nPilihan : ")
client_socket.send(pil)
print pil
if pil=="2":
	print "Masukkan nama anda :"
	message = raw_input()
	client_socket.send(message)
	print "Masukkan password anda :"
	message = raw_input()
	client_socket.send(message)

try:
	while True:
		input()

except KeyboardInterrupt:
	client_socket.close()
sys.exit(0)
