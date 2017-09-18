import sys
import socket
import datetime
import time

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_address=('localhost',17038)
print >> sys.stderr,'starting up on %s port %s'%server_address
sock.bind(server_address)

sock.listen(1)
while True:
	print >>sys.stderr,'waiting for a connection'
	socket_si_client,client_address=sock.accept()
	print >> sys.stderr,'connection from',client_address
	socket_si_client.sendall('Menu:\n1. Kuadrat 2\n2. Ucapan\n3. Waktu server\nPilihan : ')
	menu=socket_si_client.recv(100)
	menu2=int(menu)
	if(menu2==1):
		#print('Masih belum')
		angka=socket_si_client.recv(100)
		angka2=int(angka)
		angka3=angka2*angka2
		angka4=str(angka3)
		socket_si_client.sendall(angka4+'\n')
	elif(menu2==2):
		pesan_dari_client=socket_si_client.recv(100)
		print pesan_dari_client
		#pesan=pesan_dari_client[0:4]
		#print pesan
		if(pesan_dari_client[0:4] == 'Pagi'):
			socket_si_client.sendall('Semangat Pagi\n')
		elif(pesan_dari_client[0:4]=='Sore'):
			socket_si_client.sendall('Semangat Sore\n')
		elif(pesan_dari_client[0:5]=='Malam'):
			socket_si_client.sendall('Jangan lupa tugas buat besok\n')
		else:
			socket_si_client.sendall('Semangat Terus\n')
		#socket_si_client.sendall('Dari server -->'+pesan_dari_client)
		#socket_si_client.sendall('Ada apa ??'+'hehe')
	elif(menu2==3):
		localtime=time.asctime(time.localtime(time.time()))
		localtime2=str(localtime)
		socket_si_client.sendall(localtime2+'\n')
	else:
		socket_si_client.sendall('Menu yang dimasukkan salah\n')
		#print('Menu yang dimasukkan salah')
	socket_si_client.close()
