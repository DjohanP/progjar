import sys
import socket
import datetime
import time
from lib import *

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_address=('localhost',17083)
print >> sys.stderr,'starting up on %s port %s'%server_address
sock.bind(server_address)

sock.listen(1)
while True:
	print >>sys.stderr,'waiting for a connection'
	socket_si_client,client_address=sock.accept()
	print >> sys.stderr,'connection from',client_address
	#socket_si_client.sendall('Menu:\n1. Kuad')
	menu=socket_si_client.recv(100)
	a=spl(menu)
	if(a==1):
		cmd,param1,param2=menu.split(" ")
		hasil=fungsi(cmd,param1,param2)
		socket_si_client.sendall(str(hasil)+'\n')
	else:
		socket_si_client.sendall('Error\n')
	socket_si_client.close()
