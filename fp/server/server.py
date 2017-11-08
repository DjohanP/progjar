import socket
import sys

sockets=[]#buat kumpulan client
idPort = []

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_address=('localhost',5000)

print >> sys.stderr,'starting up on %s port %s'%server_address
sock.bind(server_address)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(1)

input_socket=[sock]
try:
	while True:
		client, address = sock.accept()
		sockets.append(client)
		#print client
		#print address
		print('client connected from: ',address[0],'with id : ', address[1])
		idPort.append(address[1])
		client.sendto("Masukkan nama anda: ",address)
		data = client.recv(100)
		print data

except KeyboardInterrupt:
	sock.close()
sys.exit(0)
