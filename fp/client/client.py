import socket
import sys


BUFSIZE=100
server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
print >>sys.stderr, 'connecting to %s port %s' % server_address
try:
	while True:
		message = sys.stdin.readline()
		data= client_socket.recv(100)
		print data
		client_socket.send(message)
		#print message

except KeyboardInterrupt:
	client_socket.close()
sys.exit(0)
