import socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
port = 1234
address(ip.port)
server.bind(address)
server.listen(1)
print "[*] Start listening on %s : %s" % (ip, port)
client.addr =  server.accept()
print "[*] Got a connection from %s : %s" % (addr[1], addr[1])
while True:
	data = client.recv(1024)
	print "[*] Received '%s' from the client" % data 
	print "    Processing data"
	if(data=="Hello server"):
		client.send("Hello client")
		print "    Processign done.\n[*] Reply sent"
	elif(data=="disconnect"):
		client.sent("Goodbye")
		client.close()
		break
	else:
		client.send("Invalid data")
		print "    Processing done. Invalid data.\n[*] Reply sent"
